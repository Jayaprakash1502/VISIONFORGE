from typing import Dict, Any
from fastapi import APIRouter, status
from backend.app.core.config import settings
from backend.app.core.database import check_database_connection

router = APIRouter()


@router.get(
    "/health",
    status_code=status.HTTP_200_OK,
    summary="Application Health Check",
    response_description="Returns the operational status of the API and Database connectivity",
)
def get_health() -> Dict[str, Any]:
    """
    Health check endpoint verifying:
    - API process operational state
    - Valid configuration parameters
    - Database connection status (isolated check)
    """
    db_health = check_database_connection()
    overall_status = "ok" if db_health.get("status") == "connected" else "degraded"

    return {
        "status": overall_status,
        "service": "visionforge-api",
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT,
        "database": db_health,
    }
