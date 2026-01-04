from pydantic import BaseModel
from typing import Optional

class SearchRequest(BaseModel):
    """Request model for user problem/prompt"""
    prompt: str  # Accept both English and Arabic prompts
    response_language: Optional[str] = "bilingual"  # "en", "ar", or "bilingual" for both
    include_hadith: bool = True  # Whether to include hadiths in response
    include_quran: bool = True  # Whether to include quran verses in response
    
    class Config:
        json_schema_extra = {
            "example": {
                "prompt": "I'm struggling with patience in difficult times",
                "response_language": "bilingual",
                "include_hadith": True,
                "include_quran": True
            }
        }
