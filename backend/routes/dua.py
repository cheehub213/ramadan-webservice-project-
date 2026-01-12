"""
Dua Generator Routes - Protected endpoints requiring authentication
"""
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime

from database import SessionLocal
from models_extended import DuaHistory, User
from schemas.dua import DuaGenerateRequest, DuaHistoryResponse
from services_dua import DuaService
from .auth import get_current_user, get_current_user_optional

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/categories")
async def get_categories():
    """Get all available dua categories (public)"""
    return {"categories": DuaService.get_categories()}


@router.post("/generate")
async def generate_dua(
    request: DuaGenerateRequest, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Generate a personalized dua (requires authentication)"""
    try:
        result = await DuaService.generate_dua(request.category, request.context)
        
        # Save to history using authenticated user's email
        user_email = request.email or current_user.email
        history = DuaHistory(
            email=user_email,
            category=request.category,
            context=request.context,
            dua_text_en=result.get("dua_text_en", ""),
            dua_text_ar=result.get("dua_text_ar", ""),
            how_to_use_en=result.get("how_to_use_en", ""),
            how_to_use_ar=result.get("how_to_use_ar", "")
        )
        db.add(history)
        db.commit()
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/history/{email}")
async def get_dua_history(
    email: str, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get dua history for a user (requires authentication, users can only access their own history)"""
    # Users can only access their own history, admins can access any
    if current_user.user_type != "admin" and current_user.email != email:
        raise HTTPException(status_code=403, detail="Access denied. You can only view your own history.")
    
    history = db.query(DuaHistory).filter(
        DuaHistory.email == email
    ).order_by(DuaHistory.created_at.desc()).limit(50).all()
    
    return {
        "history": [
            {
                "id": h.id,
                "category": h.category,
                "context": h.context,
                "dua_text_en": h.dua_text_en,
                "dua_text_ar": h.dua_text_ar,
                "created_at": str(h.created_at)
            }
            for h in history
        ]
    }


@router.post("/feedback/{dua_id}")
async def submit_feedback(
    dua_id: int, 
    helpful: bool, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Submit feedback on a dua (requires authentication)"""
    dua = db.query(DuaHistory).filter(DuaHistory.id == dua_id).first()
    if not dua:
        raise HTTPException(status_code=404, detail="Dua not found")
    
    dua.helpful = helpful
    db.commit()
    return {"message": "Feedback recorded", "helpful": helpful}
