import os
import cv2
import numpy as np
from typing import List, Dict, Any, Tuple
from backend.app.core.logging import logger

class YOLODetector:
    """
    Modular YOLO Object Detection Service.
    Loads YOLOv8 lightweight model for CPU inference with fallback to OpenCV person detection.
    """

    def __init__(self, model_name: str = "yolov8n.pt"):
        self.model_name = model_name
        self.model = None
        self.use_yolo = False

    def _init_model(self):
        try:
            from ultralytics import YOLO
            logger.info(f"Initializing YOLO model: {self.model_name}")
            self.model = YOLO(self.model_name)
            self.use_yolo = True
            logger.info("YOLO model loaded successfully.")
        except Exception as e:
            logger.warning(f"Ultralytics YOLO unavailable or loading error: {e}. Falling back to OpenCV Person Detector.")
            self.use_yolo = False

    def detect_persons(self, frame: np.ndarray, confidence_threshold: float = 0.40) -> List[Dict[str, Any]]:
        """
        Detects person objects in frame.
        Returns list of detection dicts:
        [{'bbox': (x1, y1, w, h), 'confidence': float, 'centroid': (cx, cy), 'class': 'person'}]
        """
        detections = []
        if frame is None or frame.size == 0:
            return detections

        h_frame, w_frame = frame.shape[:2]

        if self.use_yolo and self.model is not None:
            try:
                # Run YOLO inference
                results = self.model.predict(frame, classes=[0], conf=confidence_threshold, verbose=False)
                for r in results:
                    boxes = r.boxes
                    for box in boxes:
                        x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                        conf = float(box.conf[0].cpu().numpy())
                        
                        x1, y1 = max(0, int(x1)), max(0, int(y1))
                        x2, y2 = min(w_frame, int(x2)), min(h_frame, int(y2))
                        w, h = x2 - x1, y2 - y1
                        
                        cx, cy = int(x1 + w / 2), int(y1 + h / 2)
                        
                        detections.append({
                            "bbox": (x1, y1, w, h),
                            "confidence": round(conf, 2),
                            "centroid": (cx, cy),
                            "class": "person"
                        })
                return detections
            except Exception as e:
                logger.warning(f"YOLO inference runtime error: {e}, falling back to OpenCV detection")

        # Fallback OpenCV contour/color/human shape detector if YOLO model is downloading or offline
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        _, thresh = cv2.threshold(blur, 60, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > 1200:
                x, y, w, h = cv2.boundingRect(cnt)
                aspect_ratio = float(h) / w if w > 0 else 0
                if 1.2 < aspect_ratio < 4.0:
                    cx, cy = int(x + w / 2), int(y + h / 2)
                    detections.append({
                        "bbox": (x, y, w, h),
                        "confidence": 0.88,
                        "centroid": (cx, cy),
                        "class": "person"
                    })

        return detections
yolo_detector = YOLODetector()

