"""
Complete API Routes with JWT Authentication for myRamadan
Includes: Auth, Users, Dua, Chat, AI Analyzer, Videos, Events, History
"""
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
import os

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

# ============= JWT CONFIG =============
SECRET_KEY = os.getenv("SECRET_KEY", "ramadan-helper-secret-key-2026-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440  # 24 hours

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token")

# ============= DATABASE DEPENDENCY =============
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ============= PYDANTIC MODELS =============
class Token(BaseModel):
    access_token: str
    token_type: str
    user_email: str
    user_name: str
    user_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
    user_type: Optional[str] = None

class UserSignupRequest(BaseModel):
    email: EmailStr
    name: str
    password: str
    user_type: str = "user"

class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: str
    name: Optional[str]
    user_type: str
    is_verified: bool = True
    class Config:
        from_attributes = True

class DuaGenerateRequest(BaseModel):
    category: str
    context: str
    email: Optional[str] = None

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
    imam_id: int
    topic: str
    user_email: Optional[str] = None  # Email for non-auth users

class MessageSendRequest(BaseModel):
    conversation_id: int
    message_text: str
    sender_email: Optional[str] = None  # Email for non-auth users
    sender_type: Optional[str] = "user"  # "user" or "imam"

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

class AnalyzeRequest(BaseModel):
    question: str
    email: Optional[str] = None

class VideoSearchRequest(BaseModel):
    prompt: str

class EventCreateRequest(BaseModel):
    title: str
    description: str
    city: str
    location: str
    category: str
    event_date: str
    event_time: str
    contact_phone: Optional[str] = None
    listing_type: str = "basic"  # basic (20 TND) or featured (50 TND)

class EventResponse(BaseModel):
    id: int
    title: str
    description: str
    city: str
    location: str
    category: str
    event_date: str
    event_time: str
    organizer_email: str
    organizer_name: str
    contact_phone: Optional[str]
    is_featured: bool
    listing_type: str
    price: int
    created_at: str
    class Config:
        from_attributes = True

# ============= AUTH HELPER FUNCTIONS =============
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        user_type: str = payload.get("user_type", "user")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email, user_type=user_type)
    except JWTError:
        raise credentials_exception
    
    user = db.query(User).filter(User.email == token_data.email).first()
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    return current_user

