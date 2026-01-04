"""
YouTube AI Service
Provides AI-powered video search with keyword extraction using Groq AI
"""

import os
import json
import httpx
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

class YouTubeAIService:
    def __init__(self):
        self.groq_api_key = os.getenv("GROQ_API_KEY")
        self.youtube_api_key = os.getenv("YOUTUBE_API_KEY")
        self.groq_model = "llama-3.3-70b-versatile"
        
    async def extract_keywords_from_prompt(self, user_prompt: str) -> dict:
        """
        Uses Groq AI to understand user prompt and extract relevant keywords
        for YouTube search
        
        Returns:
            {
                'main_topic': str,
                'keywords': [str],
                'search_query': str
            }
        """
        try:
            if not self.groq_api_key:
                return {
                    "main_topic": "Islamic Content",
                    "keywords": [user_prompt[:20]],
                    "search_query": f"Islamic {user_prompt}"
                }
            
            system_prompt = """You are an expert at understanding Islamic topics and extracting search keywords.
            
            When given a user's prompt, you must:
            1. Identify the main Islamic topic or concern
            2. Extract 2-3 relevant keywords
            3. Create a natural YouTube search query that would find relevant Islamic videos
            
            Always respond in JSON format:
            {
                "main_topic": "The main topic/concern",
                "keywords": ["keyword1", "keyword2", "keyword3"],
                "search_query": "Natural YouTube search query for Islamic videos about this topic"
            }
            
            Focus on Islamic perspectives, Quranic guidance, and Islamic teachings."""
            
            user_message = f"Extract search keywords and create a YouTube query for: {user_prompt}"
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.groq_api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": self.groq_model,
                        "messages": [
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": user_message}
                        ],
                        "temperature": 0.7,
                        "max_tokens": 300
                    },
                    timeout=15.0
                )
                
                if response.status_code == 200:
                    result = response.json()
                    content = result['choices'][0]['message']['content'].strip()
                    
                    # Parse JSON from response
                    try:
                        json_start = content.find('{')
                        json_end = content.rfind('}') + 1
                        if json_start != -1 and json_end > json_start:
                            json_str = content[json_start:json_end]
                            return json.loads(json_str)
                    except (json.JSONDecodeError, ValueError):
                        pass
                    
                    # Fallback parsing
                    return {
                        "main_topic": "Islamic Guidance",
                        "keywords": user_prompt.split()[:3],
                        "search_query": f"Islamic {user_prompt}"
                    }
                else:
                    # Fallback if API fails
                    return {
                        "main_topic": "Islamic Content",
                        "keywords": user_prompt.split()[:3],
                        "search_query": f"Islamic {user_prompt}"
                    }
                    
        except Exception as e:
            print(f"Error in extract_keywords_from_prompt: {e}")
            return {
                "main_topic": "Islamic Guidance",
                "keywords": ["islam", "quran"],
                "search_query": f"Islamic {user_prompt}"
            }
    
    async def search_youtube_videos(self, search_query: str, max_results: int = 6) -> list:
        """
        Searches YouTube for videos using the provided query
        
        Returns:
            List of videos with: id, title, description, thumbnail, channel, url
        """
        try:
            if not self.youtube_api_key:
                return []
            
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    "https://www.googleapis.com/youtube/v3/search",
                    params={
                        "part": "snippet",
                        "q": search_query,
                        "type": "video",
                        "maxResults": max_results,
                        "key": self.youtube_api_key,
                        "order": "relevance",
                        "relevanceLanguage": "en"
                    },
                    timeout=15.0
                )
                
                if response.status_code == 200:
                    data = response.json()
                    videos = []
                    
                    for item in data.get('items', []):
                        video_data = {
                            'id': item['id'].get('videoId', ''),
                            'title': item['snippet'].get('title', ''),
                            'description': item['snippet'].get('description', ''),
                            'thumbnail': item['snippet']['thumbnails'].get('medium', {}).get('url', ''),
                            'channel': item['snippet'].get('channelTitle', 'Unknown Channel'),
                            'url': f"https://www.youtube.com/watch?v={item['id'].get('videoId', '')}"
                        }
                        if video_data['id']:  # Only include if valid video ID
                            videos.append(video_data)
                    
                    return videos
                else:
                    return []
                    
        except Exception as e:
            print(f"Error in search_youtube_videos: {e}")
            return []
    
    async def search_personalized_videos(self, user_prompt: str, max_results: int = 6) -> dict:
        """
        Main method that orchestrates keyword extraction and YouTube search
        
        Returns:
            {
                'main_topic': str,
                'keywords': [str],
                'search_query': str,
                'videos': [...],
                'video_count': int,
                'ai_generated': bool
            }
        """
        try:
            # Step 1: Extract keywords using AI
            keywords_data = await self.extract_keywords_from_prompt(user_prompt)
            
            # Step 2: Search YouTube using the generated query
            videos = await self.search_youtube_videos(keywords_data['search_query'], max_results)
            
            # Step 3: Return combined results
            return {
                'main_topic': keywords_data.get('main_topic', 'Islamic Content'),
                'keywords': keywords_data.get('keywords', []),
                'search_query': keywords_data.get('search_query', user_prompt),
                'videos': videos,
                'video_count': len(videos),
                'ai_generated': True
            }
            
        except Exception as e:
            print(f"Error in search_personalized_videos: {e}")
            return {
                'main_topic': 'Error',
                'keywords': [],
                'search_query': user_prompt,
                'videos': [],
                'video_count': 0,
                'ai_generated': False,
                'error': str(e)
            }
