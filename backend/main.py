"""

                         RAMADAN HELPER API v2.0                               
                    Professional Islamic Guidance Platform                     
═

A comprehensive REST API providing:
 User Authentication with Email Verification
 AI-Powered Dua Generation
 Islamic Scholar Chat System
 Quran & Hadith AI Analyzer
 Islamic Video Search

Built with FastAPI, SQLAlchemy, and AI Integration (Groq)
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from datetime import datetime
import logging

from database import Base, engine, SessionLocal
from models_extended import User, Imam, DuaHistory, Conversation, Message, Video, AIAnalysis, UserHistory
from routes_api import router as api_router
from services_chat import ChatService

# ============= LOGGING CONFIGURATION =============
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('backend.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ============= APPLICATION LIFESPAN =============
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application startup and shutdown events"""
    # Startup
    logger.info("=" * 60)
    logger.info("Starting Ramadan Helper API v2.0")
    logger.info("=" * 60)
    
    # Create database tables
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created/verified")
    
    # Initialize default imams
    db = SessionLocal()
    try:
        imam_count = db.query(Imam).count()
        if imam_count == 0:
            for imam_data in ChatService.DEFAULT_IMAMS:
                imam = Imam(**imam_data)
                db.add(imam)
            db.commit()
            logger.info(f"Initialized {len(ChatService.DEFAULT_IMAMS)} default imams")
        else:
            logger.info(f"Found {imam_count} existing imams")
    finally:
        db.close()
    
    logger.info("API Documentation: http://localhost:8000/docs")
    logger.info("Health Check: http://localhost:8000/api/health")
    logger.info("=" * 60)
    
    yield  # Application runs here
    
    # Shutdown
    logger.info("Shutting down Ramadan Helper API")

# ============= CREATE APPLICATION =============
app = FastAPI(
    title="Ramadan Helper API",
    description="""
## Islamic Guidance & Resources Platform

A comprehensive REST API providing Islamic guidance, resources, and AI-powered assistance.

### Features:
- **User Authentication**: Secure signup with email verification
- **Dua Generation**: AI-powered personalized duas based on your situation
- **Scholar Chat**: Connect with Islamic scholars for guidance
- **AI Analyzer**: Get relevant Quran verses and Hadiths for your questions
- **Video Search**: Find Islamic educational content on YouTube

### Authentication:
Most endpoints require a valid user email. Users must verify their email before accessing protected features.
    """,
    version="2.0.0",
    contact={
        "name": "Ramadan Helper Support",
        "email": "support@ramadanhelper.com"
    },
    license_info={
        "name": "MIT License"
    },
    lifespan=lifespan
)

# ============= CORS MIDDLEWARE =============
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============= GLOBAL EXCEPTION HANDLER =============
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": "An unexpected error occurred. Please try again later.",
            "timestamp": datetime.now().isoformat()
        }
    )

# ============= INCLUDE API ROUTES =============
app.include_router(api_router)

# ============= ROOT ENDPOINT =============
@app.get("/", tags=["Root"])
async def root():
    """API welcome endpoint with service information"""
    return {
        "name": "Ramadan Helper API",
        "version": "2.0.0",
        "status": "running",
        "description": "Islamic Guidance & Resources Platform",
        "documentation": "/docs",
        "services": {
            "authentication": {
                "signup": "POST /api/auth/signup",
                "login": "POST /api/auth/login",
                "verify": "POST /api/auth/verify"
            },
            "dua": {
                "generate": "POST /api/dua/generate",
                "history": "GET /api/dua/history/{email}",
                "categories": "GET /api/dua/categories"
            },
            "chat": {
                "imams": "GET /api/chat/imams",
                "conversations": "POST /api/chat/conversations",
                "messages": "POST /api/chat/messages"
            },
            "analyzer": {
                "analyze": "POST /api/analyzer/analyze",
                "topics": "GET /api/analyzer/topics"
            },
            "videos": {
                "search": "POST /api/videos/search"
            },
            "stats": {
                "dashboard": "GET /api/stats/dashboard",
                "user": "GET /api/stats/user/{email}"
            }
        },
        "timestamp": datetime.now().isoformat()
    }

# ============= RUN SERVER =============
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
