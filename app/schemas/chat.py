from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime


# ==================== CHAT SCHEMAS ====================

class ChatMessageCreate(BaseModel):
    """Schema for creating a chat message"""
    message: str
    sender_type: str  # "user" or "imam"
    sender_id: str
    sender_name: Optional[str] = None


class ChatMessageResponse(BaseModel):
    """Response schema for chat message"""
    id: int
    chat_id: int
    sender_type: str
    sender_id: str
    sender_name: Optional[str]
    message: str
    is_read: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class ChatCreate(BaseModel):
    """Schema for creating a new chat"""
    imam_id: int
    user_email: str
    user_name: Optional[str] = None
    title: str  # Chat topic
    description: str  # Problem description


class ChatResponse(BaseModel):
    """Response schema for chat"""
    id: int
    imam_id: int
    user_email: str
    user_name: Optional[str]
    title: str
    description: str
    is_active: bool
    imam_is_available: bool
    created_at: datetime
    updated_at: datetime
    last_message_at: Optional[datetime]
    
    class Config:
        from_attributes = True


class ChatDetailResponse(BaseModel):
    """Detailed chat response with messages"""
    id: int
    imam_id: int
    user_email: str
    user_name: Optional[str]
    title: str
    description: str
    is_active: bool
    imam_is_available: bool
    messages: List[ChatMessageResponse] = []
    unread_count: int = 0
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class ImamAvailabilityUpdate(BaseModel):
    """Update imam availability status"""
    is_online: bool
    is_available_for_chat: bool
    
    class Config:
        from_attributes = True


class ImamAvailabilityResponse(BaseModel):
    """Response for imam availability"""
    id: int
    imam_id: int
    is_online: bool
    is_available_for_chat: bool
    last_seen_at: Optional[datetime]
    last_status_change_at: datetime
    
    class Config:
        from_attributes = True


class ChatListResponse(BaseModel):
    """List response for chats"""
    id: int
    imam_id: int
    user_email: str
    user_name: Optional[str]
    title: str
    is_active: bool
    imam_is_available: bool
    last_message_at: Optional[datetime]
    unread_count: int = 0
    
    class Config:
        from_attributes = True


# ==================== MESSAGE MARKING ====================

class MarkMessagesReadRequest(BaseModel):
    """Request to mark messages as read"""
    message_ids: List[int]


class MarkChatReadRequest(BaseModel):
    """Request to mark entire chat as read"""
    chat_id: int
