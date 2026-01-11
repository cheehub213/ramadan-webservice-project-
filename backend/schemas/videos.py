"""
Video Search Schemas
"""
from pydantic import BaseModel
from typing import Optional, List


class VideoSearchRequest(BaseModel):
    """Request to search for Islamic videos"""
    prompt: str
    email: Optional[str] = None
    max_results: Optional[int] = 10


class VideoResponse(BaseModel):
    """Video search result"""
    title: str
    youtube_id: str
    channel: str
    duration: Optional[str]
    description: Optional[str]
    thumbnail_url: Optional[str]
