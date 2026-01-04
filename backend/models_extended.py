from database import Base
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from sqlalchemy.sql import func
import secrets
import hashlib

# ============= USER MODELS =============
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    name = Column(String, nullable=True)
    password_hash = Column(String, nullable=True)  # For password authentication
    user_type = Column(String)  # "user" or "imam"
    is_verified = Column(Boolean, default=False)  # Email verification status
    verification_token = Column(String, nullable=True)  # Token for email verification
    verification_code = Column(String, nullable=True)  # 6-digit code for verification
    reset_token = Column(String, nullable=True)  # For password reset
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    duas = relationship("DuaHistory", back_populates="user")
    conversations = relationship("Conversation", back_populates="user")
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash password using SHA256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    @staticmethod
    def generate_verification_code() -> str:
        """Generate 6-digit verification code"""
        return ''.join([str(secrets.randbelow(10)) for _ in range(6)])
    
    @staticmethod
    def generate_token() -> str:
        """Generate secure token"""
        return secrets.token_urlsafe(32)
    
    def verify_password(self, password: str) -> bool:
        """Verify password"""
        return self.password_hash == self.hash_password(password)

# ============= DUA MODELS =============
class DuaHistory(Base):
    __tablename__ = "dua_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    email = Column(String, index=True)
    category = Column(String)
    context = Column(Text)
    dua_text_en = Column(Text)
    dua_text_ar = Column(Text)
    how_to_use_en = Column(Text)
    how_to_use_ar = Column(Text)
    helpful = Column(Boolean, nullable=True)
    feedback_notes = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now())

    user = relationship("User", back_populates="duas")

# ============= CHAT MODELS =============
class Imam(Base):
    __tablename__ = "imams"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String, nullable=True)  # For imam password
    expertise = Column(String)  # Quran & Islamic Law, Hadith & History, etc
    is_available = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=True)  # Imams are pre-verified
    phone = Column(String, nullable=True)
    bio = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now())

    conversations = relationship("Conversation", back_populates="imam")
    messages = relationship("Message", back_populates="imam")

class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    user_email = Column(String, index=True)
    imam_id = Column(Integer, ForeignKey("imams.id"))
    topic = Column(String)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    user = relationship("User", back_populates="conversations")
    imam = relationship("Imam", back_populates="conversations")
    messages = relationship("Message", back_populates="conversation")

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"))
    imam_id = Column(Integer, ForeignKey("imams.id"), nullable=True)
    sender_type = Column(String)  # "user" or "imam"
    sender_email = Column(String, index=True)
    message_text = Column(Text)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())

    conversation = relationship("Conversation", back_populates="messages")
    imam = relationship("Imam", back_populates="messages")

# ============= VIDEO MODELS =============
class Video(Base):
    __tablename__ = "videos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    youtube_id = Column(String)
    channel = Column(String)
    duration = Column(String)
    description = Column(Text)
    thumbnail_url = Column(String, nullable=True)
    created_at = Column(DateTime, server_default=func.now())

# ============= AI ANALYZER MODELS =============
class AIAnalysis(Base):
    __tablename__ = "ai_analyses"

    id = Column(Integer, primary_key=True, index=True)
    user_email = Column(String, index=True)
    question = Column(Text)
    ayah = Column(JSON)
    hadith = Column(JSON)
    explanation = Column(Text)
    created_at = Column(DateTime, server_default=func.now())

# ============= HISTORY MODELS =============
class UserHistory(Base):
    __tablename__ = "user_history"

    id = Column(Integer, primary_key=True, index=True)
    user_email = Column(String, index=True)
    action_type = Column(String)
    action_data = Column(JSON)
    created_at = Column(DateTime, server_default=func.now())
