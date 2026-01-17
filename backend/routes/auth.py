"""
Authentication Routes - Enhanced JWT Authorization
Features:
- Access & Refresh Tokens
- Token Blacklisting (logout)
- Email Verification (signup)
- Password Change
- Password Reset
- Account Locking (brute force protection)
- Role-based Access Control
"""
from fastapi import APIRouter, HTTPException, Depends, status, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from jose import JWTError, jwt
import bcrypt
import os
import uuid
import secrets

from database import SessionLocal
from models_extended import User, TokenBlacklist, PasswordResetToken, EmailVerificationToken
from schemas.auth import (
    Token, TokenData, UserSignupRequest, UserLoginRequest, UserResponse,
    RefreshTokenRequest, PasswordChangeRequest, PasswordResetRequest,
    PasswordResetConfirm, UserUpdateRequest, SignupResponse, EmailVerifyRequest,
    ResendVerificationRequest
)
from services.email_service import (
    send_verification_email, send_password_reset_email, send_welcome_email,
    generate_verification_token, VERIFICATION_TOKEN_EXPIRE_HOURS
)

router = APIRouter()

# JWT Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "ramadan-helper-secret-key-2026-change-in-production")
REFRESH_SECRET_KEY = os.getenv("REFRESH_SECRET_KEY", SECRET_KEY + "-refresh")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 30 minutes
REFRESH_TOKEN_EXPIRE_DAYS = 7  # 7 days

# Security settings
MAX_LOGIN_ATTEMPTS = 5
LOCKOUT_DURATION_MINUTES = 15

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token", auto_error=False)


# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Password utilities - using bcrypt directly
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))


def get_password_hash(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    """Create access token with JTI for revocation"""
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({
        "exp": expire,
        "iat": datetime.utcnow(),
        "jti": str(uuid.uuid4()),
        "type": "access"
    })
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token(data: dict) -> str:
    """Create refresh token with longer expiry"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({
        "exp": expire,
        "iat": datetime.utcnow(),
        "jti": str(uuid.uuid4()),
        "type": "refresh"
    })
    return jwt.encode(to_encode, REFRESH_SECRET_KEY, algorithm=ALGORITHM)


def is_token_blacklisted(jti: str, db: Session) -> bool:
    """Check if token is blacklisted"""
    return db.query(TokenBlacklist).filter(TokenBlacklist.token_jti == jti).first() is not None


def blacklist_token(token: str, user_email: str, token_type: str, db: Session):
    """Add token to blacklist"""
    try:
        secret = REFRESH_SECRET_KEY if token_type == "refresh" else SECRET_KEY
        payload = jwt.decode(token, secret, algorithms=[ALGORITHM])
        jti = payload.get("jti")
        exp = datetime.fromtimestamp(payload.get("exp"))
        
        blacklisted = TokenBlacklist(
            token_jti=jti,
            user_email=user_email,
            token_type=token_type,
            expires_at=exp
        )
        db.add(blacklisted)
        db.commit()
    except Exception:
        pass  # Token already invalid


# User authentication dependencies
async def get_current_user(
    token: str = Depends(oauth2_scheme), 
    db: Session = Depends(get_db)
) -> User:
    """Get current user from JWT token"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    if not token:
        raise credentials_exception
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        token_type: str = payload.get("type")
        jti: str = payload.get("jti")
        
        if email is None or token_type != "access":
            raise credentials_exception
        
        # Check if token is blacklisted
        if jti and is_token_blacklisted(jti, db):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has been revoked"
            )
        
        token_data = TokenData(email=email, user_type=payload.get("user_type"))
    except JWTError:
        raise credentials_exception
    
    user = db.query(User).filter(User.email == token_data.email).first()
    if user is None:
        raise credentials_exception
    
    # Check if account is active
    if hasattr(user, 'is_active') and not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is deactivated"
        )
    
    return user


async def get_current_user_optional(
    token: str = Depends(oauth2_scheme), 
    db: Session = Depends(get_db)
) -> User | None:
    """Get current user if token provided, otherwise None"""
    if not token:
        return None
    try:
        return await get_current_user(token, db)
    except HTTPException:
        return None


async def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """Get current active user"""
    return current_user


async def get_current_imam(current_user: User = Depends(get_current_user)) -> User:
    """Get current imam user (requires imam role)"""
    if current_user.user_type not in ["imam", "admin"]:
        raise HTTPException(status_code=403, detail="Access denied. Imam role required.")
    return current_user


async def get_current_admin(current_user: User = Depends(get_current_user)) -> User:
    """Get current admin user (requires admin role)"""
    if current_user.user_type != "admin":
        raise HTTPException(status_code=403, detail="Access denied. Admin role required.")
    return current_user


