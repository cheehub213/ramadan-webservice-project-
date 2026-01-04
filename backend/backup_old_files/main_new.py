"""
Ramadan Helper - FastAPI Backend
Comprehensive REST API for all services
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import Base, engine
from models_extended import *  # Import all models
from routes_comprehensive import router as api_router
import json

# Create all database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="Ramadan Helper API",
    description="Complete REST API for Ramadan Helper Application",
    version="2.0"
)

# ============= CORS MIDDLEWARE =============
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============= INCLUDE ROUTES =============
app.include_router(api_router)

# ============= ROOT ENDPOINT =============
@app.get("/")
def read_root():
    """Root endpoint with API info"""
    return {
        "name": "Ramadan Helper API",
        "version": "2.0",
        "description": "Complete REST API for Islamic guidance and resources",
        "docs": "http://localhost:8000/docs",
        "services": {
            "users": "/api/users",
            "dua": "/api/dua",
            "chat": "/api/chat",
            "imams": "/api/imams",
            "analyzer": "/api/analyzer",
            "videos": "/api/videos",
            "history": "/api/history"
        }
    }

# ============= STARTUP =============
@app.on_event("startup")
async def startup():
    """Initialize imams in database on startup"""
    from database import SessionLocal
    from services_chat import ChatService
    
    db = SessionLocal()
    imams = db.query(Imam).all()
    if len(imams) == 0:
        for imam_data in ChatService.DEFAULT_IMAMS:
            imam = Imam(**imam_data)
            db.add(imam)
        db.commit()
    db.close()
    
    print("✅ Ramadan Helper Backend started successfully!")
    print("📚 Services available:")
    print("   - Users Management")
    print("   - Dua Generation & History")
    print("   - Chat with Imams")
    print("   - Islamic Videos")
    print("   - AI Analyzer")
    print("   - User History Tracking")
    print("🔗 API Docs: http://localhost:8000/docs")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
