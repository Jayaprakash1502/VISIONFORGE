from datetime import datetime
from typing import Any, Optional
from pydantic import BaseModel, ConfigDict, Field


class SystemSettingBase(BaseModel):
    key: str = Field(..., min_length=1, max_length=100, description="Setting key")
    value: Any = Field(..., description="Setting value (string, number, list, or dict)")
    description: Optional[str] = Field(None, max_length=250, description="Optional description")


class SystemSettingUpdate(BaseModel):
    value: Any = Field(..., description="New setting value")
    description: Optional[str] = Field(None, max_length=250)


class SystemSettingResponse(SystemSettingBase):
    model_config = ConfigDict(from_attributes=True)

    updated_at: datetime
