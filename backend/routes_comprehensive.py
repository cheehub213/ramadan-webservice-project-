"""
Complete API Routes for Ramadan Helper
Includes: Users, Dua, Chat, AI Analyzer, Videos, History
"""
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional
from database import SessionLocal

from services_dua import DuaService
from services_chat import ChatService
from services_analyzer import AnalyzerService
from services_ai_analyzer import AIAnalyzerService
from services_youtube_ai import YouTubeAIService
from models_extended import (
    User, DuaHistory, Imam, Conversation, Message, 
    Video, AIAnalysis, UserHistory
)

router = APIRouter(prefix="/api", tags=["api"])

# ============= DEPENDENCY =============
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ============= PYDANTIC MODELS =============
class UserLoginRequest(BaseModel):
    email: str
    name: Optional[str] = None
    user_type: str = "user"

class UserResponse(BaseModel):
    id: int
    email: str
    name: Optional[str]
    user_type: str
    class Config:
        from_attributes = True

class DuaGenerateRequest(BaseModel):
    email: str
    category: str
    context: str

class DuaHistoryResponse(BaseModel):
    id: int
    email: str
    category: str
    context: str
    dua_text_en: str
    dua_text_ar: str
    helpful: Optional[bool]
    created_at: str
    class Config:
        from_attributes = True

class ImamResponse(BaseModel):
    id: int
    name: str
    email: str
    expertise: str
    is_available: bool
    bio: Optional[str]
    class Config:
        from_attributes = True

class ConversationCreateRequest(BaseModel):
    user_email: str
    imam_id: int
    topic: str

class MessageSendRequest(BaseModel):
    conversation_id: int
    sender_email: str
    sender_type: str  # "user" or "imam"
    message_text: str

class MessageResponse(BaseModel):
    id: int
    conversation_id: int
    sender_type: str
    sender_email: str
    message_text: str
    is_read: bool
    created_at: str
    class Config:
        from_attributes = True

class VideoResponse(BaseModel):
    id: int
    title: str
    youtube_id: str
    channel: str
    duration: str
    description: str
    thumbnail_url: Optional[str]
    class Config:
        from_attributes = True

class AnalyzerQuestionRequest(BaseModel):
    email: str
    question: str

class VideoSearchRequest(BaseModel):
    email: str
    prompt: str

class DuaFeedbackRequest(BaseModel):
    dua_id: int
    helpful: bool
    notes: Optional[str] = ""

