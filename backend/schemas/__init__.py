"""
Pydantic Schemas for myRamadan API
"""
from .auth import Token, TokenData, UserSignupRequest, UserLoginRequest, UserResponse
from .dua import DuaGenerateRequest, DuaHistoryResponse
from .chat import (
    ImamResponse, ConversationCreateRequest, MessageSendRequest, 
    MessageResponse, ConversationResponse
)
from .analyzer import AnalyzeRequest
from .events import EventCreateRequest, EventResponse
from .videos import VideoSearchRequest

__all__ = [
    # Auth
    "Token", "TokenData", "UserSignupRequest", "UserLoginRequest", "UserResponse",
    # Dua
    "DuaGenerateRequest", "DuaHistoryResponse",
    # Chat
    "ImamResponse", "ConversationCreateRequest", "MessageSendRequest", 
    "MessageResponse", "ConversationResponse",
    # Analyzer
    "AnalyzeRequest",
    # Events
    "EventCreateRequest", "EventResponse",
    # Videos
    "VideoSearchRequest",
]
