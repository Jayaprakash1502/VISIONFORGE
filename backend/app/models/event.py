import uuid
from datetime import datetime
from typing import Any, List, Optional
from enum import Enum as PyEnum
from sqlalchemy import String, DateTime, ForeignKey, Enum as SQLEnum, Index
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.types import JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.models.base import Base, TimestampMixin
from backend.app.models.zone import SeverityLevel


class EventType(str, PyEnum):
    PERSON_DETECTED = "PERSON_DETECTED"
    CROWD_DETECTED = "CROWD_DETECTED"
    RESTRICTED_AREA_ENTRY = "RESTRICTED_AREA_ENTRY"
    LOITERING = "LOITERING"
    UNUSUAL_ACTIVITY = "UNUSUAL_ACTIVITY"
    CAMERA_OFFLINE = "CAMERA_OFFLINE"
    CAMERA_RECOVERED = "CAMERA_RECOVERED"
    SYSTEM_ERROR = "SYSTEM_ERROR"


class EventStatus(str, PyEnum):
    NEW = "NEW"
    ACKNOWLEDGED = "ACKNOWLEDGED"
    RESOLVED = "RESOLVED"


class Event(Base, TimestampMixin):
    """Central event model representing security triggers and operational states."""

    __tablename__ = "events"
    __table_args__ = (
        Index("idx_events_timestamp", "timestamp"),
        Index("idx_events_camera_id", "camera_id"),
        Index("idx_events_event_type", "event_type"),
        Index("idx_events_severity", "severity"),
        Index("idx_events_status", "status"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    event_type: Mapped[EventType] = mapped_column(
        SQLEnum(EventType, name="event_type_enum"),
        nullable=False,
    )
    camera_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("cameras.id", ondelete="CASCADE"),
        nullable=False,
    )
    zone_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("zones.id", ondelete="SET NULL"),
        nullable=True,
    )
    location: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    
    severity: Mapped[SeverityLevel] = mapped_column(
        SQLEnum(SeverityLevel, name="severity_level_enum"),
        default=SeverityLevel.MEDIUM,
        nullable=False,
    )
    description: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    detection_data: Mapped[Optional[Any]] = mapped_column(
        JSON().with_variant(JSONB, "postgresql"),
        nullable=True,
    )
    status: Mapped[EventStatus] = mapped_column(
        SQLEnum(EventStatus, name="event_status_enum"),
        default=EventStatus.NEW,
        nullable=False,
    )
    snapshot_path: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    # Relationships
    camera: Mapped["Camera"] = relationship("Camera", back_populates="events")
    zone: Mapped[Optional["Zone"]] = relationship("Zone", back_populates="events")
    alerts: Mapped[List["Alert"]] = relationship(
        "Alert", back_populates="event", cascade="all, delete-orphan"
    )
    detections: Mapped[List["Detection"]] = relationship("Detection", back_populates="event")
