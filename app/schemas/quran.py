from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class QuranArabicResponse(BaseModel):
    id: int
    surah_number: int
    surah_name: str
    surah_name_arabic: Optional[str] = None
    ayah_number: int
    ayah_text: str
    topic: Optional[str] = None
    explanation: Optional[str] = None  # Why this verse was chosen
    relevance_score: Optional[float] = None  # How relevant (0-1)
    
    class Config:
        from_attributes = True

class QuranEnglishResponse(BaseModel):
    id: int
    surah_number: int
    surah_name: str
    ayah_number: int
    ayah_text: str
    topic: Optional[str] = None
    explanation: Optional[str] = None  # Why this verse was chosen
    relevance_score: Optional[float] = None  # How relevant (0-1)
    
    class Config:
        from_attributes = True

class BilingualQuranResponse(BaseModel):
    """Combined Arabic and English response for a single verse"""
    surah_number: int
    surah_name_english: str
    surah_name_arabic: Optional[str] = None
    ayah_number: int
    ayah_text_english: str
    ayah_text_arabic: str
    topic: Optional[str] = None
    explanation_english: Optional[str] = None
    explanation_arabic: Optional[str] = None
    relevance_score: Optional[float] = None
    matched_keywords: Optional[list] = None  # Which keywords matched
    
    class Config:
        from_attributes = True

class HadithResponse(BaseModel):
    id: int
    hadith_number: str
    narrator: Optional[str] = None
    hadith_text_arabic: str
    hadith_text_english: str
    topic: Optional[str] = None
    source: Optional[str] = None
    explanation_english: Optional[str] = None
    explanation_arabic: Optional[str] = None
    relevance_score: Optional[float] = None
    matched_keywords: Optional[list] = None  # Which keywords matched
    
    class Config:
        from_attributes = True
