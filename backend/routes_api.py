"""

                         RAMADAN HELPER API ROUTES                             
              Organized, Professional REST API Endpoints                       

"""

from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, text, text
from datetime import datetime, timedelta
from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
import logging

from database import SessionLocal
from services_dua import DuaService
from services_chat import ChatService
from services_ai_analyzer import AIAnalyzerService
from services_youtube_ai import YouTubeAIService
from services_email import EmailService
from models_extended import (
    User, DuaHistory, Imam, Conversation, Message,
    Video, AIAnalysis, UserHistory
)

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api")

# 
#                              DATABASE DEPENDENCY
# 

def get_db():
    """Database session dependency"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 
#                              PYDANTIC SCHEMAS
# ═

# Auth Schemas
class SignupRequest(BaseModel):
    email: str = Field(..., description="User email address")
    name: str = Field(..., description="User full name")
    password: str = Field(..., min_length=6, description="Password (min 6 characters)")

class LoginRequest(BaseModel):
    email: str
    password: str

class VerifyEmailRequest(BaseModel):
    email: str
    code: str = Field(..., min_length=6, max_length=6, description="6-digit verification code")

class ResendCodeRequest(BaseModel):
    email: str

class ForgotPasswordRequest(BaseModel):
    email: str

class ResetPasswordRequest(BaseModel):
    email: str
    code: str
    new_password: str = Field(..., min_length=6)

class UpdateProfileRequest(BaseModel):
    name: Optional[str] = None
    current_password: Optional[str] = None
    new_password: Optional[str] = None

# Dua Schemas
class DuaGenerateRequest(BaseModel):
    email: str
    category: str = Field(..., description="Dua category (health, family, success, etc.)")
    context: str = Field(..., description="Your specific situation or context")

class DuaFeedbackRequest(BaseModel):
    dua_id: int
    helpful: bool
    notes: Optional[str] = ""

# Chat Schemas
class ConversationCreateRequest(BaseModel):
    user_email: str
    imam_id: int
    topic: str = Field(..., description="Topic for discussion")

class MessageSendRequest(BaseModel):
    conversation_id: int
    sender_email: str
    sender_type: str = Field(..., pattern="^(user|imam)$")
    message_text: str

# Analyzer Schemas
class AnalyzerRequest(BaseModel):
    email: str
    question: str = Field(..., description="Your question seeking Islamic guidance")

# Video Schemas
class VideoSearchRequest(BaseModel):
    email: str
    prompt: str = Field(..., description="What would you like to learn about?")

# 
#                         AUTHENTICATION ENDPOINTS
# 

@router.post("/auth/signup", tags=["Authentication"], summary="Register new user")
async def signup(request: SignupRequest, db: Session = Depends(get_db)):
    """
    Register a new user account with email verification.
    
    - Sends a 6-digit verification code to the provided email
    - User must verify email before accessing protected features
    """
    existing = db.query(User).filter(User.email == request.email).first()
    
    if existing:
        if existing.is_verified:
            raise HTTPException(400, "Email already registered. Please login.")
        # Update existing unverified user
        existing.verification_code = User.generate_verification_code()
        existing.name = request.name
        existing.password_hash = User.hash_password(request.password)
        db.commit()
        
        email_sent = EmailService.send_verification_email(
            request.email, existing.verification_code, existing.name
        )
        logger.info(f"Resent verification code to: {request.email}")
        
        return {
            "status": "pending_verification",
            "message": "New verification code sent to your email.",
            "email": request.email,
            "email_sent": email_sent
        }
    
    # Create new user
    code = User.generate_verification_code()
    user = User(
        email=request.email,
        name=request.name,
        password_hash=User.hash_password(request.password),
        user_type="user",
        is_verified=False,
        verification_code=code,
        verification_token=User.generate_token()
    )
    db.add(user)
    db.commit()
    
    email_sent = EmailService.send_verification_email(request.email, code, request.name)
    logger.info(f"New user registered: {request.email}")
    
    response = {
        "status": "pending_verification",
        "message": "Account created! Check your email for verification code.",
        "email": request.email,
        "email_sent": email_sent
    }
    
    if not EmailService.is_configured():
        response["verification_code"] = code
        response["message"] = "Demo mode - verification code shown below"
    
    return response

@router.post("/auth/verify", tags=["Authentication"], summary="Verify email")
async def verify_email(request: VerifyEmailRequest, db: Session = Depends(get_db)):
    """Verify user email with 6-digit code"""
    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        raise HTTPException(404, "User not found")
    if user.is_verified:
        return {"status": "already_verified", "message": "Email already verified"}
    if user.verification_code != request.code:
        raise HTTPException(400, "Invalid verification code")
    
    user.is_verified = True
    user.verification_code = None
    db.commit()
    logger.info(f"Email verified: {request.email}")
    
    return {
        "status": "verified",
        "message": "Email verified successfully! You can now login.",
        "user": {"id": user.id, "email": user.email, "name": user.name}
    }

@router.post("/auth/resend-code", tags=["Authentication"], summary="Resend verification code")
async def resend_code(request: ResendCodeRequest, db: Session = Depends(get_db)):
    """Resend email verification code"""
    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        raise HTTPException(404, "User not found")
    if user.is_verified:
        return {"status": "already_verified"}
    
    code = User.generate_verification_code()
    user.verification_code = code
    db.commit()
    
    email_sent = EmailService.send_verification_email(request.email, code, user.name)
    
    response = {"status": "code_sent", "message": "New code sent", "email_sent": email_sent}
    if not EmailService.is_configured():
        response["verification_code"] = code
    return response

@router.post("/auth/login", tags=["Authentication"], summary="User login")
async def login(request: LoginRequest, db: Session = Depends(get_db)):
    """Login with email and password"""
    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        raise HTTPException(404, "Account not found. Please sign up.")
    if not user.password_hash:
        raise HTTPException(400, "Password not set. Please sign up again.")
    if not user.verify_password(request.password):
        raise HTTPException(401, "Invalid password")
    if not user.is_verified:
        raise HTTPException(403, "Email not verified. Check your email for code.")
    
    logger.info(f"User logged in: {request.email}")
    return {
        "status": "success",
        "user": {
            "id": user.id,
            "email": user.email,
            "name": user.name,
            "user_type": user.user_type
        }
    }

@router.post("/auth/forgot-password", tags=["Authentication"], summary="Request password reset")
async def forgot_password(request: ForgotPasswordRequest, db: Session = Depends(get_db)):
    """Request password reset code"""
    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        # Don't reveal if email exists
        return {"status": "sent", "message": "If email exists, reset code sent"}
    
    code = User.generate_verification_code()
    user.reset_token = code
    db.commit()
    
    # Send reset email
    email_sent = EmailService.send_password_reset_email(request.email, code, user.name)
    
    response = {"status": "sent", "message": "Reset code sent to email", "email_sent": email_sent}
    if not EmailService.is_configured():
        response["reset_code"] = code
    return response

@router.post("/auth/reset-password", tags=["Authentication"], summary="Reset password")
async def reset_password(request: ResetPasswordRequest, db: Session = Depends(get_db)):
    """Reset password with code"""
    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        raise HTTPException(404, "User not found")
    if user.reset_token != request.code:
        raise HTTPException(400, "Invalid reset code")
    
    user.password_hash = User.hash_password(request.new_password)
    user.reset_token = None
    db.commit()
    
    logger.info(f"Password reset: {request.email}")
    return {"status": "success", "message": "Password reset successfully"}

# 
#                              USER ENDPOINTS
# 

@router.get("/users/{email}", tags=["Users"], summary="Get user profile")
async def get_user(email: str, db: Session = Depends(get_db)):
    """Get user profile by email"""
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(404, "User not found")
    return {
        "id": user.id,
        "email": user.email,
        "name": user.name,
        "user_type": user.user_type,
        "is_verified": user.is_verified,
        "created_at": user.created_at.isoformat() if user.created_at else None
    }

@router.put("/users/{email}", tags=["Users"], summary="Update user profile")
async def update_user(email: str, request: UpdateProfileRequest, db: Session = Depends(get_db)):
    """Update user profile"""
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(404, "User not found")
    
    if request.name:
        user.name = request.name
    
    if request.new_password:
        if not request.current_password:
            raise HTTPException(400, "Current password required")
        if not user.verify_password(request.current_password):
            raise HTTPException(401, "Invalid current password")
        user.password_hash = User.hash_password(request.new_password)
    
    db.commit()
    return {"status": "updated", "message": "Profile updated successfully"}

@router.delete("/users/{email}", tags=["Users"], summary="Delete user account")
async def delete_user(email: str, db: Session = Depends(get_db)):
    """Delete user account and all associated data"""
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(404, "User not found")
    
    # Delete associated data
    db.query(DuaHistory).filter(DuaHistory.email == email).delete()
    db.query(UserHistory).filter(UserHistory.user_email == email).delete()
    db.query(Conversation).filter(Conversation.user_email == email).delete()
    db.delete(user)
    db.commit()
    
    logger.info(f"User deleted: {email}")
    return {"status": "deleted", "message": "Account deleted successfully"}

# 
#                              DUA ENDPOINTS
# 

@router.get("/dua/categories", tags=["Dua"], summary="Get dua categories")
async def get_dua_categories():
    """Get all available dua categories"""
    return {"categories": DuaService.get_categories()}

@router.post("/dua/generate", tags=["Dua"], summary="Generate personalized dua")
async def generate_dua(request: DuaGenerateRequest, db: Session = Depends(get_db)):
    """
    Generate a personalized dua using AI based on your situation.
    
    Returns both Arabic and English text with guidance on usage.
    """
    try:
        dua_data = await DuaService.generate_dua_with_ai(request.category, request.context)
    except Exception as e:
        logger.error(f"AI dua generation failed: {e}")
        dua_data = DuaService.generate_dua(request.category, request.context)
    
    saved = DuaService.save_dua_to_history(db, request.email, dua_data)
    
    return {
        "id": saved.id,
        "category": dua_data["category"],
        "context": dua_data["context"],
        "dua_text_en": dua_data["dua_text_en"],
        "dua_text_ar": dua_data["dua_text_ar"],
        "how_to_use_en": dua_data.get("how_to_use_en", ""),
        "how_to_use_ar": dua_data.get("how_to_use_ar", ""),
        "ai_generated": dua_data.get("ai_generated", False),
        "timestamp": datetime.now().isoformat()
    }

@router.get("/dua/history/{email}", tags=["Dua"], summary="Get dua history")
async def get_dua_history(email: str, limit: int = Query(50, le=100), db: Session = Depends(get_db)):
    """Get user's dua generation history"""
    duas = DuaService.get_user_history(db, email)[:limit]
    return {"count": len(duas), "duas": duas}

