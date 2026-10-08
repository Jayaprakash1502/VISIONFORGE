from typing import Dict, Any
from fastapi import APIRouter
from backend.app.core.store import store

router = APIRouter()


@router.get("/analytics")
def get_analytics_summary() -> Dict[str, Any]:
    """Retrieve security analytics, event breakdowns, and trend metrics."""
    return store.get_analytics()
