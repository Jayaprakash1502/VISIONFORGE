from typing import Dict, Any
from fastapi import APIRouter, status
from fastapi.responses import StreamingResponse
from backend.app.video.capture_service import video_service
from backend.app.core.store import store

router = APIRouter()


@router.post("/video/start", status_code=status.HTTP_200_OK)
def start_video_analysis():
    """Start video stream reading and YOLO AI rule analysis."""
    success = video_service.start("data/videos/demo.mp4")
    return {
        "status": "started" if success else "failed",
        "message": "AI Video processing engine initiated" if success else "Failed to open video source",
        "is_processing": store.is_processing,
    }


@router.post("/video/stop", status_code=status.HTTP_200_OK)
def stop_video_analysis():
    """Stop active video processing thread."""
    video_service.stop()
    return {
        "status": "stopped",
        "message": "AI Video processing engine stopped",
        "is_processing": store.is_processing,
    }


@router.get("/video/status")
def get_video_status() -> Dict[str, Any]:
    """Retrieve current video analysis status, people count, and active alerts summary."""
    active_alerts = len([a for a in store.alerts if a.status.value == "NEW" or a.status == "NEW"])
    total_events = len(store.events)
    
    return {
        "status": "PROCESSING" if store.is_processing else "ONLINE",
        "is_processing": store.is_processing,
        "current_people_count": store.current_people_count,
        "active_alerts_count": active_alerts,
        "total_events_today": total_events,
        "camera_name": "Camera 01 (Demo Feed)",
        "location": "Main Entrance Lobby",
    }


@router.get("/video/stream")
def stream_video_feed():
    """Stream live processed video frames with bounding box and zone overlays (MJPEG format)."""
    return StreamingResponse(
        video_service.generate_mjpeg_stream(),
        media_type="multipart/x-mixed-replace; boundary=frame",
    )