@router.post("/dua/feedback", tags=["Dua"], summary="Submit dua feedback")
async def submit_dua_feedback(request: DuaFeedbackRequest, db: Session = Depends(get_db)):
    """Submit feedback on a generated dua"""
    dua = DuaService.submit_feedback(db, request.dua_id, request.helpful, request.notes)
    if not dua:
        raise HTTPException(404, "Dua not found")
    return {"status": "success", "message": "Feedback submitted"}

# 
#                              CHAT ENDPOINTS
# 

@router.get("/chat/imams", tags=["Chat"], summary="Get available imams")
async def get_imams(db: Session = Depends(get_db)):
    """Get list of available Islamic scholars"""
    imams = ChatService.get_all_imams(db)
    return {
        "count": len(imams),
        "imams": [
            {
                "id": i.id,
                "name": i.name,
                "expertise": i.expertise,
                "is_available": i.is_available,
                "bio": i.bio
            } for i in imams
        ]
    }

@router.get("/chat/imams/{imam_id}", tags=["Chat"], summary="Get imam details")
async def get_imam(imam_id: int, db: Session = Depends(get_db)):
    """Get specific imam details"""
    imam = ChatService.get_imam_by_id(db, imam_id)
    if not imam:
        raise HTTPException(404, "Imam not found")
    return {
        "id": imam.id,
        "name": imam.name,
        "email": imam.email,
        "expertise": imam.expertise,
        "is_available": imam.is_available,
        "bio": imam.bio
    }