def check_account_locked(user: User) -> bool:
    """Check if account is locked due to failed login attempts"""
    if hasattr(user, 'locked_until') and user.locked_until and user.locked_until > datetime.utcnow():
        return True
    return False


def handle_failed_login(user: User, db: Session):
    """Handle failed login attempt - increment counter and possibly lock"""
    if hasattr(user, 'login_attempts'):
        user.login_attempts = (user.login_attempts or 0) + 1
        if user.login_attempts >= MAX_LOGIN_ATTEMPTS:
            user.locked_until = datetime.utcnow() + timedelta(minutes=LOCKOUT_DURATION_MINUTES)
        db.commit()


def handle_successful_login(user: User, db: Session):
    """Reset login attempts on successful login"""
    if hasattr(user, 'login_attempts'):
        user.login_attempts = 0
        user.locked_until = None
    if hasattr(user, 'last_login'):
        user.last_login = datetime.utcnow()
    db.commit()


# ============= ROUTES =============

@router.post("/signup", response_model=SignupResponse)
async def signup(request: UserSignupRequest, db: Session = Depends(get_db)):
    """
    Register a new user - sends verification email
    User must verify email before they can login
    """
    # Check if user exists
    existing = db.query(User).filter(User.email == request.email).first()
    if existing:
        if existing.is_verified:
            raise HTTPException(status_code=400, detail="Email already registered")
        else:
            # User exists but not verified - resend verification email
            # Delete old tokens
            db.query(EmailVerificationToken).filter(
                EmailVerificationToken.user_email == request.email
            ).delete()
            db.commit()
            
            # Generate new token
            token = generate_verification_token()
            verification_token = EmailVerificationToken(
                user_email=request.email,
                token=token,
                expires_at=datetime.utcnow() + timedelta(hours=VERIFICATION_TOKEN_EXPIRE_HOURS)
            )
            db.add(verification_token)
            db.commit()
            
            # Send verification email
            email_result = send_verification_email(request.email, existing.name or request.name, token)
            
            return SignupResponse(
                message="Verification email resent. Please check your inbox.",
                email=request.email,
                requires_verification=True,
                verification_sent=email_result["email_sent"],
                # Include token in response for demo mode (when SMTP not configured)
                debug_token=token if not email_result["email_sent"] else None
            )
    
    # Create new user (unverified)
    hashed_password = get_password_hash(request.password)
    user = User(
        email=request.email,
        name=request.name,
        password_hash=hashed_password,
        user_type=request.user_type,
        is_verified=False  # Must verify email first
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    # Generate verification token
    token = generate_verification_token()
    verification_token = EmailVerificationToken(
        user_email=request.email,
        token=token,
        expires_at=datetime.utcnow() + timedelta(hours=VERIFICATION_TOKEN_EXPIRE_HOURS)
    )
    db.add(verification_token)
    db.commit()
    
    # Send verification email
    email_result = send_verification_email(request.email, request.name, token)
    
    return SignupResponse(
        message="Account created! Please check your email to verify your account.",
        email=request.email,
        requires_verification=True,
        verification_sent=email_result["email_sent"],
        # Include token in response for demo mode (when SMTP not configured)
        debug_token=token if not email_result["email_sent"] else None
    )


@router.post("/verify-email")
async def verify_email(request: EmailVerifyRequest, db: Session = Depends(get_db)):
    """
    Verify email with token sent to user's email
    """
    # Find the token
    verification = db.query(EmailVerificationToken).filter(
        EmailVerificationToken.token == request.token,
        EmailVerificationToken.used == False
    ).first()
    
    if not verification:
        raise HTTPException(status_code=400, detail="Invalid or expired verification token")
    
    # Check if expired
    if verification.expires_at < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Verification token has expired. Please request a new one.")
    
    # Find the user
    user = db.query(User).filter(User.email == verification.user_email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Mark user as verified
    user.is_verified = True
    verification.used = True
    db.commit()
    
    # Send welcome email
    send_welcome_email(user.email, user.name or user.email.split("@")[0])
    
    # Generate tokens so user can login immediately
    access_token = create_access_token(
        data={"sub": user.email, "user_type": user.user_type}
    )
    refresh_token = create_refresh_token(
        data={"sub": user.email, "user_type": user.user_type}
    )
    
    return {
        "message": "Email verified successfully! Welcome to myRamadan.",
        "verified": True,
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "user_email": user.email,
        "user_name": user.name or user.email.split("@")[0]
    }


@router.post("/resend-verification")
async def resend_verification(request: ResendVerificationRequest, db: Session = Depends(get_db)):
    """
    Resend verification email to user
    """
    user = db.query(User).filter(User.email == request.email).first()
    
    if not user:
        # Don't reveal if email exists or not
        return {"message": "If an account exists with this email, a verification link has been sent."}
    
    if user.is_verified:
        raise HTTPException(status_code=400, detail="Email is already verified. Please login.")
    
    # Delete old tokens
    db.query(EmailVerificationToken).filter(
        EmailVerificationToken.user_email == request.email
    ).delete()
    db.commit()
    
    # Generate new token
    token = generate_verification_token()
    verification_token = EmailVerificationToken(
        user_email=request.email,
        token=token,
        expires_at=datetime.utcnow() + timedelta(hours=VERIFICATION_TOKEN_EXPIRE_HOURS)
    )
    db.add(verification_token)
    db.commit()
    
    # Send verification email
    email_result = send_verification_email(request.email, user.name or request.email.split("@")[0], token)
    
    return {
        "message": "Verification email sent. Please check your inbox.",
        "email_sent": email_result["email_sent"],
        # Include token for demo mode
        "debug_token": token if not email_result["email_sent"] else None
    }


@router.post("/token", response_model=Token)
async def login_for_token(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: Session = Depends(get_db)
):
    """OAuth2 token endpoint for login"""
    user = db.query(User).filter(User.email == form_data.username).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Check if email is verified
    if not user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Email not verified. Please check your inbox for the verification link."
        )
    
    # Check if account is locked
    if check_account_locked(user):
        minutes_left = int((user.locked_until - datetime.utcnow()).total_seconds() / 60) + 1
        raise HTTPException(
            status_code=status.HTTP_423_LOCKED,
            detail=f"Account locked due to too many failed attempts. Try again in {minutes_left} minutes."
        )
    
    if not user.password_hash or not verify_password(form_data.password, user.password_hash):
        handle_failed_login(user, db)
        attempts_left = MAX_LOGIN_ATTEMPTS - (user.login_attempts or 0)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Incorrect email or password. {attempts_left} attempts remaining.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Successful login
    handle_successful_login(user, db)
    
    access_token = create_access_token(
        data={"sub": user.email, "user_type": user.user_type}
    )
    refresh_token = create_refresh_token(
        data={"sub": user.email, "user_type": user.user_type}
    )
    
    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        user_email=user.email,
        user_name=user.name or user.email.split("@")[0],
        user_type=user.user_type
    )


