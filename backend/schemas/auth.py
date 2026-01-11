"""
Authentication Schemas
"""
from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
from datetime import datetime
import re


class Token(BaseModel):
    """JWT Token response"""
    access_token: str
    refresh_token: Optional[str] = None
    token_type: str = "bearer"
    expires_in: int = 86400  # seconds
    user_email: str
    user_name: str
    user_type: str


class TokenData(BaseModel):
    """Token payload data"""
    email: Optional[str] = None
    user_type: Optional[str] = None
    token_type: Optional[str] = "access"  # "access" or "refresh"


class RefreshTokenRequest(BaseModel):
    """Request to refresh access token"""
    refresh_token: str


class UserSignupRequest(BaseModel):
    """User registration request"""
    email: EmailStr
    name: str = Field(..., min_length=2, max_length=100)
    password: str = Field(..., min_length=8)
    user_type: str = "user"  # "user" or "imam"
    
    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        if not re.search(r'[A-Za-z]', v):
            raise ValueError('Password must contain at least one letter')
        if not re.search(r'\d', v):
            raise ValueError('Password must contain at least one number')
        return v
    
    @validator('user_type')
    def validate_user_type(cls, v):
        if v not in ['user', 'imam', 'admin']:
            raise ValueError('user_type must be user, imam, or admin')
        return v


class UserLoginRequest(BaseModel):
    """User login request"""
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    """User response schema"""
    id: int
    email: str
    name: Optional[str]
    user_type: str
    is_verified: bool = True
    created_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class PasswordChangeRequest(BaseModel):
    """Password change request"""
    current_password: str
    new_password: str = Field(..., min_length=8)
    
    @validator('new_password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        if not re.search(r'[A-Za-z]', v):
            raise ValueError('Password must contain at least one letter')
        if not re.search(r'\d', v):
            raise ValueError('Password must contain at least one number')
        return v


class PasswordResetRequest(BaseModel):
    """Request password reset email"""
    email: EmailStr


class PasswordResetConfirm(BaseModel):
    """Confirm password reset with token"""
    token: str
    new_password: str = Field(..., min_length=8)
    
    @validator('new_password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        if not re.search(r'[A-Za-z]', v):
            raise ValueError('Password must contain at least one letter')
        if not re.search(r'\d', v):
            raise ValueError('Password must contain at least one number')
        return v


class UserUpdateRequest(BaseModel):
    """Update user profile"""
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    email: Optional[EmailStr] = None


# ============= EMAIL VERIFICATION SCHEMAS =============

class SignupResponse(BaseModel):
    """Response after signup - indicates verification needed"""
    message: str
    email: str
    requires_verification: bool = True
    verification_sent: bool = False
    debug_token: Optional[str] = None  # Only for demo mode when SMTP not configured


class EmailVerifyRequest(BaseModel):
    """Verify email with token"""
    token: str


class ResendVerificationRequest(BaseModel):
    """Request to resend verification email"""
    email: EmailStr
