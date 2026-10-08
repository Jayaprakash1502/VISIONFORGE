import uuid
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query, status
from backend.app.schemas.event import EventResponse
from backend.app.core.store import store

router = APIRouter()


@router.get("/events", response_model=List[EventResponse])
def get_events(
    event_type: Optional[str] = Query(None, description="Filter by event type"),
    severity: Optional[str] = Query(None, description="Filter by severity"),
    status: Optional[str] = Query(None, description="Filter by status"),
    search: Optional[str] = Query(None, description="Search description"),
    limit: int = Query(100, ge=1, le=500),
):
    """Retrieve security events history with optional filters."""
    return store.get_events(
        event_type=event_type,
        severity=severity,
        status_filter=status,
        search=search,
        limit=limit,
    )


@router.get("/events/{id}", response_model=EventResponse)
def get_event_by_id(id: uuid.UUID):
    """Retrieve event details by ID."""
    events = store.get_events(limit=500)
    for e in events:
        if e.id == id:
            return e
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")
