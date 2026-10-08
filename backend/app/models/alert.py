import uuid
from datetime import datetime
from typing import Optional
from sqlalchemy import String, DateTime, ForeignKey, Enum as SQLEnum, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.models.base import Base, TimestampMixin
from backend.app.models.zone import SeverityLevel
from backend.app.models.event import EventStatus


class Alert(Base, TimestampMixin):
    """Alert model representing actionable operator dashboard notifications."""

    __tablename__ = "alerts"
    __table_args__ = (
        Index("idx_alerts_event_id", "event_id"),
        Index("idx_alerts_status", "status"),
        Index("idx_alerts_created_at", "created_at"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    event_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("events.id", ondelete="CASCADE"),
        nullable=False,
    )
    severity: Mapped[SeverityLevel] = mapped_column(
        SQLEnum(SeverityLevel, name="severity_level_enum"),
        nullable=False,
    )
    title: Mapped[str] = mapped_column(String(150), nullable=False)
    message: Mapped[str] = mapped_column(String(500), nullable=False)
    
    status: Mapped[EventStatus] = mapped_column(
        SQLEnum(EventStatus, name="event_status_enum"),
        default=EventStatus.NEW,
        nullable=False,
    )
    
    acknowledged_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    resolved_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    # Relationships
    event: Mapped["Event"] = relationship("Event", back_populates="alerts")
