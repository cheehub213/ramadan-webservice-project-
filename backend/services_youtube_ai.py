"""
YouTube AI Service - Personalized Islamic Video Search
Uses Groq AI to extract keywords from user prompts and search YouTube
"""
import json
import httpx
import os
from typing import List, Dict, Optional
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
env_path = Path(__file__).parent / ".env"
load_dotenv(env_path)

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "").strip()
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY", "").strip()

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
YOUTUBE_API_URL = "https://www.googleapis.com/youtube/v3/search"


class YouTubeAIService:
    """Service for AI-powered personalized YouTube video search"""

    @staticmethod
    async def extract_keywords_from_prompt(user_prompt: str) -> Dict:
        """
        Use Groq AI to extract Islamic topic keywords from user's prompt
        """
        
        system_prompt = """You are an Islamic content AI assistant. When given a user's question or problem, you will:

1. Understand their specific concern or topic
2. Extract 3-5 relevant Islamic keywords/topics that would be helpful
3. Suggest appropriate YouTube search terms for Islamic educational content

Return ONLY valid JSON in this format:
{
    "main_topic": "The primary Islamic topic (e.g., Patience, Marriage, Anger Management)",
    "keywords": ["keyword1", "keyword2", "keyword3", "keyword4"],
    "search_query": "A specific YouTube search query combining the topic with 'Islamic' or 'Quran' or 'Hadith'"
}

Examples:
- User asks about marriage → search_query: "Islamic marriage guidance Quran"
- User asks about anger → search_query: "Islamic anger management hadith"
- User asks about finances → search_query: "Islamic financial wisdom Quran"

Make sure the search_query includes words like "Islamic", "Quran", "Hadith", "Islam" to get relevant content."""

        user_message = f"""Extract Islamic topic keywords for this user question:

"{user_prompt}"

Provide keywords and a YouTube search query that will find relevant Islamic educational content."""

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    GROQ_API_URL,
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {GROQ_API_KEY}"
                    },
                    json={
                        "model": "llama-3.3-70b-versatile",
                        "messages": [
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": user_message}
                        ],
                        "temperature": 0.7,
                        "max_tokens": 300
                    }
                )
                
                if response.status_code == 200:
                    result = response.json()
                    ai_response = result["choices"][0]["message"]["content"]
                    
                    # Clean and parse response
                    cleaned = ai_response.strip()
                    if cleaned.startswith("```json"):
                        cleaned = cleaned[7:]
                    if cleaned.startswith("```"):
                        cleaned = cleaned[3:]
                    if cleaned.endswith("```"):
                        cleaned = cleaned[:-3]
                    cleaned = cleaned.strip()
                    
                    try:
                        data = json.loads(cleaned)
                        return {
                            "main_topic": data.get("main_topic", "Islamic Guidance"),
                            "keywords": data.get("keywords", []),
                            "search_query": data.get("search_query", "Islamic wisdom Quran Hadith"),
                            "success": True
                        }
                    except json.JSONDecodeError:
                        # Fallback if JSON parsing fails
                        return {
                            "main_topic": "Islamic Content",
                            "keywords": ["Islam", "Quran", "Hadith"],
                            "search_query": f"{user_prompt} Islamic wisdom",
                            "success": False
                        }
                else:
                    return YouTubeAIService.get_default_keywords()
                    
        except Exception as e:
            print(f"Error extracting keywords: {str(e)}")
            return YouTubeAIService.get_default_keywords()

    @staticmethod
    async def search_youtube_videos(search_query: str, max_results: int = 6) -> List[Dict]:
        """
        Search YouTube for videos using the provided query
        Returns: List of video data with title, description, thumbnail, video URL
        """
        
        if not YOUTUBE_API_KEY:
            return []
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(
                    YOUTUBE_API_URL,
                    params={
                        "part": "snippet",
                        "q": search_query,
                        "type": "video",
                        "maxResults": max_results,
                        "relevanceLanguage": "en",
                        "order": "relevance",
                        "key": YOUTUBE_API_KEY
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    videos = []
                    
                    for item in data.get("items", []):
                        snippet = item.get("snippet", {})
                        video_id = item.get("id", {}).get("videoId")
                        
                        if video_id:
                            videos.append({
                                "video_id": video_id,
                                "title": snippet.get("title", ""),
                                "description": snippet.get("description", ""),
                                "thumbnail": snippet.get("thumbnails", {}).get("medium", {}).get("url", ""),
                                "channel": snippet.get("channelTitle", ""),
                                "published_at": snippet.get("publishedAt", ""),
                                "url": f"https://www.youtube.com/watch?v={video_id}"
                            })
                    
                    return videos
                else:
                    print(f"YouTube API error: {response.status_code}")
                    return []
                    
        except Exception as e:
            print(f"Error searching YouTube: {str(e)}")
            return []

    @staticmethod
    async def search_personalized_videos(user_prompt: str, max_results: int = 6) -> Dict:
        """
        Main method: Extract keywords from prompt and search YouTube
        """
        
        # Step 1: Extract keywords using AI
        keywords_result = await YouTubeAIService.extract_keywords_from_prompt(user_prompt)
        
        # Step 2: Search YouTube with extracted query
        videos = await YouTubeAIService.search_youtube_videos(
            keywords_result["search_query"],
            max_results=max_results
        )
        
        return {
            "main_topic": keywords_result["main_topic"],
            "keywords": keywords_result["keywords"],
            "search_query": keywords_result["search_query"],
            "videos": videos,
            "video_count": len(videos),
            "ai_generated": True
        }

    @staticmethod
    def get_default_keywords() -> Dict:
        """Return default keywords if AI fails"""
        return {
            "main_topic": "Islamic Guidance",
            "keywords": ["Islam", "Quran", "Hadith", "Islamic wisdom"],
            "search_query": "Islamic wisdom Quran Hadith teachings",
            "success": False
        }