@router.post("/chat/conversations", tags=["Chat"], summary="Start conversation")
async def create_conversation(request: ConversationCreateRequest, db: Session = Depends(get_db)):
    """Start a new conversation with an imam"""
    try:
        conv = ChatService.create_conversation(db, request.user_email, request.imam_id, request.topic)
        return {
            "id": conv.id,
            "user_email": conv.user_email,
            "imam_id": conv.imam_id,
            "topic": conv.topic,
            "created_at": conv.created_at.isoformat()
        }
    except ValueError as e:
        raise HTTPException(400, str(e))

@router.get("/chat/conversations/{user_email}", tags=["Chat"], summary="Get user conversations")
async def get_conversations(user_email: str, db: Session = Depends(get_db)):
    """Get all conversations for a user"""
    convs = ChatService.get_user_conversations(db, user_email)
    return {
        "count": len(convs),
        "conversations": [
            {
                "id": c.id,
                "imam_id": c.imam_id,
                "imam_name": c.imam.name if c.imam else "Unknown",
                "topic": c.topic,
                "created_at": c.created_at.isoformat(),
                "updated_at": c.updated_at.isoformat()
            } for c in convs
        ]
    }

@router.post("/chat/messages", tags=["Chat"], summary="Send message")
async def send_message(request: MessageSendRequest, db: Session = Depends(get_db)):
    """Send a message in a conversation"""
    try:
        msg = ChatService.send_message(
            db, request.conversation_id, request.sender_email,
            request.sender_type, request.message_text
        )
        
        # Auto-reply from imam if user sent message
        if request.sender_type == "user":
            conv = db.query(Conversation).filter(Conversation.id == request.conversation_id).first()
            if conv and conv.imam:
                reply = ChatService.generate_imam_response(request.message_text, conv.imam.name)
                ChatService.send_message(db, request.conversation_id, conv.imam.email, "imam", reply)
        
        return {
            "id": msg.id,
            "conversation_id": msg.conversation_id,
            "sender_type": msg.sender_type,
            "message_text": msg.message_text,
            "created_at": msg.created_at.isoformat()
        }
    except ValueError as e:
        raise HTTPException(400, str(e))

