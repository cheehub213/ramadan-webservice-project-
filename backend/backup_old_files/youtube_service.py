import googleapiclient.discovery
from googleapiclient.errors import HttpError
from config import settings
from sqlalchemy.orm import Session
from models import Video, Keyword
from typing import List, Dict

class YouTubeService:
    def __init__(self):
        self.youtube = googleapiclient.discovery.build(
            "youtube", "v3",
            developerKey=settings.YOUTUBE_API_KEY
        )
    
    def search_videos(self, query: str, max_results: int = 10) -> List[Dict]:
        """Search YouTube for videos"""
        try:
            request = self.youtube.search().list(
                q=query,
                part="snippet",
                maxResults=max_results,
                type="video",
                relevanceLanguage="en"
            )
            response = request.execute()
            return response.get('items', [])
        except HttpError as e:
            print(f"YouTube API Error: {e}")
            return []
    
    def get_video_details(self, video_id: str) -> Dict:
        """Get detailed information about a specific video"""
        try:
            request = self.youtube.videos().list(
                part="snippet,contentDetails,statistics",
                id=video_id
            )
            response = request.execute()
            if response.get('items'):
                return response['items'][0]
            return None
        except HttpError as e:
            print(f"YouTube API Error: {e}")
            return None
    
    def search_ramadan_videos(self, topic: str, max_results: int = 10) -> List[Dict]:
        """Search for Ramadan-related Islamic videos"""
        query = f"Ramadan {topic} Islamic lecture"
        return self.search_videos(query, max_results)

def extract_video_metadata(youtube_item: Dict) -> Dict:
    """Extract metadata from YouTube API response"""
    snippet = youtube_item.get('snippet', {})
    video_id = youtube_item.get('id', {}).get('videoId', '')
    
    return {
        'youtube_id': video_id,
        'title': snippet.get('title', ''),
        'description': snippet.get('description', ''),
        'channel': snippet.get('channelTitle', ''),
        'thumbnail_url': snippet.get('thumbnails', {}).get('high', {}).get('url', '')
    }

def add_video_to_db(db: Session, video_data: Dict, keywords: List[str] = None) -> Video:
    """Add a video to the database"""
    # Check if video already exists
    existing_video = db.query(Video).filter(
        Video.youtube_id == video_data['youtube_id']
    ).first()
    
    if existing_video:
        return existing_video
    
    # Get or create keywords
    keyword_objects = []
    if keywords:
        for keyword_name in keywords:
            keyword = db.query(Keyword).filter(
                Keyword.name == keyword_name.lower()
            ).first()
            if not keyword:
                keyword = Keyword(name=keyword_name.lower())
                db.add(keyword)
            keyword_objects.append(keyword)
        db.commit()
    
    # Create new video
    video = Video(
        youtube_id=video_data['youtube_id'],
        title=video_data['title'],
        description=video_data['description'],
        channel=video_data['channel'],
        thumbnail_url=video_data['thumbnail_url'],
        duration=video_data.get('duration', 'N/A'),
        keywords=keyword_objects
    )
    
    db.add(video)
    db.commit()
    db.refresh(video)
    return video

def search_videos_by_relevance(db: Session, query: str, max_results: int = 10) -> List[tuple]:
    """Search videos in database by keyword relevance"""
    query_lower = query.lower()
    keywords = query_lower.split()
    
    videos = db.query(Video).all()
    scored_videos = []
    
    for video in videos:
        score = 0
        # Score by title match
        title_lower = video.title.lower()
        for keyword in keywords:
            if keyword in title_lower:
                score += 2
        
        # Score by keyword match
        for vid_keyword in video.keywords:
            if vid_keyword.name in keywords:
                score += 3
        
        # Score by description match
        desc_lower = video.description.lower()
        for keyword in keywords:
            if keyword in desc_lower:
                score += 1
        
        if score > 0:
            scored_videos.append((video, score))
    
    # Sort by score
    scored_videos.sort(key=lambda x: x[1], reverse=True)
    return scored_videos[:max_results]
