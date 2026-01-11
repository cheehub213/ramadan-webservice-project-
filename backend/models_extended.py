from database import Base
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from sqlalchemy.sql import func

# ============= USER MODELS =============
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    name = Column(String, nullable=True)
    password_hash = Column(String, nullable=True)  # For JWT authentication
    user_type = Column(String, default="user")  # "user", "imam", or "admin"
    is_verified = Column(Boolean, default=False)  # Must verify email first
    is_active = Column(Boolean, default=True)
    last_login = Column(DateTime, nullable=True)
    login_attempts = Column(Integer, default=0)
    locked_until = Column(DateTime, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    duas = relationship("DuaHistory", back_populates="user")
    conversations = relationship("Conversation", back_populates="user")


# ============= TOKEN BLACKLIST (for logout/revocation) =============
class TokenBlacklist(Base):
    __tablename__ = "token_blacklist"
    
    id = Column(Integer, primary_key=True, index=True)
    token_jti = Column(String, unique=True, index=True)  # JWT ID
    user_email = Column(String, index=True)
    token_type = Column(String)  # "access" or "refresh"
    expires_at = Column(DateTime)
    blacklisted_at = Column(DateTime, server_default=func.now())


# ============= PASSWORD RESET TOKENS =============
class PasswordResetToken(Base):
    __tablename__ = "password_reset_tokens"
    
    id = Column(Integer, primary_key=True, index=True)
    user_email = Column(String, index=True)
    token = Column(String, unique=True, index=True)
    expires_at = Column(DateTime)
    used = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())


# ============= EMAIL VERIFICATION TOKENS =============
class EmailVerificationToken(Base):
    __tablename__ = "email_verification_tokens"
    
    id = Column(Integer, primary_key=True, index=True)
    user_email = Column(String, index=True)
    token = Column(String, unique=True, index=True)
    expires_at = Column(DateTime)
    used = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())

    
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
    expertise = Column(String)  # Quran & Islamic Law, Hadith & History, etc
    is_available = Column(Boolean, default=True)
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

# ============= VIDEO MODELS (already exists) =============
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
    ayah = Column(JSON)  # Store ayah object
    hadith = Column(JSON)  # Store hadith object
    explanation = Column(Text)  # AI explanation
    created_at = Column(DateTime, server_default=func.now())

# ============= HISTORY MODELS =============
class UserHistory(Base):
    __tablename__ = "user_history"
    
    id = Column(Integer, primary_key=True, index=True)
    user_email = Column(String, index=True)
    action_type = Column(String)  # "dua_generated", "video_searched", "chat_created", etc
    action_data = Column(JSON)
    created_at = Column(DateTime, server_default=func.now())


# ============= EVENTS MODELS (Tunisia) =============
class Event(Base):
    __tablename__ = "events"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    city = Column(String(100), nullable=False)
    location = Column(String(200))
    category = Column(String(50))
    event_date = Column(DateTime, nullable=False)
    start_time = Column(String(20))
    end_time = Column(String(20))
    organizer_name = Column(String(100))
    organizer_contact = Column(String(100))
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())