@router.get("/chat/messages/{conversation_id}", tags=["Chat"], summary="Get messages")
async def get_messages(conversation_id: int, db: Session = Depends(get_db)):
    """Get all messages in a conversation"""
    msgs = ChatService.get_conversation_messages(db, conversation_id)
    return {
        "count": len(msgs),
        "messages": [
            {
                "id": m.id,
                "sender_type": m.sender_type,
                "sender_email": m.sender_email,
                "message_text": m.message_text,
                "is_read": m.is_read,
                "created_at": m.created_at.isoformat()
            } for m in msgs
        ]
    }

# 
#                           AI ANALYZER ENDPOINTS
# 

@router.post("/analyzer/analyze", tags=["AI Analyzer"], summary="Analyze question")
async def analyze_question(request: AnalyzerRequest, db: Session = Depends(get_db)):
    """
    Analyze your question and get relevant Quran verses and Hadiths.
    
    AI matches your question to the most relevant Islamic guidance.
    """
    # Try enhanced method with full Quran API first
    try:
        result = await AIAnalyzerService.analyze_with_full_quran(request.question)
    except Exception as e:
        logger.error(f"Full Quran analysis failed: {e}")
        result = await AIAnalyzerService.analyze_prompt_with_ai(request.question)
    
    # Log analysis
    try:
        analysis = AIAnalysis(
            user_email=request.email,
            question=request.question,
            ayah=result.get("ayah"),
            hadith=result.get("hadith"),
            explanation=result.get("ai_explanation", "")
        )
        db.add(analysis)
        db.commit()
    except Exception as e:
        logger.error(f"Failed to log analysis: {e}")
    
    return result

@router.get("/analyzer/topics", tags=["AI Analyzer"], summary="Get available topics")
async def get_analyzer_topics():
    """Get list of topics the AI can provide guidance on"""
    return {
        "topics": AIAnalyzerService.AVAILABLE_TOPICS,
        "count": len(AIAnalyzerService.AVAILABLE_TOPICS)
    }

@router.get("/analyzer/ayahs", tags=["AI Analyzer"], summary="Get all Quran verses")
async def get_all_ayahs():
    """Get all Quranic verses in the database"""
    return {
        "count": len(AIAnalyzerService.QURAN_AYAHS),
        "ayahs": AIAnalyzerService.QURAN_AYAHS
    }

@router.get("/analyzer/hadiths", tags=["AI Analyzer"], summary="Get all Hadiths")
async def get_all_hadiths():
    """Get all Hadiths in the database"""
    return {
        "count": len(AIAnalyzerService.HADITHS),
        "hadiths": AIAnalyzerService.HADITHS
    }

