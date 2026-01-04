from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database import get_db
from models import User, Video, SavedVideo
from schemas import (
    UserCreate, UserResponse, VideoResponse, SearchRequest, 
    SearchResponse, SearchResultResponse, YouTubeSearchRequest
)
from youtube_service import YouTubeService, extract_video_metadata, add_video_to_db, search_videos_by_relevance

router = APIRouter()

# ============= USER ENDPOINTS =============
@router.post("/users", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """Create a new user"""
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        return existing_user
    
    db_user = User(email=user.email, name=user.name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get("/users/{email}", response_model=UserResponse)
def get_user(email: str, db: Session = Depends(get_db)):
    """Get user by email"""
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# ============= SEARCH ENDPOINTS =============
@router.post("/search", response_model=SearchResponse)
def search_videos(search_req: SearchRequest, db: Session = Depends(get_db)):
    """Search for videos by query"""
    # Save search history if user provided
    if search_req.user_email:
        user = db.query(User).filter(User.email == search_req.user_email).first()
        if user:
            from models import Search
            search_record = Search(user_id=user.id, query=search_req.query)
            db.add(search_record)
            db.commit()
    
    # Search videos by relevance
    results = search_videos_by_relevance(db, search_req.query, max_results=10)
    
    search_results = []
    for rank, (video, score) in enumerate(results, 1):
        search_results.append(
            SearchResultResponse(
                video=VideoResponse.from_orm(video),
                relevance_score=score,
                rank=rank
            )
        )
    
    return SearchResponse(
        query=search_req.query,
        results=search_results,
        total_results=len(search_results)
    )

@router.post("/search/youtube")
def search_youtube(search_req: YouTubeSearchRequest):
    """Search YouTube and return results (for populating database)"""
    if not search_req.query:
        raise HTTPException(status_code=400, detail="Query is required")
    
    yt_service = YouTubeService()
    results = yt_service.search_videos(search_req.query, search_req.max_results)
    
    return {
        "query": search_req.query,
        "results": results,
        "count": len(results)
    }

# ============= VIDEO ENDPOINTS =============
@router.get("/videos", response_model=list[VideoResponse])
def get_all_videos(db: Session = Depends(get_db)):
    """Get all videos in database"""
    videos = db.query(Video).all()
    return videos

@router.get("/videos/{video_id}", response_model=VideoResponse)
def get_video(video_id: int, db: Session = Depends(get_db)):
    """Get a specific video by ID"""
    video = db.query(Video).filter(Video.id == video_id).first()
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    return video

@router.post("/videos/import")
def import_youtube_videos(
    youtube_ids: list[str],
    keywords: list[str] = Query(default=[]),
    db: Session = Depends(get_db)
):
    """Import videos from YouTube by their video IDs"""
    yt_service = YouTubeService()
    imported_videos = []
    
    for youtube_id in youtube_ids:
        # Get video details from YouTube
        details = yt_service.get_video_details(youtube_id)
        if details:
            video_data = extract_video_metadata({'snippet': details['snippet'], 'id': {'videoId': youtube_id}})
            
            # Add duration
            content_details = details.get('contentDetails', {})
            duration = content_details.get('duration', 'N/A')
            video_data['duration'] = duration
            
            # Add view count
            statistics = details.get('statistics', {})
            video_data['view_count'] = int(statistics.get('viewCount', 0))
            
            # Add to database
            video = add_video_to_db(db, video_data, keywords)
            imported_videos.append(video)
    
    return {
        "imported_count": len(imported_videos),
        "videos": [VideoResponse.from_orm(v) for v in imported_videos]
    }

# ============= SAVED VIDEOS ENDPOINTS =============
@router.post("/users/{user_id}/saved-videos/{video_id}")
def save_video(user_id: int, video_id: int, db: Session = Depends(get_db)):
    """Save a video for a user"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    video = db.query(Video).filter(Video.id == video_id).first()
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    
    # Check if already saved
    existing = db.query(SavedVideo).filter(
        SavedVideo.user_id == user_id,
        SavedVideo.video_id == video_id
    ).first()
    
    if existing:
        return {"message": "Video already saved"}
    
    saved_video = SavedVideo(user_id=user_id, video_id=video_id)
    db.add(saved_video)
    db.commit()
    
    return {"message": "Video saved successfully"}

@router.get("/users/{user_id}/saved-videos", response_model=list[VideoResponse])
def get_saved_videos(user_id: int, db: Session = Depends(get_db)):
    """Get all saved videos for a user"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    saved_videos = db.query(Video).join(SavedVideo).filter(
        SavedVideo.user_id == user_id
    ).all()
    
    return saved_videos

@router.delete("/users/{user_id}/saved-videos/{video_id}")
def unsave_video(user_id: int, video_id: int, db: Session = Depends(get_db)):
    """Remove a saved video for a user"""
    saved_video = db.query(SavedVideo).filter(
        SavedVideo.user_id == user_id,
        SavedVideo.video_id == video_id
    ).first()
    
    if not saved_video:
        raise HTTPException(status_code=404, detail="Saved video not found")
    
    db.delete(saved_video)
    db.commit()
    
    return {"message": "Video removed from saved"}