async def get_current_imam(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> User:
    if current_user.user_type != "imam":
        raise HTTPException(status_code=403, detail="Access denied. Imam role required.")
    return current_user

# ============= AUTH ENDPOINTS =============
@router.post("/auth/signup", response_model=UserResponse)
async def signup(request: UserSignupRequest, db: Session = Depends(get_db)):
    """Register a new user"""
    existing = db.query(User).filter(User.email == request.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = get_password_hash(request.password)
    user = User(
        email=request.email,
        name=request.name,
        password_hash=hashed_password,
        user_type=request.user_type
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.post("/auth/login", response_model=Token)
async def login(request: UserLoginRequest, db: Session = Depends(get_db)):
    """Login and get JWT token"""
    user = db.query(User).filter(User.email == request.email).first()
    
    # For demo: if user doesn't exist, create them
    if not user:
        hashed_password = get_password_hash(request.password)
        user = User(
            email=request.email,
            name=request.email.split("@")[0],
            password_hash=hashed_password,
            user_type="user"
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    elif user.password_hash and not verify_password(request.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Incorrect password")
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email, "user_type": user.user_type},
        expires_delta=access_token_expires
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_email": user.email,
        "user_name": user.name or user.email.split("@")[0],
        "user_type": user.user_type
    }

@router.post("/auth/token", response_model=Token)
async def token_for_swagger(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """OAuth2 compatible token endpoint for Swagger UI"""
    user = db.query(User).filter(User.email == form_data.username).first()
    
    if not user:
        hashed_password = get_password_hash(form_data.password)
        user = User(
            email=form_data.username,
            name=form_data.username.split("@")[0],
            password_hash=hashed_password,
            user_type="user"
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    elif user.password_hash and not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Incorrect password")
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email, "user_type": user.user_type},
        expires_delta=access_token_expires
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_email": user.email,
        "user_name": user.name or "",
        "user_type": user.user_type
    }

# ============= USER ENDPOINTS =============
@router.get("/users/me", response_model=UserResponse)
async def get_current_user_profile(current_user: User = Depends(get_current_active_user)):
    """🔒 Get current user profile"""
    return current_user

@router.get("/users/{email}", response_model=UserResponse)
async def get_user_by_email(email: str, current_user: User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    """🔒 Get user by email"""
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# ============= DUA ENDPOINTS =============
@router.get("/dua/categories")
async def get_dua_categories():
    """Get all dua categories"""
    return {
        "categories": [
            "Fear & Anxiety", "Financial Hardship", "Health Issues",
            "Family Problems", "Career Guidance", "Spiritual Growth",
            "Relationship Issues", "Gratitude", "Protection", "Forgiveness"
        ]
    }

@router.post("/dua/generate")
async def generate_dua(request: DuaGenerateRequest, db: Session = Depends(get_db)):
    """Generate a personalized dua (no auth required)"""
    try:
        dua_service = DuaService()
        result = await dua_service.generate_dua(request.category, request.context)
        
        # Save to history
        user_email = request.email or 'guest@app.local'
        history = DuaHistory(
            email=user_email,
            category=request.category,
            context=request.context,
            dua_text_en=result.get("dua_text_en", ""),
            dua_text_ar=result.get("dua_text_ar", ""),
            how_to_use_en=result.get("how_to_use_en", ""),
            how_to_use_ar=result.get("how_to_use_ar", "")
        )
        db.add(history)
        db.commit()
        db.refresh(history)
        
        return {
            "id": history.id,
            "category": request.category,
            "context": request.context,
            **result,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/dua/history")
async def get_dua_history(current_user: User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    """🔒 Get current user's dua history"""
    history = db.query(DuaHistory).filter(DuaHistory.email == current_user.email).order_by(DuaHistory.created_at.desc()).all()
    return {"history": [{"id": h.id, "category": h.category, "context": h.context, "dua_text_en": h.dua_text_en, "dua_text_ar": h.dua_text_ar, "created_at": str(h.created_at)} for h in history]}

# ============= CHAT ENDPOINTS =============
@router.get("/chat/imams", response_model=List[ImamResponse])
async def get_all_imams(db: Session = Depends(get_db)):
    """Get all available imams"""
    imams = db.query(Imam).filter(Imam.is_available == True).all()
    if not imams:
        # Create default imams
        default_imams = [
            Imam(name="Sheikh Ahmad Al-Rashid", email="sheikh.ahmad@mosque.com", expertise="Fiqh & Islamic Jurisprudence", bio="20+ years of Islamic scholarship", is_available=True),
            Imam(name="Imam Muhammad Hassan", email="imam.hassan@mosque.com", expertise="Quran Interpretation & Tafsir", bio="Specialist in Quranic studies", is_available=True),
        ]
        for imam in default_imams:
            db.add(imam)
        db.commit()
        imams = db.query(Imam).all()
    return imams

@router.post("/chat/conversations")
async def create_conversation(request: ConversationCreateRequest, db: Session = Depends(get_db)):
    """Create a new conversation with an imam (public - no auth required)"""
    imam = db.query(Imam).filter(Imam.id == request.imam_id).first()
    if not imam:
        raise HTTPException(status_code=404, detail="Imam not found")
    
    user_email = request.user_email or "guest@app.local"
    
    conversation = Conversation(
        user_email=user_email,
        imam_id=request.imam_id,
        topic=request.topic
    )
    db.add(conversation)
    db.commit()
    db.refresh(conversation)
    return {"id": conversation.id, "user_email": user_email, "imam_id": request.imam_id, "topic": request.topic, "created_at": str(conversation.created_at)}

@router.get("/chat/conversations/{user_email}")
async def get_user_conversations(user_email: str, db: Session = Depends(get_db)):
    """Get conversations for a user by email (public)"""
    conversations = db.query(Conversation).filter(Conversation.user_email == user_email).order_by(Conversation.updated_at.desc()).all()
    result = []
    for conv in conversations:
        imam = db.query(Imam).filter(Imam.id == conv.imam_id).first()
        # Get unread count
        unread_count = db.query(Message).filter(
            Message.conversation_id == conv.id,
            Message.sender_type == "imam",
            Message.is_read == False
        ).count()
        result.append({
            "id": conv.id,
            "imam_id": conv.imam_id,
            "imam_name": imam.name if imam else "Unknown",
            "topic": conv.topic,
            "unread_count": unread_count,
            "created_at": str(conv.created_at),
            "updated_at": str(conv.updated_at)
        })
    return result

@router.post("/chat/messages")
async def send_message(request: MessageSendRequest, db: Session = Depends(get_db)):
    """Send a message in a conversation (public - no auth required)"""
    conversation = db.query(Conversation).filter(Conversation.id == request.conversation_id).first()
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    sender_email = request.sender_email or "guest@app.local"
    sender_type = request.sender_type or "user"
    
    message = Message(
        conversation_id=request.conversation_id,
        sender_email=sender_email,
        sender_type=sender_type,
        message_text=request.message_text
    )
    db.add(message)
    
    # Update conversation timestamp
    conversation.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(message)
    return {"id": message.id, "conversation_id": message.conversation_id, "sender_type": message.sender_type, "message_text": message.message_text, "created_at": str(message.created_at)}

@router.get("/chat/messages/{conversation_id}")
async def get_messages(conversation_id: int, db: Session = Depends(get_db)):
    """Get messages in a conversation (public)"""
    messages = db.query(Message).filter(Message.conversation_id == conversation_id).order_by(Message.created_at).all()
    return {"messages": [{"id": m.id, "sender_type": m.sender_type, "sender_email": m.sender_email, "message_text": m.message_text, "is_read": m.is_read, "created_at": str(m.created_at)} for m in messages]}

@router.put("/chat/messages/{conversation_id}/read")
async def mark_messages_read(conversation_id: int, reader_type: str = "user", db: Session = Depends(get_db)):
    """Mark messages as read when user/imam opens conversation"""
    # Mark messages from the other party as read
    other_type = "imam" if reader_type == "user" else "user"
    db.query(Message).filter(
        Message.conversation_id == conversation_id,
        Message.sender_type == other_type
    ).update({"is_read": True})
    db.commit()
    return {"success": True}

@router.get("/chat/all-conversations")
async def get_all_conversations(db: Session = Depends(get_db)):
    """Get all conversations (for Imam dashboard - public)"""
    conversations = db.query(Conversation).order_by(Conversation.updated_at.desc()).all()
    result = []
    for conv in conversations:
        imam = db.query(Imam).filter(Imam.id == conv.imam_id).first()
        last_message = db.query(Message).filter(Message.conversation_id == conv.id).order_by(Message.created_at.desc()).first()
        # Count unread messages from users
        unread_count = db.query(Message).filter(
            Message.conversation_id == conv.id,
            Message.sender_type == "user",
            Message.is_read == False
        ).count()
        result.append({
            "id": conv.id,
            "user_email": conv.user_email,
            "imam_id": conv.imam_id,
            "imam_name": imam.name if imam else "Unknown",
            "topic": conv.topic,
            "last_message": last_message.message_text[:50] if last_message else None,
            "unread_count": unread_count,
            "created_at": str(conv.created_at),
            "updated_at": str(conv.updated_at)
        })
    return result

@router.get("/chat/imam-conversations/{imam_email}")
async def get_imam_conversations(imam_email: str, db: Session = Depends(get_db)):
    """Get conversations for a specific imam by email"""
    imam = db.query(Imam).filter(Imam.email == imam_email).first()
    if not imam:
        return []
    
    conversations = db.query(Conversation).filter(Conversation.imam_id == imam.id).order_by(Conversation.updated_at.desc()).all()
    result = []
    for conv in conversations:
        last_message = db.query(Message).filter(Message.conversation_id == conv.id).order_by(Message.created_at.desc()).first()
        # Count unread messages from users
        unread_count = db.query(Message).filter(
            Message.conversation_id == conv.id,
            Message.sender_type == "user",
            Message.is_read == False
        ).count()
        result.append({
            "id": conv.id,
            "user_email": conv.user_email,
            "imam_id": conv.imam_id,
            "imam_name": imam.name,
            "topic": conv.topic,
            "last_message": last_message.message_text[:50] if last_message else None,
            "unread_count": unread_count,
            "created_at": str(conv.created_at),
            "updated_at": str(conv.updated_at)
        })
    return result

# ============= AI ANALYZER ENDPOINTS =============
@router.post("/analyzer/analyze")
async def analyze_question(request: AnalyzeRequest, db: Session = Depends(get_db)):
    """Analyze question with semantic search (no auth required)"""
    try:
        analyzer = AIAnalyzerService()
        result = await analyzer.analyze(request.question)
        
        # Save analysis if email provided
        user_email = request.email or 'guest@app.local'
        analysis = AIAnalysis(
            user_email=user_email,
            question=request.question,
            ayah=result.get("ayah", {}),
            hadith=result.get("hadith", {}),
            explanation=result.get("ai_explanation", "")
        )
        db.add(analysis)
        db.commit()
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/analyzer/topics")
async def get_analyzer_topics():
    """Get available topics for analysis"""
    return {
        "topics": [
            "Prayer", "Fasting", "Charity", "Pilgrimage", "Faith",
            "Family", "Marriage", "Business", "Ethics", "Patience",
            "Gratitude", "Repentance", "Forgiveness", "Anxiety", "Health"
        ]
    }

# ============= VIDEO ENDPOINTS =============
@router.post("/videos/search")
async def search_videos(request: VideoSearchRequest, current_user: User = Depends(get_current_active_user)):
    """🔒 AI-powered video search"""
    try:
        youtube_service = YouTubeAIService()
        videos = await youtube_service.search_videos(request.prompt)
        return {"videos": videos}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============= EVENTS ENDPOINTS (Tunisia) =============
TUNISIA_CITIES = [
    "Tunis", "Sfax", "Sousse", "Kairouan", "Bizerte",
    "Gabès", "Ariana", "Gafsa", "Monastir", "Ben Arous",
    "Kasserine", "Médenine", "Nabeul", "Tataouine", "Béja",
    "Jendouba", "Mahdia", "Sidi Bouzid", "Tozeur", "Siliana",
    "Kébili", "Zaghouan", "Manouba", "Le Kef"
]

EVENT_CATEGORIES = ["iftar", "tarawih", "charity", "lecture", "quran", "children", "other"]

# In-memory events storage (would be database in production)
events_db = []
event_id_counter = 1

@router.get("/events")
async def get_events(city: Optional[str] = None, category: Optional[str] = None):
    """Get all events with optional filters"""
    filtered = events_db.copy()
    if city:
        filtered = [e for e in filtered if e["city"].lower() == city.lower()]
    if category:
        filtered = [e for e in filtered if e["category"].lower() == category.lower()]
    return {"events": filtered, "total": len(filtered)}

@router.get("/events/cities")
async def get_cities():
    """Get all Tunisia cities"""
    return {"cities": TUNISIA_CITIES}

@router.get("/events/categories")
async def get_event_categories():
    """Get event categories"""
    return {"categories": EVENT_CATEGORIES}

@router.get("/events/featured")
async def get_featured_events():
    """Get featured/premium events"""
    featured = [e for e in events_db if e["is_featured"]]
    return {"events": featured, "total": len(featured)}

@router.post("/events")
async def create_event(request: EventCreateRequest, current_user: User = Depends(get_current_active_user)):
    """🔒 Create a new event"""
    global event_id_counter
    
    is_featured = request.listing_type == "featured"
    price = 50 if is_featured else 20
    
    event = {
        "id": event_id_counter,
        "title": request.title,
        "description": request.description,
        "city": request.city,
        "location": request.location,
        "category": request.category,
        "event_date": request.event_date,
        "event_time": request.event_time,
        "organizer_email": current_user.email,
        "organizer_name": current_user.name or current_user.email.split("@")[0],
        "contact_phone": request.contact_phone,
        "is_featured": is_featured,
        "listing_type": request.listing_type,
        "price": price,
        "created_at": datetime.now().isoformat()
    }
    events_db.append(event)
    event_id_counter += 1
    return event

@router.get("/events/my-events")
async def get_my_events(current_user: User = Depends(get_current_active_user)):
    """🔒 Get current user's events"""
    my_events = [e for e in events_db if e["organizer_email"] == current_user.email]
    return {"events": my_events, "total": len(my_events)}

@router.delete("/events/{event_id}")
async def delete_event(event_id: int, current_user: User = Depends(get_current_active_user)):
    """🔒 Delete an event"""
    global events_db
    event = next((e for e in events_db if e["id"] == event_id), None)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    if event["organizer_email"] != current_user.email:
        raise HTTPException(status_code=403, detail="Not authorized to delete this event")
    events_db = [e for e in events_db if e["id"] != event_id]
    return {"message": "Event deleted successfully"}

# ============= HEALTH CHECK =============
@router.get("/health")
async def health_check():
    """Check API health status"""
    return {
        "status": "healthy",
        "message": "myRamadan API is running",
        "timestamp": datetime.now().isoformat(),
        "features": ["JWT Auth", "Dua Generator", "AI Analyzer", "Chat with Imam", "Events (Tunisia)"]
    }
