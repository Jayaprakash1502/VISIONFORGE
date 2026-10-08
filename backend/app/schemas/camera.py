from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field
from backend.app.models.camera import CameraSourceType, CameraStatus


class CameraBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Name of the camera source")
    location: Optional[str] = Field(None, max_length=200, description="Physical location or channel")
    description: Optional[str] = Field(None, max_length=500, description="Optional description")
    source_type: CameraSourceType = Field(CameraSourceType.LOCAL_VIDEO, description="Type of video stream")
    source_url: str = Field(..., min_length=1, max_length=500, description="File path or RTSP URL")
    enabled: bool = Field(True, description="Whether camera monitoring is enabled")


class CameraCreate(CameraBase):
    pass


class CameraUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    location: Optional[str] = Field(None, max_length=200)
    description: Optional[str] = Field(None, max_length=500)
    source_type: Optional[CameraSourceType] = None
    source_url: Optional[str] = Field(None, min_length=1, max_length=500)
    status: Optional[CameraStatus] = None
    enabled: Optional[bool] = None


class CameraResponse(CameraBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    status: CameraStatus
    created_at: datetime
    updated_at: datetime
