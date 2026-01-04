from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.models.chat import Chat, ChatMessage, ImamAvailability
from app.models.imam import Imam
from app.schemas.chat import (
    ChatCreate,
    ChatResponse,
    ChatDetailResponse,
    ChatListResponse,
    ChatMessageCreate,
    ChatMessageResponse,
    ImamAvailabilityUpdate,
    ImamAvailabilityResponse,
    MarkMessagesReadRequest,
    MarkChatReadRequest,
)
from typing import List, Optional
from datetime import datetime

router = APIRouter(prefix="/api/v1/chat", tags=["live-chat"])


# ==================== CHAT ENDPOINTS ====================

@router.post("/conversations", response_model=ChatResponse)
async def start_chat(chat_data: ChatCreate, db: Session = Depends(get_db)) -> ChatResponse:
    """
    Start a new chat conversation with an imam
    
    Request Body:
    - imam_id: ID of the imam (required)
    - user_email: User's email (required)
    - user_name: User's name (optional)
    - title: Chat topic/subject (required)
    - description: Problem description (required)
    """
    try:
        # Verify imam exists
        imam = db.query(Imam).filter(Imam.id == chat_data.imam_id).first()
        if not imam:
            raise HTTPException(status_code=404, detail=f"Imam with ID {chat_data.imam_id} not found")
        
        # Create new chat
        new_chat = Chat(
            imam_id=chat_data.imam_id,
            user_email=chat_data.user_email,
            user_name=chat_data.user_name,
            title=chat_data.title,
            description=chat_data.description,
            is_active=True,
            imam_is_available=False,  # Check if imam is currently available
        )
        
        # Check imam availability
        availability = db.query(ImamAvailability).filter(
            ImamAvailability.imam_id == chat_data.imam_id
        ).first()
        if availability:
            new_chat.imam_is_available = availability.is_available_for_chat
        
        db.add(new_chat)
        db.commit()
        db.refresh(new_chat)
        
        return new_chat
    
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating chat: {str(e)}")


