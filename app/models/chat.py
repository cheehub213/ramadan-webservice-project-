from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.sql import func
from app.database import Base
from datetime import datetime

class Chat(Base):
    """Chat conversation between user and imam"""
    __tablename__ = "chats"
    
    id = Column(Integer, primary_key=True, index=True)
    imam_id = Column(Integer, nullable=False)  # FK to Imam
    user_email = Column(String(255), nullable=False)  # User's email
    user_name = Column(String(255))  # User's name (optional)
    
    # Chat metadata
    title = Column(String(255))  # Chat topic/subject
    description = Column(Text)  # Initial problem description
    
    # Status
    is_active = Column(Boolean, default=True)
    imam_is_available = Column(Boolean, default=False)  # Imam online/available status
    
    # Timestamps
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    last_message_at = Column(DateTime)  # Last message timestamp
    
    class Config:
        from_attributes = True


class ChatMessage(Base):
    """Individual chat messages"""
    __tablename__ = "chat_messages"
    
    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(Integer, ForeignKey("chats.id"), nullable=False)
    
    # Message details
    sender_type = Column(String(20), nullable=False)  # "user" or "imam"
    sender_id = Column(String(255), nullable=False)  # Email (user) or Imam ID
    sender_name = Column(String(255))  # Display name
    
    message = Column(Text, nullable=False)  # Message content
    
    # Message status
    is_read = Column(Boolean, default=False)
    read_at = Column(DateTime)
    
    # Metadata
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    class Config:
        from_attributes = True


class ImamAvailability(Base):
    """Track imam online/availability status"""
    __tablename__ = "imam_availability"
    
    id = Column(Integer, primary_key=True, index=True)
    imam_id = Column(Integer, nullable=False, unique=True)  # FK to Imam
    
    # Status
    is_online = Column(Boolean, default=False)
    is_available_for_chat = Column(Boolean, default=False)
    
    # Tracking
    last_seen_at = Column(DateTime)
    last_status_change_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # Auto status
    auto_offline_after_minutes = Column(Integer, default=15)  # Auto mark offline after X minutes
    
    class Config:
        from_attributes = True
