from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app.routes import search, health, imam, chat, dua
from app.config import settings

# Create tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="Ramadan Decision Assistant API",
    description="Help people find answers to their problems during Ramadan using Quran, Hadiths, and Real Imams",
    version="2.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router)
app.include_router(search.router)
app.include_router(imam.router)
app.include_router(chat.router)
app.include_router(dua.router)

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": "Ramadan Decision Assistant API",
        "version": "1.0.0",
        "documentation": "/docs",
        "endpoints": {
            "health": "/api/v1/health",
            "find_answer": "/api/v1/search/answer",
            "search_quran": "/api/v1/search/quran",
            "search_hadith": "/api/v1/search/hadith"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.debug
    )
