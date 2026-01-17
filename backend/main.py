"""
myRamadan - FastAPI Backend with JWT Authentication
Comprehensive REST API for all services including Events (Tunisia)
"""
from dotenv import load_dotenv
load_dotenv()  # Load .env file before other imports

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import Base, engine
from models_extended import *  # Import all models
from routes import api_router  # New modular routes
import json

# Create all database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="🌙 myRamadan API",
    description="""
## Complete REST API for myRamadan Application

### 🔐 Authentication
This API uses **JWT (JSON Web Tokens)** for authentication.
- Use `/api/auth/login` to get your access token
- Include the token in the `Authorization: Bearer <token>` header
- 🔒 endpoints require authentication

### 🎪 Events Feature (Tunisia)
Post and discover Ramadan events across 24 Tunisian cities!
- **Basic Listing**: 20 TND
- **Featured Listing**: 50 TND (highlighted, priority display)

### Features
| Feature | Description |
|---------|-------------|
| 📿 Dua Generator | Bilingual (Arabic/English) personalized duas |
| 🤖 AI Analyzer | Quran verses & Hadith with AI explanations |
| 💬 Chat with Imam | Real-time chat with Islamic scholars |
| 📺 Videos | AI-powered Islamic video search |
| 🎪 Events | Ramadan events in Tunisia |
    """,
    version="3.0"
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
# Modular API routes (auth, dua, chat, analyzer, events, videos)
app.include_router(api_router)

# ============= ROOT ENDPOINT =============
@app.get("/")
def read_root():
    """Root endpoint with API info"""
    return {
        "name": "🌙 myRamadan API",
        "version": "3.0",
        "description": "Complete REST API with JWT Authentication for Islamic guidance and resources",
        "docs": "http://localhost:8000/docs",
        "authentication": "JWT Bearer Token",
        "services": {
            "auth": "/api/auth (login, signup, token)",
            "users": "/api/users",
            "dua": "/api/dua",
            "chat": "/api/chat",
            "analyzer": "/api/analyzer",
            "videos": "/api/videos",
            "events": "/api/events (Tunisia - 24 cities)",
            "health": "/api/health"
        },
        "events_pricing": {
            "basic": "20 TND",
            "featured": "50 TND"
        }
    }


@app.get("/api/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "myRamadan API",
        "version": "3.0"
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
    
    print("✅ myRamadan Backend started successfully!")
    print("📚 Services available:")
    print("   - 🔐 JWT Authentication")
    print("   - 👤 Users Management")
    print("   - 📿 Dua Generation & History")
    print("   - 💬 Chat with Imams")
    print("   - 📺 Islamic Videos")
    print("   - 🤖 AI Analyzer")
    print("   - 🎪 Events (Tunisia - 24 cities)")
    print("🔗 API Docs: http://localhost:8000/docs")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
