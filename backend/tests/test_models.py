import uuid
from datetime import datetime, timezone
from sqlalchemy import create_engine
from backend.app.models import (
    Base,
    Camera,
    CameraSourceType,
    CameraStatus,
    Zone,
    ZoneType,
    SeverityLevel,
    Detection,
    Event,
    EventType,
    EventStatus,
    Alert,
    SystemSetting,
)


def test_models_metadata_tables():
    """Verify all Version 1 domain tables exist in Base.metadata."""
    table_names = set(Base.metadata.tables.keys())
    expected_tables = {"cameras", "zones", "detections", "events", "alerts", "system_settings"}
    assert expected_tables.issubset(table_names), f"Missing tables: {expected_tables - table_names}"


def test_sqlite_in_memory_schema_creation():
    """Verify SQLAlchemy metadata creates cleanly in an in-memory SQLite engine."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    created_tables = set(engine.dialect.get_table_names(engine.connect()))
    assert {"cameras", "zones", "detections", "events", "alerts", "system_settings"}.issubset(created_tables)


def test_model_instantiation_and_relationships():
    """Test instantiating domain models in memory and verifying relationships."""
    camera = Camera(
        id=uuid.uuid4(),
        name="Main Gate Camera",
        location="Gate 1",
        source_type=CameraSourceType.RTSP,
        source_url="rtsp://192.168.1.100/stream1",
        status=CameraStatus.ONLINE,
        enabled=True,
    )
    assert camera.name == "Main Gate Camera"
    assert camera.source_type == CameraSourceType.RTSP
    assert camera.status == CameraStatus.ONLINE

    zone = Zone(
        id=uuid.uuid4(),
        camera_id=camera.id,
        name="Restricted Foyer",
        zone_type=ZoneType.RESTRICTED,
        polygon_coordinates=[{"x": 10, "y": 10}, {"x": 100, "y": 10}, {"x": 50, "y": 100}],
        severity=SeverityLevel.HIGH,
        cooldown_seconds=15,
    )
    assert zone.camera_id == camera.id
    assert zone.severity == SeverityLevel.HIGH

    now = datetime.now(timezone.utc)
    event = Event(
        id=uuid.uuid4(),
        event_type=EventType.RESTRICTED_AREA_ENTRY,
        camera_id=camera.id,
        zone_id=zone.id,
        timestamp=now,
        severity=SeverityLevel.HIGH,
        description="Person breached Restricted Foyer",
        status=EventStatus.NEW,
    )
    assert event.event_type == EventType.RESTRICTED_AREA_ENTRY

    alert = Alert(
        id=uuid.uuid4(),
        event_id=event.id,
        severity=SeverityLevel.HIGH,
        title="RESTRICTED AREA BREACH",
        message="Person detected in Restricted Foyer at Gate 1",
        status=EventStatus.NEW,
    )
    assert alert.event_id == event.id
