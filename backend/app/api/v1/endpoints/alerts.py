import uuid
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query, status
from backend.app.schemas.alert import AlertResponse
from backend.app.core.store import store

router = APIRouter()


@router.get("/alerts", response_model=List[AlertResponse])
def get_alerts(
    status: Optional[str] = Query(None, description="Filter by status (NEW, ACKNOWLEDGED, RESOLVED)"),
    severity: Optional[str] = Query(None, description="Filter by severity"),
):
    """Retrieve active or filtered alerts."""
    return store.get_alerts(status_filter=status, severity=severity)


@router.post("/alerts/{id}/acknowledge", response_model=AlertResponse)
def acknowledge_alert(id: uuid.UUID):
    """Acknowledge an active alert."""
    alert = store.acknowledge_alert(id)
    if not alert:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Alert not found")
    return alert


@router.post("/alerts/{id}/resolve", response_model=AlertResponse)
def resolve_alert(id: uuid.UUID):
    """Resolve an active alert."""
    alert = store.resolve_alert(id)
    if not alert:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Alert not found")
    return alert
