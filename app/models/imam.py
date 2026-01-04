from sqlalchemy import Column, Integer, String, Text, DateTime, Float, Boolean, Enum
from sqlalchemy.sql import func
from app.database import Base
import enum
from datetime import datetime

class ImamSpecialization(str, enum.Enum):
    """Imam specializations/expertise"""
    GENERAL = "general"  # General Islamic guidance
    FIQH = "fiqh"  # Islamic jurisprudence
    QURAN = "quran"  # Quranic interpretation (Tafsir)
    HADITH = "hadith"  # Hadith knowledge
    FAMILY = "family"  # Family and marriage issues
    YOUTH = "youth"  # Youth counseling
    BUSINESS = "business"  # Islamic business ethics
    SPIRITUALITY = "spirituality"  # Spiritual guidance
    MADHAB = "madhab"  # Specific madhab expert (Hanafi, Maliki, Shafi'i, Hanbali)


class ConsultationStatus(str, enum.Enum):
    """Consultation booking status"""
    PENDING = "pending"  # Waiting for imam confirmation
    CONFIRMED = "confirmed"  # Imam confirmed the booking
    CANCELLED = "cancelled"  # Consultation cancelled
    COMPLETED = "completed"  # Consultation finished
    RESCHEDULED = "rescheduled"  # Rescheduled by imam or user


class ConsultationMethod(str, enum.Enum):
    """Consultation delivery method"""
    PHONE = "phone"  # Phone call
    EMAIL = "email"  # Email correspondence
    IN_PERSON = "in_person"  # Face-to-face meeting
    VIDEO = "video"  # Video call
    MESSAGING = "messaging"  # Chat/messaging service


class Imam(Base):
    """Imam profiles for direct consultation"""
    __tablename__ = "imams"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)  # Imam's name
    title = Column(String(255))  # Title (e.g., "Dr.", "Mufti", etc.)
    
    # Expertise and background
    specializations = Column(String(500))  # Comma-separated specializations
    madhab = Column(String(100))  # Islamic school (Hanafi, Maliki, Shafi'i, Hanbali)
    bio = Column(Text)  # Biography/description
    years_experience = Column(Integer)  # Years of Islamic knowledge
    qualifications = Column(Text)  # Educational qualifications
    
    # Contact information
    email = Column(String(255), unique=True, nullable=False)
    phone = Column(String(20))
    website = Column(String(255))
    
    # Consultation methods offered
    consultation_methods = Column(String(200))  # Comma-separated methods (phone, email, video, etc.)
    consultation_fee = Column(Float, default=0.0)  # Consultation fee (if any)
    currency = Column(String(10), default="USD")
    
    # Availability
    is_available = Column(Boolean, default=True)
    languages = Column(String(200))  # Comma-separated languages (English, Arabic, etc.)
    timezone = Column(String(50))  # Imam's timezone
    
    # Rating and reviews
    average_rating = Column(Float, default=5.0)  # 0-5 stars
    total_consultations = Column(Integer, default=0)
    total_reviews = Column(Integer, default=0)
    
    # Metadata
    verified = Column(Boolean, default=False)  # Is imam verified?
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    class Config:
        from_attributes = True


class Consultation(Base):
    """User consultation bookings with imams"""
    __tablename__ = "consultations"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Relationships
    imam_id = Column(Integer, nullable=False)  # FK to Imam
    user_id = Column(String(255), nullable=False)  # Anonymous user ID or email
    
    # Consultation details
    title = Column(String(255), nullable=False)  # Brief title of concern
    description = Column(Text, nullable=False)  # Detailed description of issue
    category = Column(String(100))  # Category (family, finance, spirituality, etc.)
    madhab_preference = Column(String(100))  # Preferred madhab (optional)
    
    # Deepseek response context
    original_prompt = Column(Text)  # Original user prompt
    deepseek_response = Column(Text)  # The response that was confusing/insufficient
    reason_for_consultation = Column(Text)  # Why they're seeking imam consultation
    
    # Scheduling
    preferred_method = Column(String(50))  # Preferred consultation method
    preferred_date = Column(DateTime)  # Preferred date/time
    actual_date = Column(DateTime)  # Actual consultation date/time
    duration_minutes = Column(Integer, default=30)  # Expected duration
    
    # Status and outcomes
    status = Column(String(50), default="pending")  # pending, confirmed, completed, cancelled
    imam_notes = Column(Text)  # Imam's notes/response
    resolution = Column(Text)  # Resolution provided by imam
    rating = Column(Integer)  # User rating after consultation (1-5)
    review = Column(Text)  # User review after consultation
    
    # Metadata
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    completed_at = Column(DateTime)  # When consultation was completed
    
    class Config:
        from_attributes = True
