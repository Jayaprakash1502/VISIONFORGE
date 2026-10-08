from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field
from backend.app.models.zone import SeverityLevel
from backend.app.models.event import EventStatus


class AlertBase(BaseModel):
    severity: SeverityLevel = Field(..., description="Alert severity level")
    title: str = Field(..., min_length=1, max_length=150, description="Short alert title")
    message: str = Field(..., min_length=1, max_length=500, description="Detailed alert description")
    status: EventStatus = Field(EventStatus.NEW, description="Alert state")


class AlertCreate(AlertBase):
    event_id: UUID = Field(..., description="UUID of triggering event")


class AlertUpdate(BaseModel):
    status: Optional[EventStatus] = Field(None, description="New alert lifecycle state")


class AlertResponse(AlertBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    event_id: UUID
    created_at: datetime
    acknowledged_at: Optional[datetime] = None
    resolved_at: Optional[datetime] = None