# ============= USER ENDPOINTS =============
@router.post("/users/login", response_model=UserResponse)
def user_login(request: UserLoginRequest, db: Session = Depends(get_db)):
    """Login/Register user"""
    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        user = User(
            email=request.email,
            name=request.name,
            user_type=request.user_type
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    return user

@router.get("/users/{email}", response_model=UserResponse)
def get_user(email: str, db: Session = Depends(get_db)):
    """Get user by email"""
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# ============= DUA ENDPOINTS =============
@router.get("/dua/categories")
def get_dua_categories():
    """Get all dua categories"""
    return {"categories": DuaService.get_categories()}

@router.post("/dua/generate")
async def generate_dua(request: DuaGenerateRequest, db: Session = Depends(get_db)):
    """Generate a personalized dua using AI - addresses the SPECIFIC situation"""
    try:
        # Try to use AI-powered generation first
        dua_data = await DuaService.generate_dua_with_ai(request.category, request.context)
    except Exception as e:
        print(f"AI generation failed: {e}")
        # Fall back to intelligent template generation
        dua_data = DuaService.generate_dua(request.category, request.context)
    
    try:
        saved_dua = DuaService.save_dua_to_history(db, request.email, dua_data)
        return {
            "id": saved_dua.id,
            "category": dua_data["category"],
            "context": dua_data["context"],
            "dua_text_en": dua_data["dua_text_en"],
            "dua_text_ar": dua_data["dua_text_ar"],
            "how_to_use_en": dua_data.get("how_to_use_en", ""),
            "how_to_use_ar": dua_data.get("how_to_use_ar", ""),
            "ai_generated": dua_data.get("ai_generated", False),
            "timestamp": dua_data.get("timestamp", datetime.now().isoformat())
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/dua/history/{email}", response_model=List[DuaHistoryResponse])
def get_dua_history(email: str, db: Session = Depends(get_db)):
    """Get user's dua history"""
    duas = DuaService.get_user_history(db, email)
    return duas

@router.post("/dua/feedback")
def submit_dua_feedback(request: DuaFeedbackRequest, db: Session = Depends(get_db)):
    """Submit feedback on a dua"""
    dua = DuaService.submit_feedback(db, request.dua_id, request.helpful, request.notes)
    if not dua:
        raise HTTPException(status_code=404, detail="Dua not found")
    return {"status": "success", "dua_id": dua.id}

# ============= IMAM ENDPOINTS =============
@router.get("/imams", response_model=List[ImamResponse])
def get_imams(db: Session = Depends(get_db)):
    """Get all available imams"""
    imams = ChatService.get_all_imams(db)
    return imams

@router.get("/imams/{imam_id}", response_model=ImamResponse)
def get_imam(imam_id: int, db: Session = Depends(get_db)):
    """Get specific imam"""
    imam = ChatService.get_imam_by_id(db, imam_id)
    if not imam:
        raise HTTPException(status_code=404, detail="Imam not found")
    return imam

# ============= CHAT ENDPOINTS =============
@router.post("/chat/conversations")
def create_conversation(request: ConversationCreateRequest, db: Session = Depends(get_db)):
    """Create new conversation with imam"""
    try:
        conversation = ChatService.create_conversation(
            db, request.user_email, request.imam_id, request.topic
        )
        return {
            "id": conversation.id,
            "user_email": conversation.user_email,
            "imam_id": conversation.imam_id,
            "topic": conversation.topic,
            "created_at": conversation.created_at.isoformat()
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/chat/conversations/{user_email}")
def get_user_conversations(user_email: str, db: Session = Depends(get_db)):
    """Get all conversations for user"""
    conversations = ChatService.get_user_conversations(db, user_email)
    return [
        {
            "id": c.id,
            "user_email": c.user_email,
            "imam_id": c.imam_id,
            "imam_name": c.imam.name if c.imam else "Unknown",
            "topic": c.topic,
            "created_at": c.created_at.isoformat(),
            "updated_at": c.updated_at.isoformat()
        }
        for c in conversations
    ]

@router.post("/chat/messages")
def send_message(request: MessageSendRequest, db: Session = Depends(get_db)):
    """Send message in conversation"""
    try:
        message = ChatService.send_message(
            db, request.conversation_id, request.sender_email,
            request.sender_type, request.message_text
        )
        
        # If user sent a message, generate imam response after a delay
        if request.sender_type == "user":
            conversation = db.query(Conversation).filter(
                Conversation.id == request.conversation_id
            ).first()
            if conversation and conversation.imam:
                imam_response_text = ChatService.generate_imam_response(
                    request.message_text, conversation.imam.name
                )
                imam_message = ChatService.send_message(
                    db, request.conversation_id, 
                    conversation.imam.email, "imam",
                    imam_response_text
                )
        
        return {
            "id": message.id,
            "conversation_id": message.conversation_id,
            "sender_type": message.sender_type,
            "message_text": message.message_text,
            "created_at": message.created_at.isoformat()
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/chat/messages/{conversation_id}")
def get_messages(conversation_id: int, db: Session = Depends(get_db)):
    """Get all messages in conversation"""
    messages = ChatService.get_conversation_messages(db, conversation_id)
    return [
        {
            "id": m.id,
            "conversation_id": m.conversation_id,
            "sender_type": m.sender_type,
            "sender_email": m.sender_email,
            "message_text": m.message_text,
            "is_read": m.is_read,
            "created_at": m.created_at.isoformat()
        }
        for m in messages
    ]

# ============= AI ANALYZER ENDPOINTS =============
@router.post("/analyzer/analyze")
async def analyze_question(request: AnalyzerQuestionRequest, db: Session = Depends(get_db)):
    """Analyze Islamic question and return personalized guidance using AI"""
    # Use AI to analyze the prompt and find relevant Quran verse and Hadith
    analysis_result = await AIAnalyzerService.analyze_prompt_with_ai(request.question)
    
    # TODO: Save to database when AIAnalysis model is created
    # For now, just return the AI analysis result
    
    return analysis_result

@router.get("/analyzer/ayahs")
def get_ayahs():
    """Get all Quranic verses"""
    return {"ayahs": AnalyzerService.get_all_ayahs()}

@router.get("/analyzer/hadiths")
def get_hadiths():
    """Get all Hadiths"""
    return {"hadiths": AnalyzerService.get_all_hadiths()}

# ============= VIDEO ENDPOINTS =============
@router.get("/videos", response_model=List[VideoResponse])
def get_videos(db: Session = Depends(get_db)):
    """Get all videos"""
    videos = db.query(Video).all()
    return videos

@router.get("/videos/{video_id}", response_model=VideoResponse)
def get_video(video_id: int, db: Session = Depends(get_db)):
    """Get specific video"""
    video = db.query(Video).filter(Video.id == video_id).first()
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    return video

@router.get("/videos/search")
def search_videos(query: str, db: Session = Depends(get_db)):
    """Search videos by title or description"""
    videos = db.query(Video).filter(
        (Video.title.ilike(f"%{query}%")) |
        (Video.description.ilike(f"%{query}%"))
    ).all()
    return videos

@router.post("/videos/search-by-prompt")
async def search_videos_by_prompt(request: VideoSearchRequest, db: Session = Depends(get_db)):
    """
    AI-powered personalized video search
    Takes user prompt, extracts Islamic keywords, and searches YouTube
    """
    try:
        service = YouTubeAIService()
        result = await service.search_personalized_videos(
            user_prompt=request.prompt,
            max_results=6
        )
        return result
    except Exception as e:
        print(f"Error in video search: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Video search failed: {str(e)}")

@router.post("/videos/add")
def add_video(video: VideoResponse, db: Session = Depends(get_db)):
    """Add new video to database"""
    new_video = Video(**video.dict())
    db.add(new_video)
    db.commit()
    return {"id": new_video.id, "status": "success"}

# ============= HISTORY ENDPOINTS =============
@router.get("/history/{user_email}")
def get_user_history(user_email: str, db: Session = Depends(get_db)):
    """Get user activity history"""
    history = db.query(UserHistory).filter(
        UserHistory.user_email == user_email
    ).order_by(UserHistory.created_at.desc()).all()
    
    return [
        {
            "id": h.id,
            "action_type": h.action_type,
            "action_data": h.action_data,
            "created_at": h.created_at.isoformat()
        }
        for h in history
    ]

@router.post("/history/log")
def log_action(user_email: str, action_type: str, action_data: dict, db: Session = Depends(get_db)):
    """Log user action"""
    history = UserHistory(
        user_email=user_email,
        action_type=action_type,
        action_data=action_data
    )
    db.add(history)
    db.commit()
    return {"status": "logged"}

# ============= HEALTH CHECK =============
@router.get("/health")
def health_check(db: Session = Depends(get_db)):
    """Health check endpoint"""
    try:
        # Test database connection
        db.execute("SELECT 1")
        return {
            "status": "healthy",
            "message": "Backend is running",
            "database": "sqlite",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

# ============= IMAM CHAT ENDPOINTS =============
@router.get("/chat/imam/conversations/{imam_email}")
def get_imam_conversations(imam_email: str, db: Session = Depends(get_db)):
    """Get all conversations for an imam to respond to"""
    from models_extended import Conversation, Imam
    
    imam = db.query(Imam).filter(Imam.email == imam_email).first()
    if not imam:
        imams = ChatService.get_all_imams(db)
        imam = next((i for i in imams if i.email == imam_email), None)
    
    if not imam:
        conversations = db.query(Conversation).order_by(Conversation.updated_at.desc()).all()
    else:
        conversations = db.query(Conversation).filter(
            Conversation.imam_id == imam.id
        ).order_by(Conversation.updated_at.desc()).all()
    
    return [
        {
            "id": c.id,
            "user_email": c.user_email,
            "imam_id": c.imam_id,
            "imam_name": c.imam.name if c.imam else "Unknown",
            "topic": c.topic,
            "created_at": c.created_at.isoformat(),
            "updated_at": c.updated_at.isoformat(),
            "unread_count": ChatService.get_unread_message_count(db, c.id, "imam")
        }
        for c in conversations
    ]

@router.get("/chat/all-conversations")
def get_all_conversations(db: Session = Depends(get_db)):
    """Get all conversations (for imam dashboard)"""
    from models_extended import Conversation
    
    conversations = db.query(Conversation).order_by(Conversation.updated_at.desc()).all()
    return [
        {
            "id": c.id,
            "user_email": c.user_email,
            "imam_id": c.imam_id,
            "imam_name": c.imam.name if c.imam else "Unknown",
            "topic": c.topic,
            "created_at": c.created_at.isoformat(),
            "updated_at": c.updated_at.isoformat(),
            "unread_count": ChatService.get_unread_message_count(db, c.id, "imam")
        }
        for c in conversations
    ]

@router.put("/chat/messages/{message_id}/read")
def mark_message_read(message_id: int, db: Session = Depends(get_db)):
    """Mark a message as read"""
    from models_extended import Message
    
    message = db.query(Message).filter(Message.id == message_id).first()
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    
    message.is_read = True
    db.commit()
    return {"status": "success", "message_id": message_id}
