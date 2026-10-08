import uuid
from datetime import datetime
from typing import Any, Optional
from sqlalchemy import String, Float, Integer, DateTime, ForeignKey, CheckConstraint, Index
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.types import JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.models.base import Base, TimestampMixin


class Detection(Base, TimestampMixin):
    """Detection model storing frame-level AI object detection results."""

    __tablename__ = "detections"
    __table_args__ = (
        Index("idx_detections_camera_id", "camera_id"),
        Index("idx_detections_frame_timestamp", "frame_timestamp"),
        Index("idx_detections_object_class", "object_class"),
        CheckConstraint("confidence >= 0.0 AND confidence <= 1.0", name="ck_detections_confidence_range"),
        CheckConstraint("bbox_width >= 0.0 AND bbox_height >= 0.0", name="ck_detections_bbox_positive"),
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
    event_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("events.id", ondelete="SET NULL"),
        nullable=True,
    )
    object_class: Mapped[str] = mapped_column(String(50), default="person", nullable=False)
    confidence: Mapped[float] = mapped_column(Float, nullable=False)
    
    bbox_x: Mapped[float] = mapped_column(Float, nullable=False)
    bbox_y: Mapped[float] = mapped_column(Float, nullable=False)
    bbox_width: Mapped[float] = mapped_column(Float, nullable=False)
    bbox_height: Mapped[float] = mapped_column(Float, nullable=False)
    
    tracking_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    frame_timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    detection_metadata: Mapped[Optional[Any]] = mapped_column(
        "metadata",
        JSON().with_variant(JSONB, "postgresql"),
        nullable=True,
    )

    # Relationships
    camera: Mapped["Camera"] = relationship("Camera", back_populates="detections")
    event: Mapped[Optional["Event"]] = relationship("Event", back_populates="detections")
