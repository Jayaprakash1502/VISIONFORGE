from typing import Dict, Any
from fastapi import APIRouter
from backend.app.core.store import store

router = APIRouter()


@router.get("/settings")
def get_system_settings() -> Dict[str, Any]:
    """Retrieve system configuration thresholds and engine status."""
    return store.settings


@router.put("/settings")
def update_system_settings(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Update dynamic system configuration thresholds."""
    return store.update_settings(payload)
