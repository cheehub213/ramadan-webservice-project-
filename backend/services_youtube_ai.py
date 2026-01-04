"""
YouTube AI Service - Personalized Islamic Video Search
Uses Groq AI to extract optimized keywords from user prompts and search YouTube
"""
import json
import httpx
import os
import re
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
        Use Groq AI to extract optimized Islamic YouTube search terms from user's long prompt.
        Converts long, emotional prompts into concise 3-5 word search queries.
        """

        system_prompt = """You are an expert at converting long user requests into SHORT, OPTIMIZED YouTube search queries for Islamic content.

CRITICAL RULES:
1. Output search_query must be 3-5 words MAXIMUM (YouTube works best with short queries)
2. Always include "Islamic" or "Islam" in the search query
3. Focus on the MAIN topic, ignore emotional details
4. Use simple, common search terms

EXAMPLES:

User: "I am fasting this Ramadan but I'm really struggling emotionally and spiritually. I get angry very fast during the day, especially when I'm tired or hungry, and later I regret my words."
search_query: "anger management Islamic Ramadan"

User: "My marriage is going through a very difficult time and I don't know what to do. My spouse and I argue constantly and I feel like giving up but I want to save our marriage according to Islamic principles."
search_query: "Islamic marriage advice"

User: "I'm having financial difficulties and don't know how to pay my bills. I'm worried about my family. Is there any Islamic guidance?"
search_query: "Islamic financial guidance"

User: "How to pray tahajjud and what are the benefits according to hadith?"
search_query: "tahajjud prayer benefits"

Return ONLY valid JSON:
{"main_topic": "2-3 word topic", "keywords": ["word1", "word2", "word3"], "search_query": "3-5 word YouTube search"}"""

        user_message = f"""Convert this user request into a SHORT YouTube search query (3-5 words max):

"{user_prompt}"

