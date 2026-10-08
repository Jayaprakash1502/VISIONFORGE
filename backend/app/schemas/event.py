from datetime import datetime
from typing import Any, Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field
from backend.app.models.event import EventType, EventStatus
from backend.app.models.zone import SeverityLevel


class EventBase(BaseModel):
    event_type: EventType = Field(..., description="Category of event triggered")
    location: Optional[str] = Field(None, max_length=200, description="Location description")
    timestamp: datetime = Field(..., description="Timestamp when event occurred")
    severity: SeverityLevel = Field(SeverityLevel.MEDIUM, description="Event severity rating")
    description: Optional[str] = Field(None, max_length=500, description="Human-readable description")
    detection_data: Optional[Any] = Field(None, description="Detailed detection snapshot or count data")
    status: EventStatus = Field(EventStatus.NEW, description="Event lifecycle status")
    snapshot_path: Optional[str] = Field(None, max_length=500, description="Path to captured snapshot image")


class EventCreate(EventBase):
    camera_id: UUID = Field(..., description="Camera source UUID")
    zone_id: Optional[UUID] = Field(None, description="Associated zone UUID if applicable")


class EventUpdate(BaseModel):
    status: Optional[EventStatus] = None
    severity: Optional[SeverityLevel] = None
    description: Optional[str] = Field(None, max_length=500)


class EventResponse(EventBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    camera_id: UUID
    zone_id: Optional[UUID] = None
    created_at: datetime
