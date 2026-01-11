"""
Dua Generator Routes
"""
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime

from database import SessionLocal
from models_extended import DuaHistory
from schemas.dua import DuaGenerateRequest, DuaHistoryResponse
from services_dua import DuaService

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/categories")
async def get_categories():
    """Get all available dua categories"""
    return {"categories": DuaService.get_categories()}


@router.post("/generate")
async def generate_dua(request: DuaGenerateRequest, db: Session = Depends(get_db)):
    """Generate a personalized dua (public - no auth required)"""
    try:
        result = await DuaService.generate_dua(request.category, request.context)
        
        # Save to history if email provided
        if request.email:
            history = DuaHistory(
                email=request.email,
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
async def get_dua_history(email: str, db: Session = Depends(get_db)):
    """Get dua history for a user"""
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
async def submit_feedback(dua_id: int, helpful: bool, db: Session = Depends(get_db)):
    """Submit feedback on a dua"""
    dua = db.query(DuaHistory).filter(DuaHistory.id == dua_id).first()
    if not dua:
        raise HTTPException(status_code=404, detail="Dua not found")
    
    dua.helpful = helpful
    db.commit()
    return {"message": "Feedback recorded", "helpful": helpful}
