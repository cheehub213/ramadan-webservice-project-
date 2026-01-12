"""
Chat with Imam Routes - Protected endpoints requiring authentication
"""
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List

from database import SessionLocal
from models_extended import Imam, Conversation, Message, User
from schemas.chat import (
    ImamResponse, ConversationCreateRequest, MessageSendRequest, MessageResponse
)
from .auth import get_current_user, get_current_user_optional

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/imams", response_model=List[ImamResponse])
async def get_all_imams(db: Session = Depends(get_db)):
    """Get all available imams (public)"""
    imams = db.query(Imam).filter(Imam.is_available == True).all()
    
    # Create default imams if none exist
    if not imams:
        default_imams = [
            Imam(
                name="Imam Ahmad",
                email="imam.ahmad@mosque.local",
                expertise="Quran & Islamic Law",
                bio="Expert in Quranic interpretation and Islamic jurisprudence",
                is_available=True
            ),
            Imam(
                name="Imam Mohammed",
                email="imam.mohammed@mosque.local",
                expertise="Hadith & Islamic History",
                bio="Specialist in authentic hadith and Islamic history",
                is_available=True
            ),
            Imam(
                name="Imam Fatima",
                email="imam.fatima@mosque.local",
                expertise="Women's Islamic Issues",
                bio="Expert in women's issues in Islam and family matters",
                is_available=True
            ),
        ]
        for imam in default_imams:
            db.add(imam)
        db.commit()
        imams = db.query(Imam).all()
    
    return imams


@router.post("/conversations")
async def create_conversation(
    request: ConversationCreateRequest, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new conversation with an imam (requires authentication)"""
    imam = db.query(Imam).filter(Imam.id == request.imam_id).first()
    if not imam:
        raise HTTPException(status_code=404, detail="Imam not found")
    
    # Use authenticated user's email
    user_email = current_user.email
    
    conversation = Conversation(
        user_email=user_email,
        imam_id=request.imam_id,
        topic=request.topic
    )
    db.add(conversation)
    db.commit()
    db.refresh(conversation)
    
    return {
        "id": conversation.id,
        "user_email": user_email,
        "imam_id": request.imam_id,
        "topic": request.topic,
        "created_at": str(conversation.created_at)
    }


@router.get("/conversations/{user_email}")
async def get_user_conversations(
    user_email: str, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get conversations for a user by email (requires authentication, users can only access their own)"""
    # Users can only access their own conversations, admins/imams can access any
    if current_user.user_type not in ["admin", "imam"] and current_user.email != user_email:
        raise HTTPException(status_code=403, detail="Access denied. You can only view your own conversations.")
    
    conversations = db.query(Conversation).filter(
        Conversation.user_email == user_email
    ).order_by(Conversation.updated_at.desc()).all()
    
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


@router.get("/imam-conversations/{imam_email}")
async def get_imam_conversations(
    imam_email: str, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get conversations for a specific imam by email (requires imam or admin)"""
    # Only imams can access their own conversations, admins can access any
    if current_user.user_type == "imam" and current_user.email != imam_email:
        raise HTTPException(status_code=403, detail="Access denied. You can only view your own conversations.")
    elif current_user.user_type not in ["admin", "imam"]:
        raise HTTPException(status_code=403, detail="Access denied. Imam or admin role required.")
    
    imam = db.query(Imam).filter(Imam.email == imam_email).first()
    if not imam:
        return []
    
    conversations = db.query(Conversation).filter(
        Conversation.imam_id == imam.id
    ).order_by(Conversation.updated_at.desc()).all()
    
    result = []
    for conv in conversations:
        last_message = db.query(Message).filter(
            Message.conversation_id == conv.id
        ).order_by(Message.created_at.desc()).first()
        
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


@router.get("/all-conversations")
async def get_all_conversations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all conversations (requires imam or admin role)"""
    if current_user.user_type not in ["admin", "imam"]:
        raise HTTPException(status_code=403, detail="Access denied. Imam or admin role required.")
    
    conversations = db.query(Conversation).order_by(Conversation.updated_at.desc()).all()
    
    result = []
    for conv in conversations:
        imam = db.query(Imam).filter(Imam.id == conv.imam_id).first()
        last_message = db.query(Message).filter(
            Message.conversation_id == conv.id
        ).order_by(Message.created_at.desc()).first()
        
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


@router.post("/messages")
async def send_message(
    request: MessageSendRequest, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Send a message in a conversation (requires authentication)"""
    conversation = db.query(Conversation).filter(
        Conversation.id == request.conversation_id
    ).first()
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    # Verify user has access to this conversation
    is_participant = (
        conversation.user_email == current_user.email or
        current_user.user_type in ["admin", "imam"]
    )
    if not is_participant:
        raise HTTPException(status_code=403, detail="Access denied. Not a participant in this conversation.")
    
    sender_email = current_user.email
    sender_type = "imam" if current_user.user_type == "imam" else "user"
    
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
    
    return {
        "id": message.id,
        "conversation_id": message.conversation_id,
        "sender_type": message.sender_type,
        "message_text": message.message_text,
        "created_at": str(message.created_at)
    }


@router.get("/messages/{conversation_id}")
async def get_messages(
    conversation_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get messages in a conversation (requires authentication)"""
    conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    # Verify user has access to this conversation
    is_participant = (
        conversation.user_email == current_user.email or
        current_user.user_type in ["admin", "imam"]
    )
    if not is_participant:
        raise HTTPException(status_code=403, detail="Access denied. Not a participant in this conversation.")
    
    messages = db.query(Message).filter(
        Message.conversation_id == conversation_id
    ).order_by(Message.created_at).all()

    return {
        "messages": [
            {
                "id": m.id,
                "sender_type": m.sender_type,
                "sender_email": m.sender_email,
                "message_text": m.message_text,
                "is_read": m.is_read,
                "created_at": str(m.created_at)
            }
            for m in messages
        ]
    }


@router.put("/messages/{conversation_id}/read")
async def mark_messages_read(
    conversation_id: int, 
    reader_type: str = "user", 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Mark messages as read when user/imam opens conversation (requires authentication)"""
    conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    # Verify user has access to this conversation
    is_participant = (
        conversation.user_email == current_user.email or
        current_user.user_type in ["admin", "imam"]
    )
    if not is_participant:
        raise HTTPException(status_code=403, detail="Access denied. Not a participant in this conversation.")
    
    # Mark messages from the other party as read
    other_type = "imam" if reader_type == "user" else "user"
    db.query(Message).filter(
        Message.conversation_id == conversation_id,
        Message.sender_type == other_type
    ).update({"is_read": True})
    db.commit()
    return {"success": True}
