from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


# ==================== DUA GENERATOR SCHEMAS ====================

class DuaGeneratorRequest(BaseModel):
    """Request schema for dua generator"""
    problem_description: str  # User's problem/situation
    problem_category: Optional[str] = None  # family, health, work, finance, spiritual, etc.
    user_email: Optional[str] = None
    user_name: Optional[str] = None
    language: Optional[str] = "English"  # Language for response


class DuaGeneratedResponse(BaseModel):
    """Generated dua response with bilingual output"""
    id: int
    user_email: str
    user_name: str
    problem_description: str
    problem_category: Optional[str]
    language: str
    dua_text_en: str  # Personalized dua in English
    dua_text_ar: str  # Personalized dua in Arabic
    how_to_use_en: str  # Instructions on how/when to recite (English)
    how_to_use_ar: str  # Instructions on how/when to recite (Arabic)
    created_at: datetime
    
    class Config:
        from_attributes = True


class DuaGeneratorResponse(BaseModel):
    """Response schema for dua generator endpoint - DEPRECATED, use DuaGeneratedResponse"""
    id: int
    user_email: Optional[str]
    user_name: Optional[str]
    problem_description: str
    problem_category: Optional[str]
    generated_dua: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class DuaFeedbackRequest(BaseModel):
    """Feedback on generated dua"""
    dua_request_id: int
    is_helpful: str  # "yes" or "no"
    feedback: Optional[str] = None


class DuaCategoryResponse(BaseModel):
    """Response for dua category"""
    id: int
    name: str
    description: Optional[str]
    icon: Optional[str]
    example_problems: Optional[str]
    
    class Config:
        from_attributes = True


class DuaHistoryResponse(BaseModel):
    """Dua history entry (bilingual)"""
    id: int
    problem_description: str
    problem_category: Optional[str]
    generated_dua_en: str
    generated_dua_ar: str
    is_helpful: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True
