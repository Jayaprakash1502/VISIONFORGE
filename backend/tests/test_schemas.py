import uuid
from datetime import datetime, timezone
import pytest
from pydantic import ValidationError

from backend.app.schemas.camera import CameraCreate, CameraResponse
from backend.app.schemas.zone import ZoneCreate, PointSchema
from backend.app.schemas.detection import DetectionCreate
from backend.app.schemas.event import EventCreate
from backend.app.schemas.alert import AlertCreate
from backend.app.schemas.setting import SystemSettingBase
from backend.app.models import CameraSourceType, CameraStatus, ZoneType, SeverityLevel, EventType, EventStatus


def test_camera_schema_validation():
    """Verify camera input validation."""
    valid_cam = CameraCreate(
        name="Camera 01",
        location="North Entrance",
        source_type=CameraSourceType.LOCAL_VIDEO,
        source_url="data/videos/demo.mp4",
        enabled=True,
    )
    assert valid_cam.name == "Camera 01"

    # Empty name should fail validation
    with pytest.raises(ValidationError):
        CameraCreate(name="", source_url="data/videos/demo.mp4")


def test_zone_polygon_vertex_validation():
    """Verify polygon coordinates enforce at least 3 vertices."""
    cam_id = uuid.uuid4()
    
    # 3 vertices -> Valid
    valid_zone = ZoneCreate(
        camera_id=cam_id,
        name="Zone A",
        polygon_coordinates=[
            PointSchema(x=10, y=10),
            PointSchema(x=100, y=10),
            PointSchema(x=50, y=100),
        ],
        severity=SeverityLevel.HIGH,
    )
    assert len(valid_zone.polygon_coordinates) == 3

    # Less than 3 vertices -> Raises ValidationError
    with pytest.raises(ValidationError):
        ZoneCreate(
            camera_id=cam_id,
            name="Invalid Zone",
            polygon_coordinates=[PointSchema(x=10, y=10), PointSchema(x=100, y=10)],
        )


def test_detection_confidence_validation():
    """Verify detection confidence bounds (0.0 to 1.0)."""
    cam_id = uuid.uuid4()
    now = datetime.now(timezone.utc)

    # Valid confidence 0.85
    det = DetectionCreate(
        camera_id=cam_id,
        object_class="person",
        confidence=0.85,
        bbox_x=100.0,
        bbox_y=150.0,
        bbox_width=50.0,
        bbox_height=120.0,
        frame_timestamp=now,
    )
    assert det.confidence == 0.85

    # Confidence > 1.0 -> Raises ValidationError
    with pytest.raises(ValidationError):
        DetectionCreate(
            camera_id=cam_id,
            confidence=1.5,
            bbox_x=10, bbox_y=10, bbox_width=10, bbox_height=10,
            frame_timestamp=now,
        )


def test_system_setting_schema():
    """Verify runtime settings key/value parsing."""
    setting = SystemSettingBase(
        key="crowd_threshold",
        value=40,
        description="Threshold triggering CROWD_DETECTED event",
    )
    assert setting.key == "crowd_threshold"
    assert setting.value == 40
