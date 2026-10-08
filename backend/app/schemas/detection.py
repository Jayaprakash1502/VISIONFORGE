from datetime import datetime
from typing import Any, Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field


class DetectionBase(BaseModel):
    object_class: str = Field("person", description="Detected object class name")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Detection confidence score")
    bbox_x: float = Field(..., description="Bounding box top-left X coordinate")
    bbox_y: float = Field(..., description="Bounding box top-left Y coordinate")
    bbox_width: float = Field(..., ge=0.0, description="Bounding box width")
    bbox_height: float = Field(..., ge=0.0, description="Bounding box height")
    tracking_id: Optional[int] = Field(None, description="Persistent tracking ID")
    frame_timestamp: datetime = Field(..., description="Timestamp of the processed video frame")
    detection_metadata: Optional[Any] = Field(None, description="Optional extra detection details")


class DetectionCreate(DetectionBase):
    camera_id: UUID = Field(..., description="Associated camera UUID")
    event_id: Optional[UUID] = Field(None, description="Associated event UUID if linked")


class DetectionResponse(DetectionBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    camera_id: UUID
    event_id: Optional[UUID] = None
    created_at: datetime