@router.post("/login")
async def login(request: UserLoginRequest, db: Session = Depends(get_db)):
    """JSON-based login endpoint"""
    user = db.query(User).filter(User.email == request.email).first()
    
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    # Check if email is verified
    if not user.is_verified:
        raise HTTPException(
            status_code=403,
            detail="EMAIL_NOT_VERIFIED",
            headers={"X-Email": request.email}
        )
    
    # Check if account is locked
    if check_account_locked(user):
        minutes_left = int((user.locked_until - datetime.utcnow()).total_seconds() / 60) + 1
        raise HTTPException(
            status_code=423,
            detail=f"Account locked. Try again in {minutes_left} minutes."
        )
    
    if not user.password_hash or not verify_password(request.password, user.password_hash):
        handle_failed_login(user, db)
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    # Successful login
    handle_successful_login(user, db)
    
    access_token = create_access_token(
        data={"sub": user.email, "user_type": user.user_type}
    )
    refresh_token = create_refresh_token(
        data={"sub": user.email, "user_type": user.user_type}
    )
    
    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        user_email=user.email,
        user_name=user.name or user.email.split("@")[0],
        user_type=user.user_type
    )


@router.post("/refresh", response_model=Token)
async def refresh_token(request: RefreshTokenRequest, db: Session = Depends(get_db)):
    """Refresh access token using refresh token"""
    try:
        payload = jwt.decode(request.refresh_token, REFRESH_SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        token_type: str = payload.get("type")
        jti: str = payload.get("jti")
        
        if email is None or token_type != "refresh":
            raise HTTPException(status_code=401, detail="Invalid refresh token")
        
        # Check if token is blacklisted
        if jti and is_token_blacklisted(jti, db):
            raise HTTPException(status_code=401, detail="Refresh token has been revoked")
        
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    if hasattr(user, 'is_active') and not user.is_active:
        raise HTTPException(status_code=401, detail="User account is inactive")
    
    # Create new access token
    access_token = create_access_token(
        data={"sub": user.email, "user_type": user.user_type}
    )
    
    return Token(
        access_token=access_token,
        refresh_token=request.refresh_token,  # Return same refresh token
        token_type="bearer",
        expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        user_email=user.email,
        user_name=user.name or user.email.split("@")[0],
        user_type=user.user_type
    )


@router.post("/logout")
async def logout(
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Logout - blacklist current access token"""
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.split(" ")[1]
        blacklist_token(token, current_user.email, "access", db)
    
    return {"message": "Successfully logged out"}


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_active_user)):
    """Get current user profile"""
    return current_user


@router.put("/me", response_model=UserResponse)
async def update_profile(
    request: UserUpdateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update current user profile"""
    if request.name:
        current_user.name = request.name
    if request.email and request.email != current_user.email:
        # Check if email is already taken
        existing = db.query(User).filter(User.email == request.email).first()
        if existing:
            raise HTTPException(status_code=400, detail="Email already in use")
        current_user.email = request.email
    
    db.commit()
    db.refresh(current_user)
    return current_user


@router.post("/change-password")
async def change_password(
    request: PasswordChangeRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Change password for logged-in user"""
    if not verify_password(request.current_password, current_user.password_hash):
        raise HTTPException(status_code=400, detail="Current password is incorrect")
    
    if request.current_password == request.new_password:
        raise HTTPException(status_code=400, detail="New password must be different")
    
    current_user.password_hash = get_password_hash(request.new_password)
    db.commit()
    
    return {"message": "Password changed successfully"}


@router.post("/forgot-password")
async def forgot_password(request: PasswordResetRequest, db: Session = Depends(get_db)):
    """Request password reset - generates reset token"""
    user = db.query(User).filter(User.email == request.email).first()
    
    # Always return success to prevent email enumeration
    if not user:
        return {"message": "If the email exists, a reset link has been sent"}
    
    # Generate reset token
    reset_token = secrets.token_urlsafe(32)
    expires_at = datetime.utcnow() + timedelta(hours=1)
    
    # Invalidate any existing reset tokens
    db.query(PasswordResetToken).filter(
        PasswordResetToken.user_email == request.email,
        PasswordResetToken.used == False
    ).update({"used": True})
    
    # Create new reset token
    token_record = PasswordResetToken(
        user_email=request.email,
        token=reset_token,
        expires_at=expires_at
    )
    db.add(token_record)
    db.commit()
    
    # In production, send email with reset link
    return {
        "message": "If the email exists, a reset link has been sent",
        "reset_token": reset_token,  # Remove in production!
        "expires_in": "1 hour"
    }


@router.post("/reset-password")
async def reset_password(request: PasswordResetConfirm, db: Session = Depends(get_db)):
    """Reset password using reset token"""
    token_record = db.query(PasswordResetToken).filter(
        PasswordResetToken.token == request.token,
        PasswordResetToken.used == False,
        PasswordResetToken.expires_at > datetime.utcnow()
    ).first()
    
    if not token_record:
        raise HTTPException(status_code=400, detail="Invalid or expired reset token")
    
    user = db.query(User).filter(User.email == token_record.user_email).first()
    if not user:
        raise HTTPException(status_code=400, detail="User not found")
    
    # Update password
    user.password_hash = get_password_hash(request.new_password)
    if hasattr(user, 'login_attempts'):
        user.login_attempts = 0
        user.locked_until = None
    
    # Mark token as used
    token_record.used = True
    
    db.commit()
    
    return {"message": "Password reset successfully"}


@router.get("/verify-token")
async def verify_token(current_user: User = Depends(get_current_user)):
    """Verify if current token is valid"""
    return {
        "valid": True,
        "user_email": current_user.email,
        "user_type": current_user.user_type
    }


# Admin routes
@router.get("/users")
async def list_users(
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """List all users (admin only)"""
    users = db.query(User).all()
    return [
        {
            "id": u.id,
            "email": u.email,
            "name": u.name,
            "user_type": u.user_type,
            "is_active": getattr(u, 'is_active', True),
            "created_at": str(u.created_at) if u.created_at else None
        }
        for u in users
    ]


@router.put("/users/{user_id}/deactivate")
async def deactivate_user(
    user_id: int,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Deactivate a user account (admin only)"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.id == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot deactivate your own account")
    
    if hasattr(user, 'is_active'):
        user.is_active = False
        db.commit()
    return {"message": f"User {user.email} deactivated"}


@router.put("/users/{user_id}/activate")
async def activate_user(
    user_id: int,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Activate a user account (admin only)"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if hasattr(user, 'is_active'):
        user.is_active = True
    if hasattr(user, 'login_attempts'):
        user.login_attempts = 0
        user.locked_until = None
    db.commit()
    return {"message": f"User {user.email} activated"}
