from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from app.database import Base

class QuranArabic(Base):
    """Quran verses in Arabic"""
    __tablename__ = "quran_arabic"
    
    id = Column(Integer, primary_key=True, index=True)
    surah_number = Column(Integer, nullable=False)
    surah_name = Column(String(255), nullable=False)
    ayah_number = Column(Integer, nullable=False)
    ayah_text = Column(Text, nullable=False)
    topic = Column(String(255))  # For categorization (e.g., patience, forgiveness, etc.)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    class Config:
        from_attributes = True

class QuranEnglish(Base):
    """Quran verses in English"""
    __tablename__ = "quran_english"
    
    id = Column(Integer, primary_key=True, index=True)
    surah_number = Column(Integer, nullable=False)
    surah_name = Column(String(255), nullable=False)
    ayah_number = Column(Integer, nullable=False)
    ayah_text = Column(Text, nullable=False)
    topic = Column(String(255))  # For categorization
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    class Config:
        from_attributes = True

class Hadith(Base):
    """Hadiths collection"""
    __tablename__ = "hadiths"
    
    id = Column(Integer, primary_key=True, index=True)
    hadith_number = Column(String(50), unique=True, nullable=False)
    narrator = Column(String(255))
    hadith_text_arabic = Column(Text, nullable=False)
    hadith_text_english = Column(Text, nullable=False)
    topic = Column(String(255))  # For categorization
    source = Column(String(255))  # e.g., Sahih Bukhari, Muslim, etc.
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    class Config:
        from_attributes = True
