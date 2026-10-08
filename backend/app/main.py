from contextlib import asynccontextmanager
from typing import AsyncGenerator
from fastapi import FastAPI, Request, status, WebSocket, WebSocketDisconnect
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from backend.app.core.config import settings
from backend.app.core.logging import logger
from backend.app.core.websocket_manager import ws_manager
from backend.app.api.v1.router import api_v1_router
from backend.app.api.v1.endpoints.health import get_health
from backend.app.api.v1.endpoints.cameras import list_cameras, create_camera
from backend.app.api.v1.endpoints.events import get_events, get_event_by_id
from backend.app.api.v1.endpoints.alerts import get_alerts, acknowledge_alert, resolve_alert
from backend.app.api.v1.endpoints.video import start_video_analysis, stop_video_analysis, get_video_status, stream_video_feed
from backend.app.api.v1.endpoints.settings import get_system_settings, update_system_settings
from backend.app.api.v1.endpoints.analytics import get_analytics_summary


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan manager handling startup and shutdown events."""
    logger.info(f"Starting {settings.PROJECT_NAME} (v{settings.VERSION})")
    logger.info(f"Environment: {settings.ENVIRONMENT} | Log Level: {settings.LOG_LEVEL}")
    yield
    logger.info(f"Shutting down {settings.PROJECT_NAME}")


def create_application() -> FastAPI:
    """Factory function for creating and configuring the FastAPI instance."""
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        description="AI Based Intelligent Video Analytics Platform API",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        lifespan=lifespan,
    )

    # Configure CORS Middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Exception Handlers
    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException) -> JSONResponse:
        logger.warning(f"HTTPException {exc.status_code} on {request.url.path}: {exc.detail}")
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": True,
                "code": exc.status_code,
                "message": str(exc.detail),
            },
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
        logger.warning(f"Validation error on {request.url.path}: {exc.errors()}")
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "error": True,
                "code": status.HTTP_422_UNPROCESSABLE_ENTITY,
                "message": "Invalid request payload or parameters",
                "details": exc.errors(),
            },
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        logger.error(f"Unhandled exception on {request.url.path}: {exc}", exc_info=True)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": True,
                "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "message": "An internal server error occurred",
            },
        )

    # Include Versioned API Routes
    app.include_router(api_v1_router, prefix=settings.API_V1_PREFIX)

    # Top-Level Root Endpoint Aliases for Review 1 API contract compatibility
    app.add_api_route("/api/health", get_health, methods=["GET"], include_in_schema=False)
    app.add_api_route("/health", get_health, methods=["GET"], include_in_schema=False)
    
    app.add_api_route("/api/cameras", list_cameras, methods=["GET"], include_in_schema=False)
    app.add_api_route("/api/cameras", create_camera, methods=["POST"], include_in_schema=False)
    app.add_api_route("/api/events", get_events, methods=["GET"], include_in_schema=False)
    app.add_api_route("/api/events/{id}", get_event_by_id, methods=["GET"], include_in_schema=False)
    app.add_api_route("/api/alerts", get_alerts, methods=["GET"], include_in_schema=False)
    app.add_api_route("/api/alerts/{id}/acknowledge", acknowledge_alert, methods=["POST"], include_in_schema=False)
    app.add_api_route("/api/alerts/{id}/resolve", resolve_alert, methods=["POST"], include_in_schema=False)
    
    app.add_api_route("/api/video/start", start_video_analysis, methods=["POST"], include_in_schema=False)
    app.add_api_route("/api/video/stop", stop_video_analysis, methods=["POST"], include_in_schema=False)
    app.add_api_route("/api/video/status", get_video_status, methods=["GET"], include_in_schema=False)
    app.add_api_route("/api/video/stream", stream_video_feed, methods=["GET"], include_in_schema=False)
    
    app.add_api_route("/api/settings", get_system_settings, methods=["GET"], include_in_schema=False)
    app.add_api_route("/api/settings", update_system_settings, methods=["PUT"], include_in_schema=False)
    app.add_api_route("/api/analytics", get_analytics_summary, methods=["GET"], include_in_schema=False)

    # WebSocket Real-Time Endpoint
    @app.websocket("/ws/events")
    async def websocket_events_endpoint(websocket: WebSocket):
        await ws_manager.connect(websocket)
        try:
            while True:
                # Keepalive loop listening for client messages
                data = await websocket.receive_text()
        except WebSocketDisconnect:
            ws_manager.disconnect(websocket)
        except Exception as e:
            logger.warning(f"WebSocket connection error: {e}")
            ws_manager.disconnect(websocket)

    return app


app = create_application()
