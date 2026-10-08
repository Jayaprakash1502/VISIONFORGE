import uuid
from datetime import datetime, timezone, timedelta
from typing import List, Dict, Optional, Any
from threading import Lock

from backend.app.schemas.camera import CameraResponse, CameraSourceType, CameraStatus
from backend.app.schemas.zone import ZoneResponse, ZoneType, SeverityLevel, PointSchema
from backend.app.schemas.event import EventResponse, EventType, EventStatus
from backend.app.schemas.alert import AlertResponse


class InMemoryStore:
    """Thread-safe in-memory store for cameras, zones, events, alerts, and system settings."""

    def __init__(self):
        self._lock = Lock()
        self.cameras: Dict[uuid.UUID, CameraResponse] = {}
        self.zones: Dict[uuid.UUID, ZoneResponse] = {}
        self.events: List[EventResponse] = []
        self.alerts: List[AlertResponse] = []
        self.settings: Dict[str, Any] = {
            "ai_confidence_threshold": 0.45,
            "inference_fps": 5,
            "crowd_threshold": 8,
            "loitering_threshold_seconds": 20,
            "event_cooldown_seconds": 10,
        }
        self.is_processing: bool = False
        self.current_people_count: int = 13
        self._seed_default_data()

    def _seed_default_data(self):
        """Seed default 4 demo cameras, 4 zones, 3 active alerts, and 18 events for DEMO MODE consistency."""
        now = datetime.now(timezone.utc)
        
        # 1. Seed 4 Demo Cameras
        cam_1 = CameraResponse(
            id=uuid.UUID("11111111-1111-1111-1111-111111111111"),
            name="Camera 01 — Main Entrance & Lobby",
            location="Main Entrance Lobby",
            description="High-definition surveillance feed monitoring main entrance foyer",
            source_type=CameraSourceType.LOCAL_VIDEO,
            source_url="data/videos/demo.mp4",
            status=CameraStatus.ONLINE,
            enabled=True,
            created_at=now - timedelta(hours=24),
            updated_at=now,
        )
        cam_2 = CameraResponse(
            id=uuid.UUID("22222222-2222-2222-2222-222222222222"),
            name="Camera 02 — West Gate Perimeter",
            location="West Gate Perimeter Zone B",
            description="Perimeter optical camera focused on restricted zone entry points",
            source_type=CameraSourceType.LOCAL_VIDEO,
            source_url="data/videos/demo.mp4",
            status=CameraStatus.ONLINE,
            enabled=True,
            created_at=now - timedelta(hours=24),
            updated_at=now,
        )
        cam_3 = CameraResponse(
            id=uuid.UUID("33333333-3333-3333-3333-333333333333"),
            name="Camera 03 — Parking Area",
            location="South Parking Structure Zone C",
            description="Wide-angle coverage of vehicle parking bays and pedestrian walkways",
            source_type=CameraSourceType.LOCAL_VIDEO,
            source_url="data/videos/demo.mp4",
            status=CameraStatus.ONLINE,
            enabled=True,
            created_at=now - timedelta(hours=24),
            updated_at=now,
        )
        cam_4 = CameraResponse(
            id=uuid.UUID("44444444-4444-4444-4444-444444444444"),
            name="Camera 04 — VIP Access Corridor",
            location="Executive Corridor Zone D",
            description="Restricted interior hallway leading to executive suites and server vault",
            source_type=CameraSourceType.LOCAL_VIDEO,
            source_url="data/videos/demo.mp4",
            status=CameraStatus.ONLINE,
            enabled=True,
            created_at=now - timedelta(hours=24),
            updated_at=now,
        )

        for c in [cam_1, cam_2, cam_3, cam_4]:
            self.cameras[c.id] = c

        # 2. Seed 4 Monitored Zones
        zone_1 = ZoneResponse(
            id=uuid.UUID("a1111111-1111-1111-1111-111111111111"),
            camera_id=cam_1.id,
            name="Zone A (Main Entrance Foyer)",
            zone_type=ZoneType.MONITORED,
            polygon_coordinates=[PointSchema(x=50, y=50), PointSchema(x=500, y=50), PointSchema(x=500, y=400), PointSchema(x=50, y=400)],
            enabled=True,
            applicable_object_class="person",
            severity=SeverityLevel.HIGH,
            cooldown_seconds=10,
            created_at=now - timedelta(hours=24),
            updated_at=now,
        )
        zone_2 = ZoneResponse(
            id=uuid.UUID("b2222222-2222-2222-2222-222222222222"),
            camera_id=cam_2.id,
            name="Perimeter Zone B (Secure Gate)",
            zone_type=ZoneType.RESTRICTED,
            polygon_coordinates=[PointSchema(x=100, y=100), PointSchema(x=450, y=100), PointSchema(x=450, y=320), PointSchema(x=100, y=320)],
            enabled=True,
            applicable_object_class="person",
            severity=SeverityLevel.HIGH,
            cooldown_seconds=10,
            created_at=now - timedelta(hours=24),
            updated_at=now,
        )
        for z in [zone_1, zone_2]:
            self.zones[z.id] = z

        # 3. Seed Initial 18 Events for Today
        seed_events_spec = [
            (EventType.RESTRICTED_AREA_ENTRY, SeverityLevel.HIGH, cam_2.id, "West Gate Perimeter Zone B", "Unauthorized individual detected inside restricted perimeter zone B.", EventStatus.NEW, 5),
            (EventType.CROWD_DETECTED, SeverityLevel.HIGH, cam_1.id, "Main Entrance Lobby", "Unusual gathering of 8+ individuals detected near VIP access corridor.", EventStatus.NEW, 15),
            (EventType.LOITERING, SeverityLevel.MEDIUM, cam_3.id, "South Parking Structure", "Individual observed loitering in the premises for more than 5 minutes.", EventStatus.NEW, 45),
            (EventType.RESTRICTED_AREA_ENTRY, SeverityLevel.HIGH, cam_4.id, "Executive Corridor", "Unscheduled access attempt at Vault Foyer entry door.", EventStatus.RESOLVED, 90),
            (EventType.CROWD_DETECTED, SeverityLevel.MEDIUM, cam_1.id, "Main Entrance Lobby", "Crowd accumulation threshold reached (6 people in foyer).", EventStatus.RESOLVED, 120),
            (EventType.LOITERING, SeverityLevel.MEDIUM, cam_2.id, "West Gate Perimeter", "Person standing near exterior fence line for 35 seconds.", EventStatus.RESOLVED, 150),
            (EventType.UNUSUAL_ACTIVITY, SeverityLevel.LOW, cam_3.id, "South Parking Structure", "Abnormal movement pattern detected near loading dock.", EventStatus.RESOLVED, 180),
            (EventType.RESTRICTED_AREA_ENTRY, SeverityLevel.HIGH, cam_2.id, "West Gate Perimeter", "Perimeter beam trip in Zone B north quadrant.", EventStatus.RESOLVED, 210),
            (EventType.CROWD_DETECTED, SeverityLevel.MEDIUM, cam_1.id, "Main Entrance Lobby", "Group gathering detected near security screening checkpoint.", EventStatus.RESOLVED, 240),
            (EventType.LOITERING, SeverityLevel.LOW, cam_3.id, "South Parking Structure", "Vehicle parked with hazard lights on for extended period.", EventStatus.RESOLVED, 270),
            (EventType.RESTRICTED_AREA_ENTRY, SeverityLevel.HIGH, cam_4.id, "Executive Corridor", "Person detected inside server room access corridor.", EventStatus.RESOLVED, 300),
            (EventType.CROWD_DETECTED, SeverityLevel.MEDIUM, cam_1.id, "Main Entrance Lobby", "Foyer crowd density peak recorded at 10 people.", EventStatus.RESOLVED, 330),
            (EventType.LOITERING, SeverityLevel.MEDIUM, cam_2.id, "West Gate Perimeter", "Loitering state confirmed near gate control room.", EventStatus.RESOLVED, 360),
            (EventType.UNUSUAL_ACTIVITY, SeverityLevel.LOW, cam_3.id, "South Parking Structure", "Motion detected in restricted staff parking bay.", EventStatus.RESOLVED, 390),
            (EventType.RESTRICTED_AREA_ENTRY, SeverityLevel.HIGH, cam_2.id, "West Gate Perimeter", "Polygon zone breach by unidentified individual.", EventStatus.RESOLVED, 420),
            (EventType.CROWD_DETECTED, SeverityLevel.MEDIUM, cam_1.id, "Main Entrance Lobby", "Entry lobby crowd count reached 7 persons.", EventStatus.RESOLVED, 450),
            (EventType.LOITERING, SeverityLevel.LOW, cam_3.id, "South Parking Structure", "Pedestrian loitering in vehicle lane.", EventStatus.RESOLVED, 480),
            (EventType.UNUSUAL_ACTIVITY, SeverityLevel.LOW, cam_4.id, "Executive Corridor", "After-hours motion detected near executive elevator bank.", EventStatus.RESOLVED, 510),
        ]

        seeded_events = []
        for idx, (etype, sev, cid, loc, desc, st, mins_ago) in enumerate(seed_events_spec):
            evt_id = uuid.uuid4()
            evt_time = now - timedelta(minutes=mins_ago)
            evt = EventResponse(
                id=evt_id,
                camera_id=cid,
                zone_id=zone_2.id if etype == EventType.RESTRICTED_AREA_ENTRY else zone_1.id,
                event_type=etype,
                location=loc,
                timestamp=evt_time,
                severity=sev,
                description=desc,
                detection_data={"person_count": 3 if etype == EventType.RESTRICTED_AREA_ENTRY else (8 if etype == EventType.CROWD_DETECTED else 1)},
                status=st,
                snapshot_path=None,
                created_at=evt_time,
            )
            seeded_events.append(evt)

        self.events = seeded_events

        # 4. Seed Initial 3 ACTIVE Alerts
        alert_1 = AlertResponse(
            id=uuid.uuid4(),
            event_id=self.events[0].id,
            camera_id=cam_2.id,
            title="RESTRICTED AREA ENTRY",
            message="Unauthorized individual detected inside restricted perimeter zone B.",
            severity=SeverityLevel.HIGH,
            status=EventStatus.NEW,
            created_at=now - timedelta(minutes=5),
            acknowledged_at=None,
            resolved_at=None,
        )
        alert_2 = AlertResponse(
            id=uuid.uuid4(),
            event_id=self.events[1].id,
            camera_id=cam_1.id,
            title="CROWD DETECTED",
            message="Unusual gathering of 8+ individuals detected near VIP access corridor.",
            severity=SeverityLevel.HIGH,
            status=EventStatus.NEW,
            created_at=now - timedelta(minutes=15),
            acknowledged_at=None,
            resolved_at=None,
        )
        alert_3 = AlertResponse(
            id=uuid.uuid4(),
            event_id=self.events[2].id,
            camera_id=cam_3.id,
            title="LOITERING BEHAVIOR",
            message="Individual observed loitering in the premises for more than 5 minutes.",
            severity=SeverityLevel.MEDIUM,
            status=EventStatus.NEW,
            created_at=now - timedelta(minutes=45),
            acknowledged_at=None,
            resolved_at=None,
        )

        self.alerts = [alert_1, alert_2, alert_3]

    def add_camera(self, camera: CameraResponse) -> CameraResponse:
        with self._lock:
            self.cameras[camera.id] = camera
            return camera

    def add_event(self, event: EventResponse) -> EventResponse:
        with self._lock:
            self.events.insert(0, event)
            return event

    def add_alert(self, alert: AlertResponse) -> AlertResponse:
        with self._lock:
            self.alerts.insert(0, alert)
            return alert

    def get_events(
        self,
        event_type: Optional[str] = None,
        severity: Optional[str] = None,
        status_filter: Optional[str] = None,
        search: Optional[str] = None,
        limit: int = 100,
    ) -> List[EventResponse]:
        with self._lock:
            res = list(self.events)
            if event_type:
                res = [e for e in res if e.event_type.value == event_type or e.event_type == event_type]
            if severity:
                res = [e for e in res if e.severity.value == severity or e.severity == severity]
            if status_filter:
                res = [e for e in res if e.status.value == status_filter or e.status == status_filter]
            if search:
                query = search.lower()
                res = [
                    e for e in res
                    if query in e.description.lower() or query in e.event_type.value.lower()
                ]
            return res[:limit]

    def get_alerts(
        self,
        status_filter: Optional[str] = None,
        severity: Optional[str] = None,
        limit: int = 50,
    ) -> List[AlertResponse]:
        with self._lock:
            res = list(self.alerts)
            if status_filter:
                res = [a for a in res if a.status.value == status_filter or a.status == status_filter]
            if severity:
                res = [a for a in res if a.severity.value == severity or a.severity == severity]
            return res[:limit]

    def acknowledge_alert(self, alert_id: uuid.UUID) -> Optional[AlertResponse]:
        with self._lock:
            now = datetime.now(timezone.utc)
            for alert in self.alerts:
                if alert.id == alert_id:
                    alert.status = EventStatus.ACKNOWLEDGED
                    alert.acknowledged_at = now
                    for event in self.events:
                        if event.id == alert.event_id:
                            event.status = EventStatus.ACKNOWLEDGED
                    return alert
            return None

    def resolve_alert(self, alert_id: uuid.UUID) -> Optional[AlertResponse]:
        with self._lock:
            now = datetime.now(timezone.utc)
            for alert in self.alerts:
                if alert.id == alert_id:
                    alert.status = EventStatus.RESOLVED
                    alert.resolved_at = now
                    for event in self.events:
                        if event.id == alert.event_id:
                            event.status = EventStatus.RESOLVED
                    return alert
            return None

    def update_settings(self, new_settings: Dict[str, Any]) -> Dict[str, Any]:
        with self._lock:
            self.settings.update(new_settings)
            return dict(self.settings)

    def get_analytics(self) -> Dict[str, Any]:
        with self._lock:
            events_by_type = {}
            for e in self.events:
                t_val = e.event_type.value if hasattr(e.event_type, 'value') else str(e.event_type)
                events_by_type[t_val] = events_by_type.get(t_val, 0) + 1

            type_data = [{"name": k, "count": v} for k, v in events_by_type.items()]

            trend_data = [
                {"day": "Mon", "events": 4, "people": 12},
                {"day": "Tue", "events": 8, "people": 25},
                {"day": "Wed", "events": 3, "people": 15},
                {"day": "Thu", "events": 9, "people": 30},
                {"day": "Fri", "events": 6, "people": 18},
                {"day": "Sat", "events": 11, "people": 42},
                {"day": "Sun", "events": len(self.events), "people": max(self.current_people_count, 12)},
            ]

            return {
                "total_events": len(self.events),
                "total_alerts": len(self.alerts),
                "active_alerts": len([a for a in self.alerts if a.status == EventStatus.NEW or getattr(a.status, 'value', '') == 'NEW']),
                "current_people_count": self.current_people_count,
                "type_breakdown": type_data,
                "trend_data": trend_data,
            }


store = InMemoryStore()