@router.get("/conversations/{chat_id}", response_model=ChatDetailResponse)
async def get_chat_detail(chat_id: int, db: Session = Depends(get_db)) -> ChatDetailResponse:
    """
    Get detailed chat conversation with all messages
    
    Parameters:
    - chat_id: ID of the chat conversation
    """
    try:
        chat = db.query(Chat).filter(Chat.id == chat_id).first()
        if not chat:
            raise HTTPException(status_code=404, detail="Chat not found")
        
        messages = db.query(ChatMessage).filter(ChatMessage.chat_id == chat_id).order_by(
            ChatMessage.created_at
        ).all()
        
        unread_count = db.query(func.count(ChatMessage.id)).filter(
            ChatMessage.chat_id == chat_id,
            ChatMessage.is_read == False
        ).scalar()
        
        return ChatDetailResponse(
            id=chat.id,
            imam_id=chat.imam_id,
            user_email=chat.user_email,
            user_name=chat.user_name,
            title=chat.title,
            description=chat.description,
            is_active=chat.is_active,
            imam_is_available=chat.imam_is_available,
            messages=messages,
            unread_count=unread_count or 0,
            created_at=chat.created_at,
            updated_at=chat.updated_at,
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching chat: {str(e)}")


@router.get("/conversations/user/{user_email}", response_model=List[ChatListResponse])
async def get_user_chats(
    user_email: str,
    active_only: bool = Query(True, description="Show only active chats"),
    db: Session = Depends(get_db)
) -> List[ChatListResponse]:
    """
    Get all chat conversations for a user
    
    Parameters:
    - user_email: User's email address
    - active_only: Show only active chats (default: true)
    """
    try:
        query = db.query(Chat).filter(Chat.user_email == user_email)
        
        if active_only:
            query = query.filter(Chat.is_active == True)
        
        chats = query.order_by(Chat.updated_at.desc()).all()
        
        # Get unread count for each chat
        result = []
        for chat in chats:
            unread_count = db.query(func.count(ChatMessage.id)).filter(
                ChatMessage.chat_id == chat.id,
                ChatMessage.is_read == False
            ).scalar()
            
            result.append(ChatListResponse(
                id=chat.id,
                imam_id=chat.imam_id,
                user_email=chat.user_email,
                user_name=chat.user_name,
                title=chat.title,
                is_active=chat.is_active,
                imam_is_available=chat.imam_is_available,
                last_message_at=chat.last_message_at,
                unread_count=unread_count or 0,
            ))
        
        return result
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching chats: {str(e)}")


@router.get("/conversations/imam/{imam_id}", response_model=List[ChatListResponse])
async def get_imam_chats(
    imam_id: int,
    active_only: bool = Query(True, description="Show only active chats"),
    db: Session = Depends(get_db)
) -> List[ChatListResponse]:
    """
    Get all chat conversations for an imam
    
    Parameters:
    - imam_id: Imam's ID
    - active_only: Show only active chats (default: true)
    """
    try:
        query = db.query(Chat).filter(Chat.imam_id == imam_id)
        
        if active_only:
            query = query.filter(Chat.is_active == True)
        
        chats = query.order_by(Chat.updated_at.desc()).all()
        
        # Get unread count for each chat
        result = []
        for chat in chats:
            unread_count = db.query(func.count(ChatMessage.id)).filter(
                ChatMessage.chat_id == chat.id,
                ChatMessage.is_read == False,
                ChatMessage.sender_type == "user"
            ).scalar()
            
            result.append(ChatListResponse(
                id=chat.id,
                imam_id=chat.imam_id,
                user_email=chat.user_email,
                user_name=chat.user_name,
                title=chat.title,
                is_active=chat.is_active,
                imam_is_available=chat.imam_is_available,
                last_message_at=chat.last_message_at,
                unread_count=unread_count or 0,
            ))
        
        return result
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching chats: {str(e)}")


# ==================== MESSAGE ENDPOINTS ====================

@router.post("/conversations/{chat_id}/messages", response_model=ChatMessageResponse)
async def send_message(
    chat_id: int,
    message_data: ChatMessageCreate,
    db: Session = Depends(get_db)
) -> ChatMessageResponse:
    """
    Send a message in a chat conversation
    
    Parameters:
    - chat_id: ID of the chat conversation
    
    Request Body:
    - message: Message content (required)
    - sender_type: "user" or "imam" (required)
    - sender_id: Email (user) or Imam ID (required)
    - sender_name: Display name (optional)
    """
    try:
        # Verify chat exists
        chat = db.query(Chat).filter(Chat.id == chat_id).first()
        if not chat:
            raise HTTPException(status_code=404, detail="Chat not found")
        
        # Create message
        new_message = ChatMessage(
            chat_id=chat_id,
            sender_type=message_data.sender_type,
            sender_id=message_data.sender_id,
            sender_name=message_data.sender_name,
            message=message_data.message,
            is_read=False,
        )
        
        db.add(new_message)
        
        # Update chat's last message timestamp
        chat.last_message_at = datetime.utcnow()
        chat.updated_at = datetime.utcnow()
        
        db.commit()
        db.refresh(new_message)
        
        return new_message
    
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error sending message: {str(e)}")


@router.get("/conversations/{chat_id}/messages", response_model=List[ChatMessageResponse])
async def get_messages(chat_id: int, db: Session = Depends(get_db)) -> List[ChatMessageResponse]:
    """Get all messages in a chat conversation"""
    try:
        chat = db.query(Chat).filter(Chat.id == chat_id).first()
        if not chat:
            raise HTTPException(status_code=404, detail="Chat not found")
        
        messages = db.query(ChatMessage).filter(
            ChatMessage.chat_id == chat_id
        ).order_by(ChatMessage.created_at).all()
        
        return messages
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching messages: {str(e)}")


@router.put("/messages/read", response_model=dict)
async def mark_messages_read(
    request: MarkMessagesReadRequest,
    db: Session = Depends(get_db)
) -> dict:
    """Mark specific messages as read"""
    try:
        db.query(ChatMessage).filter(
            ChatMessage.id.in_(request.message_ids)
        ).update(
            {ChatMessage.is_read: True, ChatMessage.read_at: datetime.utcnow()},
            synchronize_session=False
        )
        db.commit()
        
        return {"status": "success", "marked_as_read": len(request.message_ids)}
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error marking messages: {str(e)}")


@router.put("/conversations/{chat_id}/read", response_model=dict)
async def mark_chat_read(chat_id: int, db: Session = Depends(get_db)) -> dict:
    """Mark all messages in a chat as read"""
    try:
        count = db.query(func.count(ChatMessage.id)).filter(
            ChatMessage.chat_id == chat_id,
            ChatMessage.is_read == False
        ).scalar()
        
        db.query(ChatMessage).filter(
            ChatMessage.chat_id == chat_id
        ).update(
            {ChatMessage.is_read: True, ChatMessage.read_at: datetime.utcnow()},
            synchronize_session=False
        )
        db.commit()
        
        return {"status": "success", "marked_as_read": count or 0}
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error marking chat: {str(e)}")


# ==================== IMAM AVAILABILITY ====================

@router.put("/imam/{imam_id}/availability", response_model=ImamAvailabilityResponse)
async def update_imam_availability(
    imam_id: int,
    availability: ImamAvailabilityUpdate,
    db: Session = Depends(get_db)
) -> ImamAvailabilityResponse:
    """
    Update imam's online/availability status
    
    Parameters:
    - imam_id: ID of the imam
    
    Request Body:
    - is_online: Is imam online (required)
    - is_available_for_chat: Is imam available for chat (required)
    """
    try:
        # Verify imam exists
        imam = db.query(Imam).filter(Imam.id == imam_id).first()
        if not imam:
            raise HTTPException(status_code=404, detail="Imam not found")
        
        # Update or create availability record
        availability_record = db.query(ImamAvailability).filter(
            ImamAvailability.imam_id == imam_id
        ).first()
        
        if not availability_record:
            availability_record = ImamAvailability(imam_id=imam_id)
        
        availability_record.is_online = availability.is_online
        availability_record.is_available_for_chat = availability.is_available_for_chat
        availability_record.last_seen_at = datetime.utcnow()
        
        db.add(availability_record)
        
        # Update all active chats with this imam
        db.query(Chat).filter(
            Chat.imam_id == imam_id,
            Chat.is_active == True
        ).update({Chat.imam_is_available: availability.is_available_for_chat})
        
        db.commit()
        db.refresh(availability_record)
        
        return availability_record
    
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error updating availability: {str(e)}")


@router.get("/imam/{imam_id}/availability", response_model=ImamAvailabilityResponse)
async def get_imam_availability(imam_id: int, db: Session = Depends(get_db)) -> ImamAvailabilityResponse:
    """Get imam's current availability status"""
    try:
        availability = db.query(ImamAvailability).filter(
            ImamAvailability.imam_id == imam_id
        ).first()
        
        if not availability:
            raise HTTPException(status_code=404, detail="Availability info not found")
        
        return availability
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching availability: {str(e)}")


@router.put("/conversations/{chat_id}/close", response_model=ChatResponse)
async def close_chat(chat_id: int, db: Session = Depends(get_db)) -> ChatResponse:
    """Close a chat conversation"""
    try:
        chat = db.query(Chat).filter(Chat.id == chat_id).first()
        if not chat:
            raise HTTPException(status_code=404, detail="Chat not found")
        
        chat.is_active = False
        chat.updated_at = datetime.utcnow()
        
        db.commit()
        db.refresh(chat)
        
        return chat
    
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error closing chat: {str(e)}")
