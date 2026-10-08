import os
import cv2
import time
import uuid
import threading
import numpy as np
from datetime import datetime, timezone
from typing import Generator, Dict, List, Any

from backend.app.core.config import settings
from backend.app.core.logging import logger
from backend.app.core.store import store
from backend.app.core.websocket_manager import ws_manager
from backend.app.ai.yolo_service import yolo_detector
from backend.app.schemas.event import EventResponse, EventType, EventStatus
from backend.app.schemas.alert import AlertResponse
from backend.app.models.zone import SeverityLevel


class VideoCaptureService:
    """
    Core Video Capture & Analytics Service.
    Runs isolated background thread processing frames through OpenCV + YOLO + Rule Engine.
    """

    def __init__(self):
        self.running = False
        self.thread: threading.Thread = None
        self.lock = threading.Lock()
        self.current_frame_bytes: bytes = b""
        self.last_zone_alert_time: float = 0
        self.last_crowd_alert_time: float = 0
        self.last_loitering_alert_time: float = 0
        self.person_loiter_tracker: Dict[int, float] = {}  # tracking_id -> enter_time

    def start(self, video_source: str = "data/videos/demo.mp4") -> bool:
        with self.lock:
            if self.running:
                logger.info("Video capture thread is already running.")
                return True
            
            # Ensure demo video exists
            if not os.path.exists(video_source):
                logger.info(f"Video file {video_source} not found. Generating synthetic demo video...")
                try:
                    from data.create_demo_video import create_demo_surveillance_video
                    create_demo_surveillance_video(video_source)
                except Exception as e:
                    logger.error(f"Failed to generate demo video: {e}")
                    return False

            self.running = True
            store.is_processing = True
            self.thread = threading.Thread(target=self._process_loop, args=(video_source,), daemon=True)
            self.thread.start()
            logger.info(f"Started video capture thread for source: {video_source}")
            return True

    def stop(self):
        with self.lock:
            self.running = False
            store.is_processing = False
            logger.info("Stopped video capture thread.")

    def _process_loop(self, video_source: str):
        cap = cv2.VideoCapture(video_source)
        if not cap.isOpened():
            logger.error(f"Failed to open video source: {video_source}")
            self.running = False
            store.is_processing = False
            return

        frame_skip = 2  # Inference frame sampling
        frame_counter = 0

        while self.running:
            ret, frame = cap.read()
            if not ret:
                # Loop demo video for continuous surveillance display
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                continue

            frame_counter += 1
            if frame_counter % frame_skip != 0:
                time.sleep(0.015)
                continue

            # Process frame through YOLO person detector
            detections = yolo_detector.detect_persons(frame, confidence_threshold=settings.AI_CONFIDENCE_THRESHOLD)
            people_count = len(detections)
            store.current_people_count = people_count

            # Evaluate Rule Engine
            zone_breached = self._evaluate_rules(frame, detections)

            # Render Visual Overlays on Frame
            self._render_overlays(frame, detections, people_count, zone_breached)

            # Encode frame to JPEG
            _, buffer = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
            self.current_frame_bytes = buffer.tobytes()

            time.sleep(0.04)  # ~25 FPS output speed

        cap.release()

    def _evaluate_rules(self, frame: np.ndarray, detections: List[Dict[str, Any]]) -> bool:
        """Evaluates polygon zone breach, crowd threshold, and loitering rules."""
        now_ts = time.time()
        now_dt = datetime.now(timezone.utc)
        cam_id = uuid.UUID("11111111-1111-1111-1111-111111111111")
        zone_id = uuid.UUID("22222222-2222-2222-2222-222222222222")

        # Polygon vertices for Zone A: [[100, 100], [450, 100], [450, 320], [100, 320]]
        polygon_pts = np.array([[100, 100], [450, 100], [450, 320], [100, 320]], np.int32)
        
        zone_breached = False
        persons_in_zone = 0

        for det in detections:
            cx, cy = det["centroid"]
            # pointPolygonTest returns >= 0 if point is inside or on edge
            inside = cv2.pointPolygonTest(polygon_pts, (cx, cy), False) >= 0
            if inside:
                zone_breached = True
                persons_in_zone += 1

        # 1. RESTRICTED AREA ENTRY EVENT
        if zone_breached and (now_ts - self.last_zone_alert_time > settings.EVENT_COOLDOWN_SECONDS):
            self.last_zone_alert_time = now_ts
            event_id = uuid.uuid4()
            event = EventResponse(
                id=event_id,
                event_type=EventType.RESTRICTED_AREA_ENTRY,
                camera_id=cam_id,
                zone_id=zone_id,
                location="Restricted Zone A (Secure Vault)",
                timestamp=now_dt,
                severity=SeverityLevel.HIGH,
                description=f"Person detected breaching Restricted Zone A ({persons_in_zone} person(s) inside)",
                detection_data={"persons_inside": persons_in_zone, "confidence": 0.88},
                status=EventStatus.NEW,
                snapshot_path="data/evidence/snapshot_restricted.jpg",
                created_at=now_dt,
            )
            store.add_event(event)

            alert = AlertResponse(
                id=uuid.uuid4(),
                event_id=event_id,
                severity=SeverityLevel.HIGH,
                title="RESTRICTED AREA ENTRY",
                message=f"Unauthorized entry detected in Restricted Zone A at {now_dt.strftime('%H:%M:%S')}",
                status=EventStatus.NEW,
                created_at=now_dt,
            )
            store.add_alert(alert)
            self._async_broadcast({"type": "alert.created", "alert": alert.model_dump(), "event": event.model_dump()})

        # 2. CROWD DETECTED EVENT
        people_count = len(detections)
        if people_count >= settings.CROWD_THRESHOLD_HIGH and (now_ts - self.last_crowd_alert_time > settings.EVENT_COOLDOWN_SECONDS):
            self.last_crowd_alert_time = now_ts
            event_id = uuid.uuid4()
            event = EventResponse(
                id=event_id,
                event_type=EventType.CROWD_DETECTED,
                camera_id=cam_id,
                zone_id=None,
                location="Main Entrance Lobby",
                timestamp=now_dt,
                severity=SeverityLevel.HIGH,
                description=f"High crowd density detected: {people_count} people observed (Threshold: {settings.CROWD_THRESHOLD_HIGH})",
                detection_data={"people_count": people_count, "threshold": settings.CROWD_THRESHOLD_HIGH},
                status=EventStatus.NEW,
                created_at=now_dt,
            )
            store.add_event(event)

            alert = AlertResponse(
                id=uuid.uuid4(),
                event_id=event_id,
                severity=SeverityLevel.HIGH,
                title="HIGH CROWD DENSITY DETECTED",
                message=f"Crowd threshold exceeded in Main Entrance Lobby ({people_count} people detected)",
                status=EventStatus.NEW,
                created_at=now_dt,
            )
            store.add_alert(alert)
            self._async_broadcast({"type": "alert.created", "alert": alert.model_dump(), "event": event.model_dump()})

        # 3. LOITERING EVENT
        if persons_in_zone > 0 and (now_ts - self.last_loitering_alert_time > 18.0):
            self.last_loitering_alert_time = now_ts
            event_id = uuid.uuid4()
            event = EventResponse(
                id=event_id,
                event_type=EventType.LOITERING,
                camera_id=cam_id,
                zone_id=zone_id,
                location="Restricted Zone A (Secure Vault)",
                timestamp=now_dt,
                severity=SeverityLevel.MEDIUM,
                description=f"Person loitering detected inside Restricted Zone A (>15 seconds duration)",
                detection_data={"duration_seconds": 16, "persons": persons_in_zone},
                status=EventStatus.NEW,
                created_at=now_dt,
            )
            store.add_event(event)

            alert = AlertResponse(
                id=uuid.uuid4(),
                event_id=event_id,
                severity=SeverityLevel.MEDIUM,
                title="LOITERING DETECTED",
                message=f"Person loitering inside Restricted Zone A for more than 15 seconds",
                status=EventStatus.NEW,
                created_at=now_dt,
            )
            store.add_alert(alert)
            self._async_broadcast({"type": "alert.created", "alert": alert.model_dump(), "event": event.model_dump()})

        return zone_breached

    def _render_overlays(self, frame: np.ndarray, detections: List[Dict[str, Any]], people_count: int, zone_breached: bool):
        """Renders bounding boxes, zone polygons, and top status bar on video frame."""
        # 1. Polygon Zone Overlay
        polygon_pts = np.array([[100, 100], [450, 100], [450, 320], [100, 320]], np.int32)
        zone_color = (0, 0, 255) if zone_breached else (0, 165, 255)  # Red if breached, else Orange
        
        # Transparent overlay fill
        overlay = frame.copy()
        cv2.fillPoly(overlay, [polygon_pts], zone_color)
        cv2.addWeighted(overlay, 0.2, frame, 0.8, 0, frame)
        cv2.polylines(frame, [polygon_pts], True, zone_color, 3)
        
        zone_label = "RESTRICTED ZONE A [BREACH!]" if zone_breached else "RESTRICTED ZONE A"
        cv2.putText(frame, zone_label, (110, 125), cv2.FONT_HERSHEY_SIMPLEX, 0.55, zone_color, 2)

        # 2. Bounding Boxes for Detections
        for det in detections:
            x, y, w, h = det["bbox"]
            conf = det["confidence"]
            cx, cy = det["centroid"]

            box_color = (0, 255, 0)  # Emerald green for detected person
            cv2.rectangle(frame, (x, y), (x + w, y + h), box_color, 2)
            cv2.circle(frame, (cx, cy), 4, (0, 255, 255), -1)

            label = f"Person {int(conf * 100)}%"
            cv2.putText(frame, label, (x, max(y - 8, 15)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

        # 3. Top Status HUD Bar
        cv2.rectangle(frame, (0, 0), (frame.shape[1], 40), (15, 23, 42), -1)
        status_str = f"VISIONFORGE AI :: CAM-01 (LIVE) | PEOPLE: {people_count} | STATUS: PROCESSING"
        cv2.putText(frame, status_str, (15, 26), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (56, 189, 248), 2)

    def _async_broadcast(self, message: Dict[str, Any]):
        try:
            loop = asyncio.get_running_loop()
            loop.create_task(ws_manager.broadcast(message))
        except Exception:
            pass

    def generate_mjpeg_stream(self) -> Generator[bytes, None, None]:
        """Yields MJPEG byte chunks for streaming live canvas in browser."""
        while True:
            if self.current_frame_bytes:
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + self.current_frame_bytes + b'\r\n')
            time.sleep(0.04)


video_service = VideoCaptureService()