Return JSON with a concise search_query optimized for YouTube."""

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
                        "temperature": 0.3,  # Low temperature for consistent output
                        "max_tokens": 200
                    }
                )

                if response.status_code == 200:
                    result = response.json()
                    ai_response = result["choices"][0]["message"]["content"]
                    
                    print(f"[YouTube AI] Raw response: {ai_response[:200]}")

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
                        search_query = data.get("search_query", "")
                        
                        # Ensure search query is not too long (max 50 chars)
                        if len(search_query) > 50:
                            words = search_query.split()[:5]
                            search_query = " ".join(words)
                        
                        # Ensure it has Islamic context
                        search_lower = search_query.lower()
                        if "islam" not in search_lower and "quran" not in search_lower and "hadith" not in search_lower:
                            search_query = f"Islamic {search_query}"
                        
                        print(f"[YouTube AI] Optimized search: {search_query}")
                        
                        return {
                            "main_topic": data.get("main_topic", "Islamic Guidance"),
                            "keywords": data.get("keywords", []),
                            "search_query": search_query,
                            "original_prompt": user_prompt[:100] + "..." if len(user_prompt) > 100 else user_prompt,
                            "success": True
                        }
                    except json.JSONDecodeError:
                        # Fallback: Extract key Islamic terms manually
                        return YouTubeAIService.fallback_keyword_extraction(user_prompt)
                else:
                    print(f"[YouTube AI] API error: {response.status_code}")
                    return YouTubeAIService.fallback_keyword_extraction(user_prompt)

        except Exception as e:
            print(f"[YouTube AI] Error: {str(e)}")
            return YouTubeAIService.fallback_keyword_extraction(user_prompt)

    @staticmethod
    def fallback_keyword_extraction(user_prompt: str) -> Dict:
        """
        Fallback method: Extract keywords manually using common Islamic terms
        """
        prompt_lower = user_prompt.lower()
        
        # Define topic mappings
        topic_keywords = {
            "anger": ("Anger Management", "Islamic anger control tips"),
            "fasting": ("Fasting", "Ramadan fasting tips Islamic"),
            "ramadan": ("Ramadan", "Ramadan spiritual guidance"),
            "marriage": ("Marriage", "Islamic marriage advice"),
            "wife": ("Marriage", "Islamic marriage guidance"),
            "husband": ("Marriage", "Islamic spouse relationship"),
            "patience": ("Patience", "Islamic patience sabr"),
            "prayer": ("Prayer", "Islamic prayer guide salah"),
            "money": ("Finance", "Islamic financial guidance"),
            "debt": ("Finance", "Islamic debt advice halal"),
            "anxiety": ("Mental Health", "Islamic anxiety relief"),
            "depression": ("Mental Health", "Islamic depression help"),
            "death": ("Death", "Islamic death grief comfort"),
            "parent": ("Family", "Islamic parents respect"),
            "children": ("Family", "Islamic parenting advice"),
            "sin": ("Repentance", "Islamic repentance tawbah"),
            "forgiveness": ("Forgiveness", "Islamic forgiveness Allah"),
            "dua": ("Dua", "powerful dua Islamic"),
            "quran": ("Quran", "Quran recitation guidance"),
            "hadith": ("Hadith", "hadith teachings prophet"),
        }
        
        # Find matching topics
        for keyword, (topic, search) in topic_keywords.items():
            if keyword in prompt_lower:
                return {
                    "main_topic": topic,
                    "keywords": [keyword, "Islamic", "guidance"],
                    "search_query": search,
                    "original_prompt": user_prompt[:100] + "..." if len(user_prompt) > 100 else user_prompt,
                    "success": True
                }
        
        # Default fallback
        return {
            "main_topic": "Islamic Guidance",
            "keywords": ["Islam", "guidance", "wisdom"],
            "search_query": "Islamic guidance motivation",
            "original_prompt": user_prompt[:100] + "..." if len(user_prompt) > 100 else user_prompt,
            "success": False
        }

    @staticmethod
    async def search_youtube_videos(search_query: str, max_results: int = 6) -> List[Dict]:
        """
        Search YouTube for videos using the provided query
        Returns: List of video data with title, description, thumbnail, video URL
        """

        if not YOUTUBE_API_KEY:
            print("[YouTube AI] No YouTube API key configured - returning demo results")
            return YouTubeAIService.get_demo_videos(search_query)

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
                        "safeSearch": "strict",
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
                                "description": snippet.get("description", "")[:200] + "..." if len(snippet.get("description", "")) > 200 else snippet.get("description", ""),
                                "thumbnail": snippet.get("thumbnails", {}).get("medium", {}).get("url", ""),
                                "channel": snippet.get("channelTitle", ""),
                                "published_at": snippet.get("publishedAt", ""),
                                "url": f"https://www.youtube.com/watch?v={video_id}"
                            })

                    print(f"[YouTube AI] Found {len(videos)} videos for: {search_query}")
                    return videos
                else:
                    print(f"[YouTube AI] YouTube API error: {response.status_code}")
                    return YouTubeAIService.get_demo_videos(search_query)

        except Exception as e:
            print(f"[YouTube AI] Error searching YouTube: {str(e)}")
            return YouTubeAIService.get_demo_videos(search_query)

    @staticmethod
    async def search_personalized_videos(user_prompt: str, max_results: int = 6) -> Dict:
        """
        Main method: Extract keywords from prompt and search YouTube
        """
        print(f"[YouTube AI] Processing prompt: {user_prompt[:80]}...")

        # Step 1: Extract optimized keywords using AI
        keywords_result = await YouTubeAIService.extract_keywords_from_prompt(user_prompt)
        
        print(f"[YouTube AI] Search query: {keywords_result['search_query']}")

        # Step 2: Search YouTube with extracted query
        videos = await YouTubeAIService.search_youtube_videos(
            keywords_result["search_query"],
            max_results=max_results
        )

        return {
            "main_topic": keywords_result["main_topic"],
            "keywords": keywords_result["keywords"],
            "search_query": keywords_result["search_query"],
            "original_prompt_preview": keywords_result.get("original_prompt", user_prompt[:100]),
            "videos": videos,
            "video_count": len(videos),
            "ai_optimized": keywords_result.get("success", True)
        }

    @staticmethod
    def get_demo_videos(search_query: str) -> List[Dict]:
        """Return demo videos when YouTube API is not available"""
        return [
            {
                "video_id": "demo1",
                "title": f"Islamic Guidance: {search_query.title()}",
                "description": "This is a demo video. Configure YOUTUBE_API_KEY in .env to get real results.",
                "thumbnail": "https://via.placeholder.com/320x180?text=Demo+Video",
                "channel": "Demo Channel",
                "published_at": "2024-01-01T00:00:00Z",
                "url": "https://www.youtube.com/watch?v=demo"
            }
        ]

    @staticmethod
    def get_default_keywords() -> Dict:
        """Return default keywords if AI fails"""
        return {
            "main_topic": "Islamic Guidance",
            "keywords": ["Islam", "Quran", "Hadith"],
            "search_query": "Islamic guidance Quran",
            "success": False
        }
