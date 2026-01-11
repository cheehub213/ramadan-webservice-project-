"""
Routes Package - Modular API Routes for Ramadan Helper
"""
from fastapi import APIRouter
from .auth import router as auth_router
from .dua import router as dua_router
from .chat import router as chat_router
from .analyzer import router as analyzer_router
from .events import router as events_router
from .videos import router as videos_router

# Main API router
api_router = APIRouter(prefix="/api")

# Include all sub-routers
api_router.include_router(auth_router, prefix="/auth", tags=["Authentication"])
api_router.include_router(dua_router, prefix="/dua", tags=["Dua Generator"])
api_router.include_router(chat_router, prefix="/chat", tags=["Chat with Imam"])
api_router.include_router(analyzer_router, prefix="/analyzer", tags=["AI Analyzer"])
api_router.include_router(events_router, prefix="/events", tags=["Events"])
api_router.include_router(videos_router, prefix="/videos", tags=["Islamic Videos"])

__all__ = ["api_router"]
