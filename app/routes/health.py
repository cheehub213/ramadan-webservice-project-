from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db

router = APIRouter(prefix="/api/v1/health", tags=["health"])

@router.get("")
async def health_check(db: Session = Depends(get_db)):
    """Check API health and database connection"""
    try:
        # Try a simple query to test DB connection
        db.execute("SELECT 1")
        return {
            "status": "healthy",
            "database": "connected"
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e)
        }
