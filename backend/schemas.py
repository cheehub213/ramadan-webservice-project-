from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

# User Schemas
class UserCreate(BaseModel):
    email: str
    name: str

class UserResponse(BaseModel):
    id: int
    email: str
    name: str
    created_at: datetime
    
    class Config:
        from_attributes = True

# Video Schemas
class KeywordResponse(BaseModel):
    id: int
    name: str
    
    class Config:
        from_attributes = True

class VideoCreate(BaseModel):
    youtube_id: str
    title: str
    description: str
    channel: str
    duration: str
    thumbnail_url: str
    view_count: int = 0
    keywords: List[str] = []

class VideoResponse(BaseModel):
    id: int
    youtube_id: str
    title: str
    description: str
    channel: str
    duration: str
    thumbnail_url: str
    view_count: int
    rating: float
    keywords: List[KeywordResponse]
    
    class Config:
        from_attributes = True

# Search Schemas
class SearchRequest(BaseModel):
    query: str
    user_email: Optional[str] = None

class SearchResultResponse(BaseModel):
    video: VideoResponse
    relevance_score: float
    rank: int
    
    class Config:
        from_attributes = True

class SearchResponse(BaseModel):
    query: str
    results: List[SearchResultResponse]
    total_results: int

# YouTube Integration Schemas
class YouTubeSearchRequest(BaseModel):
    query: str
    max_results: int = 10

class YouTubeVideoImport(BaseModel):
    youtube_ids: List[str]
    keywords: List[str] = []
