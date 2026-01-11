"""
AI Analyzer Schemas
"""
from pydantic import BaseModel
from typing import Optional


class AnalyzeRequest(BaseModel):
    """Request for AI analysis"""
    question: str
    email: Optional[str] = None


class AnalyzeResponse(BaseModel):
    """AI analysis response"""
    question: str
    ayah: Optional[dict] = None
    hadith: Optional[dict] = None
    ai_explanation: str
    match_found: bool = True
    available_topics: Optional[list] = None
