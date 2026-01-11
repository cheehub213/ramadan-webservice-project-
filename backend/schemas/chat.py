"""
Chat with Imam Schemas
"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ImamResponse(BaseModel):
    """Imam information response"""
    id: int
    name: str
    email: str
    expertise: str
    is_available: bool
    bio: Optional[str]
    
    class Config:
        from_attributes = True


class ConversationCreateRequest(BaseModel):
    """Request to create a new conversation"""
    imam_id: int
    topic: str
    user_email: Optional[str] = None


class ConversationResponse(BaseModel):
    """Conversation response"""
    id: int
    imam_id: int
    imam_name: str
    user_email: str
    topic: str
    unread_count: int = 0
    created_at: str
    updated_at: str
    
    class Config:
        from_attributes = True


class MessageSendRequest(BaseModel):
    """Request to send a message"""
    conversation_id: int
    message_text: str
    sender_email: Optional[str] = None
    sender_type: Optional[str] = "user"  # "user" or "imam"


class MessageResponse(BaseModel):
    """Message response"""
    id: int
    conversation_id: int
    sender_type: str
    sender_email: str
    message_text: str
    is_read: bool
    created_at: str
    
    class Config:
        from_attributes = True
