import uuid
from typing import Any, List, Optional
from enum import Enum as PyEnum
from sqlalchemy import String, Boolean, Integer, ForeignKey, Enum as SQLEnum, CheckConstraint, Index
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.types import JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.models.base import Base, TimestampMixin


class ZoneType(str, PyEnum):
    RESTRICTED = "RESTRICTED"
    MONITORED = "MONITORED"
    CROWD_ZONE = "CROWD_ZONE"
    LOITERING_ZONE = "LOITERING_ZONE"


class SeverityLevel(str, PyEnum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class Zone(Base, TimestampMixin):
    """Zone model defining polygonal monitored regions associated with a camera."""

    __tablename__ = "zones"
    __table_args__ = (
        Index("idx_zones_camera_id", "camera_id"),
        CheckConstraint("cooldown_seconds >= 0", name="ck_zones_cooldown_positive"),
        CheckConstraint("length(name) > 0", name="ck_zones_name_not_empty"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    camera_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("cameras.id", ondelete="CASCADE"),
        nullable=False,
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    
    zone_type: Mapped[ZoneType] = mapped_column(
        SQLEnum(ZoneType, name="zone_type_enum"),
        default=ZoneType.RESTRICTED,
        nullable=False,
    )
    polygon_coordinates: Mapped[Any] = mapped_column(
        JSON().with_variant(JSONB, "postgresql"),
        nullable=False,
    )
    enabled: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    applicable_object_class: Mapped[str] = mapped_column(String(50), default="person", nullable=False)
    
    severity: Mapped[SeverityLevel] = mapped_column(
        SQLEnum(SeverityLevel, name="severity_level_enum"),
        default=SeverityLevel.HIGH,
        nullable=False,
    )
    cooldown_seconds: Mapped[int] = mapped_column(Integer, default=10, nullable=False)

    # Relationships
    camera: Mapped["Camera"] = relationship("Camera", back_populates="zones")
    events: Mapped[List["Event"]] = relationship("Event", back_populates="zone")
