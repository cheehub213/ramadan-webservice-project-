"""
Videos Routes (YouTube Search) - Protected endpoints requiring authentication
"""
from fastapi import APIRouter, HTTPException, Depends
from typing import Optional
import os
import httpx

from schemas.videos import VideoSearchRequest, VideoResponse
from .auth import get_current_user
from models_extended import User

router = APIRouter()

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY", "")


@router.post("/search")
@router.post("/search-by-prompt")
async def search_videos(
    request: VideoSearchRequest,
    current_user: User = Depends(get_current_user)
):
    """Search YouTube for Islamic videos (requires authentication)"""
    try:
        query = request.prompt  # Use prompt field from request
        max_results = request.max_results or 10
        
        # Add Islamic context to search
        if "ramadan" not in query.lower() and "islamic" not in query.lower():
            query = f"Islamic {query}"
        
        if YOUTUBE_API_KEY:
            # Use YouTube Data API
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    "https://www.googleapis.com/youtube/v3/search",
                    params={
                        "part": "snippet",
                        "q": query,
                        "type": "video",
                        "maxResults": max_results,
                        "key": YOUTUBE_API_KEY,
                        "safeSearch": "strict"
                    }
                )
                data = response.json()
                
                videos = []
                for item in data.get("items", []):
                    videos.append({
                        "video_id": item["id"]["videoId"],
                        "title": item["snippet"]["title"],
                        "description": item["snippet"]["description"],
                        "thumbnail": item["snippet"]["thumbnails"]["medium"]["url"],
                        "channel": item["snippet"]["channelTitle"],
                        "published_at": item["snippet"]["publishedAt"]
                    })
                
                return {"videos": videos, "search_query": query}
        else:
            # Return curated list if no API key
            return {
                "videos": get_curated_videos(query),
                "search_query": query
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/curated")
async def get_curated_list(
    category: Optional[str] = None,
    current_user: User = Depends(get_current_user)
):
    """Get curated Islamic videos (requires authentication)"""
    videos = get_curated_videos(category or "ramadan")
    return {"videos": videos}


def get_curated_videos(topic: str) -> list:
    """Return curated video list for common topics"""
    curated = {
        "ramadan": [
            {
                "video_id": "example1",
                "title": "Benefits of Fasting in Ramadan",
                "description": "Learn about the spiritual and physical benefits of fasting",
                "thumbnail": "https://img.youtube.com/vi/example1/mqdefault.jpg",
                "channel": "Islamic Guidance",
                "published_at": "2024-03-01"
            },
            {
                "video_id": "example2",
                "title": "How to Maximize Your Ramadan",
                "description": "Tips for making the most of the blessed month",
                "thumbnail": "https://img.youtube.com/vi/example2/mqdefault.jpg",
                "channel": "Yaqeen Institute",
                "published_at": "2024-03-01"
            }
        ],
        "quran": [
            {
                "video_id": "quran1",
                "title": "Beautiful Quran Recitation",
                "description": "Peaceful recitation for reflection",
                "thumbnail": "https://img.youtube.com/vi/quran1/mqdefault.jpg",
                "channel": "Quran Central",
                "published_at": "2024-01-01"
            }
        ],
        "prayer": [
            {
                "video_id": "prayer1",
                "title": "How to Pray - Complete Guide",
                "description": "Step by step guide to Islamic prayer",
                "thumbnail": "https://img.youtube.com/vi/prayer1/mqdefault.jpg",
                "channel": "Islamic Academy",
                "published_at": "2024-01-01"
            }
        ]
    }
    
    # Return matching videos or default to ramadan
    for key in curated:
        if key.lower() in topic.lower():
            return curated[key]
    
    return curated["ramadan"]
