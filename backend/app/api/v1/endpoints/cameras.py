import uuid
from typing import List
from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException, status
from backend.app.schemas.camera import CameraResponse, CameraCreate, CameraStatus
from backend.app.core.store import store

router = APIRouter()


@router.get("/cameras", response_model=List[CameraResponse])
def list_cameras():
    """List registered camera sources."""
    return list(store.cameras.values())


@router.get("/cameras/{id}", response_model=CameraResponse)
def get_camera_by_id(id: uuid.UUID):
    """Retrieve camera source details by ID."""
    if id in store.cameras:
        return store.cameras[id]
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Camera not found")


@router.post("/cameras", response_model=CameraResponse, status_code=status.HTTP_201_CREATED)
def create_camera(payload: CameraCreate):
    """Register a new camera surveillance stream."""
    now = datetime.now(timezone.utc)
    new_cam = CameraResponse(
        id=uuid.uuid4(),
        name=payload.name,
        location=payload.location or "Unspecified",
        description=payload.description or "Registered surveillance stream",
        source_type=payload.source_type,
        source_url=payload.source_url,
        status=CameraStatus.ONLINE,
        enabled=payload.enabled,
        created_at=now,
        updated_at=now,
    )
    store.add_camera(new_cam)
    return new_cam