# 
#                              VIDEO ENDPOINTS
# 

@router.post("/videos/search", tags=["Videos"], summary="Search Islamic videos")
async def search_videos(request: VideoSearchRequest, db: Session = Depends(get_db)):
    """
    Search for Islamic educational videos on YouTube.
    
    AI generates relevant search terms based on your question.
    """
    try:
        service = YouTubeAIService()
        result = await service.search_personalized_videos(request.prompt, max_results=6)
        return result
    except Exception as e:
        logger.error(f"Video search failed: {e}")
        raise HTTPException(500, f"Video search failed: {str(e)}")

# 
#                          STATISTICS ENDPOINTS
# 

@router.get("/stats/dashboard", tags=["Statistics"], summary="Get dashboard stats")
async def get_dashboard_stats(db: Session = Depends(get_db)):
    """Get overall platform statistics"""
    users = db.query(User).count()
    verified = db.query(User).filter(User.is_verified == True).count()
    duas = db.query(DuaHistory).count()
    conversations = db.query(Conversation).count()
    messages = db.query(Message).count()
    analyses = db.query(AIAnalysis).count()
    
    # Recent activity (last 7 days)
    week_ago = datetime.now() - timedelta(days=7)
    recent_users = db.query(User).filter(User.created_at >= week_ago).count()
    recent_duas = db.query(DuaHistory).filter(DuaHistory.created_at >= week_ago).count()
    
    return {
        "totals": {
            "users": users,
            "verified_users": verified,
            "duas_generated": duas,
            "conversations": conversations,
            "messages": messages,
            "ai_analyses": analyses
        },
        "last_7_days": {
            "new_users": recent_users,
            "duas_generated": recent_duas
        },
        "timestamp": datetime.now().isoformat()
    }

@router.get("/stats/user/{email}", tags=["Statistics"], summary="Get user stats")
async def get_user_stats(email: str, db: Session = Depends(get_db)):
    """Get statistics for a specific user"""
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(404, "User not found")
    
    duas = db.query(DuaHistory).filter(DuaHistory.email == email).count()
    conversations = db.query(Conversation).filter(Conversation.user_email == email).count()
    analyses = db.query(AIAnalysis).filter(AIAnalysis.user_email == email).count()
    
    # Get favorite dua category
    fav_category = db.query(DuaHistory.category, func.count(DuaHistory.id).label('count'))\
        .filter(DuaHistory.email == email)\
        .group_by(DuaHistory.category)\
        .order_by(func.count(DuaHistory.id).desc())\
        .first()
    
    return {
        "user": {
            "email": email,
            "name": user.name,
            "member_since": user.created_at.isoformat() if user.created_at else None
        },
        "activity": {
            "duas_generated": duas,
            "conversations": conversations,
            "ai_analyses": analyses,
            "favorite_category": fav_category[0] if fav_category else None
        }
    }

# 
#                              HEALTH CHECK
# 

@router.get("/health", tags=["System"], summary="Health check")
async def health_check(db: Session = Depends(get_db)):
    """Check API and database health"""
    try:
        db.execute(text("SELECT 1"))
        db_status = "connected"
    except:
        db_status = "disconnected"
    
    return {
        "status": "healthy" if db_status == "connected" else "degraded",
        "api": "running",
        "database": db_status,
        "version": "2.0.0",
        "timestamp": datetime.now().isoformat()
    }

# 
#                         LEGACY COMPATIBILITY ROUTES
# 
# These routes maintain backward compatibility with existing frontend

@router.post("/users/signup", tags=["Legacy"], include_in_schema=False)
async def legacy_signup(request: SignupRequest, db: Session = Depends(get_db)):
    return await signup(request, db)

@router.post("/users/verify", tags=["Legacy"], include_in_schema=False)
async def legacy_verify(request: VerifyEmailRequest, db: Session = Depends(get_db)):
    return await verify_email(request, db)

@router.post("/users/resend-code", tags=["Legacy"], include_in_schema=False)
async def legacy_resend(request: ResendCodeRequest, db: Session = Depends(get_db)):
    return await resend_code(request, db)

@router.post("/users/login", tags=["Legacy"], include_in_schema=False)
async def legacy_login(request: LoginRequest, db: Session = Depends(get_db)):
    return await login(request, db)



