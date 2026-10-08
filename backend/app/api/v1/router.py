from fastapi import APIRouter
from backend.app.api.v1.endpoints import health, cameras, events, alerts, video, settings, analytics

api_v1_router = APIRouter()

api_v1_router.include_router(health.router, tags=["Health & Diagnostics"])
api_v1_router.include_router(cameras.router, tags=["Camera Management"])
api_v1_router.include_router(events.router, tags=["Event Management"])
api_v1_router.include_router(alerts.router, tags=["Alert Management"])
api_v1_router.include_router(video.router, tags=["Video Processing & Streaming"])
api_v1_router.include_router(settings.router, tags=["System Settings"])
api_v1_router.include_router(analytics.router, tags=["Security Analytics"])
