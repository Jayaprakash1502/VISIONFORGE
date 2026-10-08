from datetime import datetime
from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field, field_validator
from backend.app.models.zone import ZoneType, SeverityLevel


class PointSchema(BaseModel):
    x: float = Field(..., description="X coordinate (pixel offset or normalized)")
    y: float = Field(..., description="Y coordinate (pixel offset or normalized)")


class ZoneBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Zone identifier name")
    zone_type: ZoneType = Field(ZoneType.RESTRICTED, description="Category of zone rule")
    polygon_coordinates: List[PointSchema] = Field(..., min_length=3, description="Multi-vertex polygon")
    enabled: bool = Field(True, description="Whether zone monitoring rule is active")
    applicable_object_class: str = Field("person", description="Target object class for rule evaluation")
    severity: SeverityLevel = Field(SeverityLevel.HIGH, description="Alert severity level on breach")
    cooldown_seconds: int = Field(10, ge=0, description="Cooldown seconds before duplicate alert trigger")

    @field_validator("polygon_coordinates")
    @classmethod
    def validate_polygon_vertices(cls, v: List[PointSchema]) -> List[PointSchema]:
        if len(v) < 3:
            raise ValueError("A polygon zone requires at least 3 vertices.")
        return v


class ZoneCreate(ZoneBase):
    camera_id: UUID = Field(..., description="Parent camera UUID")


class ZoneUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    zone_type: Optional[ZoneType] = None
    polygon_coordinates: Optional[List[PointSchema]] = None
    enabled: Optional[bool] = None
    applicable_object_class: Optional[str] = None
    severity: Optional[SeverityLevel] = None
    cooldown_seconds: Optional[int] = Field(None, ge=0)


class ZoneResponse(ZoneBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    camera_id: UUID
    created_at: datetime
    updated_at: datetime
