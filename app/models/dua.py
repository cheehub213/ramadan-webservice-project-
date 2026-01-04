from sqlalchemy import Column, Integer, String, Text, DateTime, Float
from sqlalchemy.sql import func
from app.database import Base
from datetime import datetime

class DuaRequest(Base):
    """Store dua generator requests"""
    __tablename__ = "dua_requests"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # User info
    user_email = Column(String(255), nullable=False)
    user_name = Column(String(255))
    
    # Request details
    problem_description = Column(Text, nullable=False)  # User's problem/situation
    problem_category = Column(String(100))  # Category: family, health, work, finance, spiritual, etc.
    language = Column(String(50), default="English")  # Language for response
    
    # Generated responses
    generated_aya = Column(Text)  # Quranic verse with explanation
    generated_hadith = Column(Text)  # Relevant hadith with explanation
    generated_dua = Column(Text)  # Personalized dua
    
    # Metadata
    deepseek_prompt = Column(Text)  # The prompt sent to Deepseek
    deepseek_response = Column(Text)  # Raw response from Deepseek
    
    # User feedback
    is_helpful = Column(String(10))  # "yes", "no", or null
    user_feedback = Column(Text)  # Additional user comments
    
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    class Config:
        from_attributes = True


class DuaCategory(Base):
    """Categories for dua requests"""
    __tablename__ = "dua_categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text)
    icon = Column(String(50))  # Icon name or emoji
    example_problems = Column(Text)  # Comma-separated examples
    
    class Config:
        from_attributes = True
