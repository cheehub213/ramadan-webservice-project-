from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from enum import Enum


class ImamSpecializationEnum(str, Enum):
    GENERAL = "general"
    FIQH = "fiqh"
    QURAN = "quran"
    HADITH = "hadith"
    FAMILY = "family"
    YOUTH = "youth"
    BUSINESS = "business"
    SPIRITUALITY = "spirituality"
    MADHAB = "madhab"


class ConsultationMethodEnum(str, Enum):
    PHONE = "phone"
    EMAIL = "email"
    IN_PERSON = "in_person"
    VIDEO = "video"
    MESSAGING = "messaging"


class ConsultationStatusEnum(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    COMPLETED = "completed"
    RESCHEDULED = "rescheduled"


# ==================== IMAM SCHEMAS ====================

class ImamBase(BaseModel):
    """Base Imam schema"""
    name: str
    title: Optional[str] = None
    specializations: str  # Comma-separated
    madhab: Optional[str] = None
    bio: Optional[str] = None
    years_experience: Optional[int] = None
    qualifications: Optional[str] = None
    email: str
    phone: Optional[str] = None
    website: Optional[str] = None
    consultation_methods: str  # Comma-separated
    consultation_fee: Optional[float] = 0.0
    currency: Optional[str] = "USD"
    is_available: Optional[bool] = True
    languages: str  # Comma-separated
    timezone: Optional[str] = None
    verified: Optional[bool] = False


class ImamCreate(ImamBase):
    """Schema for creating an Imam"""
    pass


class ImamUpdate(BaseModel):
    """Schema for updating Imam info"""
    name: Optional[str] = None
    is_available: Optional[bool] = None
    consultation_fee: Optional[float] = None
    average_rating: Optional[float] = None
    verified: Optional[bool] = None
    
    class Config:
        from_attributes = True


class ImamResponse(ImamBase):
    """Response schema for Imam"""
    id: int
    average_rating: float
    total_consultations: int
    total_reviews: int
    verified: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class ImamListResponse(BaseModel):
    """Response for list of imams"""
    id: int
    name: str
    title: Optional[str]
    specializations: str
    madhab: Optional[str]
    bio: Optional[str]
    consultation_methods: str
    consultation_fee: float
    is_available: bool
    languages: str
    average_rating: float
    total_consultations: int
    verified: bool
    
    class Config:
        from_attributes = True


# ==================== CONSULTATION SCHEMAS ====================

class ConsultationBase(BaseModel):
    """Base consultation schema"""
    title: str
    description: str
    category: Optional[str] = None
    madhab_preference: Optional[str] = None


class ConsultationRequest(ConsultationBase):
    """Request to book a consultation"""
    imam_id: int
    user_email: str  # User's email for contact
    preferred_method: str  # phone, email, video, in_person
    preferred_date: Optional[datetime] = None
    duration_minutes: Optional[int] = 30
    
    # Context from Deepseek search
    original_prompt: Optional[str] = None
    deepseek_response: Optional[str] = None
    reason_for_consultation: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "imam_id": 1,
                "title": "Marriage and Family Issues",
                "description": "I'm struggling with family relationships and seeking Islamic guidance...",
                "category": "family",
                "user_email": "user@example.com",
                "preferred_method": "phone",
                "reason_for_consultation": "The AI response didn't address my specific madhab perspective",
                "original_prompt": "I have family conflicts...",
                "deepseek_response": "Based on Islamic teachings...",
            }
        }


class ConsultationResponse(BaseModel):
    """Response schema for consultation"""
    id: int
    imam_id: int
    title: str
    description: str
    category: Optional[str]
    madhab_preference: Optional[str]
    preferred_method: str
    preferred_date: Optional[datetime]
    status: str
    rating: Optional[int]
    review: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class ConsultationDetailResponse(ConsultationResponse):
    """Detailed consultation response"""
    imam_notes: Optional[str]
    resolution: Optional[str]
    original_prompt: Optional[str]
    deepseek_response: Optional[str]
    reason_for_consultation: Optional[str]
    actual_date: Optional[datetime]
    completed_at: Optional[datetime]
    duration_minutes: int


class ConsultationRatingRequest(BaseModel):
    """Schema for rating a consultation"""
    rating: int  # 1-5
    review: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "rating": 5,
                "review": "The imam provided excellent guidance. Very helpful!"
            }
        }


class ConsultationListResponse(BaseModel):
    """Response for list of consultations"""
    id: int
    title: str
    category: Optional[str]
    status: str
    preferred_method: str
    preferred_date: Optional[datetime]
    rating: Optional[int]
    created_at: datetime
    
    class Config:
        from_attributes = True


class ConsultationConfirmRequest(BaseModel):
    """Imam confirming a consultation"""
    status: str  # confirmed, rescheduled
    actual_date: Optional[datetime] = None
    imam_notes: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "confirmed",
                "actual_date": "2026-01-15T18:00:00",
                "imam_notes": "Ready to discuss your family concerns. Please call at..."
            }
        }


class ConsultationCompleteRequest(BaseModel):
    """Imam completing a consultation"""
    imam_notes: Optional[str] = None
    resolution: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "imam_notes": "Discussed the issue in detail",
                "resolution": "Based on Islamic principles, here's my guidance..."
            }
        }
