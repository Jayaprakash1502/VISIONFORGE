import uuid
from typing import List, Optional
from enum import Enum as PyEnum
from sqlalchemy import String, Boolean, Enum as SQLEnum, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.models.base import Base, TimestampMixin


class CameraSourceType(str, PyEnum):
    LOCAL_VIDEO = "LOCAL_VIDEO"
    UPLOAD = "UPLOAD"
    WEBCAM = "WEBCAM"
    RTSP = "RTSP"


class CameraStatus(str, PyEnum):
    ONLINE = "ONLINE"
    OFFLINE = "OFFLINE"
    CONNECTING = "CONNECTING"
    ERROR = "ERROR"
    DISABLED = "DISABLED"


class Camera(Base, TimestampMixin):
    """Camera model storing surveillance video sources and state."""

    __tablename__ = "cameras"
    __table_args__ = (
        CheckConstraint("length(name) > 0", name="ck_cameras_name_not_empty"),
        CheckConstraint("length(source_url) > 0", name="ck_cameras_source_url_not_empty"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    location: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    description: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    
    source_type: Mapped[CameraSourceType] = mapped_column(
        SQLEnum(CameraSourceType, name="camera_source_type_enum"),
        default=CameraSourceType.LOCAL_VIDEO,
        nullable=False,
    )
    source_url: Mapped[str] = mapped_column(String(500), nullable=False)
    
    status: Mapped[CameraStatus] = mapped_column(
        SQLEnum(CameraStatus, name="camera_status_enum"),
        default=CameraStatus.OFFLINE,
        nullable=False,
    )
    enabled: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Relationships
    zones: Mapped[List["Zone"]] = relationship(
        "Zone", back_populates="camera", cascade="all, delete-orphan"
    )
    detections: Mapped[List["Detection"]] = relationship(
        "Detection", back_populates="camera", cascade="all, delete-orphan"
    )
    events: Mapped[List["Event"]] = relationship(
        "Event", back_populates="camera", cascade="all, delete-orphan"
    )
