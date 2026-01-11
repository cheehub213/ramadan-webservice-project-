"""
Dua Generator Schemas
"""
from pydantic import BaseModel
from typing import Optional


class DuaGenerateRequest(BaseModel):
    """Request to generate a dua"""
    category: str
    context: str
    email: Optional[str] = None


class DuaHistoryResponse(BaseModel):
    """Dua history item response"""
    id: int
    email: str
    category: str
    context: str
    dua_text_en: str
    dua_text_ar: str
    helpful: Optional[bool]
    created_at: str
    
    class Config:
        from_attributes = True


class DuaFeedbackRequest(BaseModel):
    """Feedback on a dua"""
    dua_id: int
    helpful: bool
    notes: Optional[str] = None
