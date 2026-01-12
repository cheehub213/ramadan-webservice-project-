"""
Admin Routes - Administrative endpoints for managing the application
Requires admin role for all endpoints
"""
from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from database import SessionLocal
from models_extended import User, Event, Imam, Conversation, Message, DuaHistory
from .auth import get_current_admin, get_password_hash

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ============= USER MANAGEMENT =============

@router.get("/users")
async def list_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    user_type: Optional[str] = None,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    """List all users (Admin only)"""
    query = db.query(User)
    if user_type:
        query = query.filter(User.user_type == user_type)
    
    total = query.count()
    users = query.offset(skip).limit(limit).all()
    
    return {
        "total": total,
        "users": [
            {
                "id": u.id,
                "email": u.email,
                "name": u.name,
                "user_type": u.user_type,
                "is_verified": u.is_verified,
                "is_active": getattr(u, 'is_active', True),
                "created_at": str(u.created_at) if u.created_at else None,
                "last_login": str(u.last_login) if getattr(u, 'last_login', None) else None
            }
            for u in users
        ]
    }


@router.get("/users/{user_id}")
async def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    """Get user details (Admin only)"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {
        "id": user.id,
        "email": user.email,
        "name": user.name,
        "user_type": user.user_type,
        "is_verified": user.is_verified,
        "is_active": getattr(user, 'is_active', True),
        "login_attempts": getattr(user, 'login_attempts', 0),
        "locked_until": str(user.locked_until) if getattr(user, 'locked_until', None) else None,
        "created_at": str(user.created_at) if user.created_at else None,
        "last_login": str(user.last_login) if getattr(user, 'last_login', None) else None
    }


@router.put("/users/{user_id}/role")
async def update_user_role(
    user_id: int,
    role: str = Query(..., regex="^(user|imam|admin)$"),
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    """Update user role (Admin only)"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Prevent admin from demoting themselves
    if user.id == admin.id and role != "admin":
        raise HTTPException(status_code=400, detail="Cannot change your own admin role")
    
    old_role = user.user_type
    user.user_type = role
    db.commit()
    
    return {"message": f"User role updated from {old_role} to {role}", "user_id": user_id}


@router.put("/users/{user_id}/activate")
async def activate_user(
    user_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    """Activate a user account (Admin only)"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.is_active = True
    user.login_attempts = 0
    user.locked_until = None
    db.commit()
    
    return {"message": "User activated", "user_id": user_id}


@router.put("/users/{user_id}/deactivate")
async def deactivate_user(
    user_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    """Deactivate a user account (Admin only)"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Prevent admin from deactivating themselves
    if user.id == admin.id:
        raise HTTPException(status_code=400, detail="Cannot deactivate your own account")
    
    user.is_active = False
    db.commit()
    
    return {"message": "User deactivated", "user_id": user_id}


@router.delete("/users/{user_id}")
async def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    """Delete a user (Admin only)"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Prevent admin from deleting themselves
    if user.id == admin.id:
        raise HTTPException(status_code=400, detail="Cannot delete your own account")
    
    db.delete(user)
    db.commit()
    
    return {"message": "User deleted", "user_id": user_id}


@router.post("/users/create-admin")
async def create_admin_user(
    email: str,
    password: str,
    name: str = "Admin",
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    """Create a new admin user (Admin only)"""
    existing = db.query(User).filter(User.email == email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    new_admin = User(
        email=email,
        name=name,
        password_hash=get_password_hash(password),
        user_type="admin",
        is_verified=True,
        is_active=True
    )
    db.add(new_admin)
    db.commit()
    
    return {"message": "Admin user created", "email": email}


# ============= IMAM MANAGEMENT =============

@router.get("/imams")
async def list_imams(
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    """List all imams (Admin only)"""
    imams = db.query(Imam).all()
    return {
        "total": len(imams),
        "imams": [
            {
                "id": i.id,
                "name": i.name,
                "email": i.email,
                "expertise": i.expertise,
                "bio": i.bio,
                "is_available": i.is_available,
                "created_at": str(i.created_at) if hasattr(i, 'created_at') and i.created_at else None
            }
            for i in imams
        ]
    }


@router.post("/imams")
async def create_imam(
    name: str,
    email: str,
    expertise: str = "",
    bio: str = "",
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    """Create a new imam (Admin only)"""
    existing = db.query(Imam).filter(Imam.email == email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Imam with this email already exists")
    
    imam = Imam(
        name=name,
        email=email,
        expertise=expertise,
        bio=bio,
        is_available=True
    )
    db.add(imam)
    db.commit()
    db.refresh(imam)
    
    return {"message": "Imam created", "id": imam.id, "name": name}


@router.put("/imams/{imam_id}")
async def update_imam(
    imam_id: int,
    name: Optional[str] = None,
    expertise: Optional[str] = None,
    bio: Optional[str] = None,
    is_available: Optional[bool] = None,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    """Update imam details (Admin only)"""
    imam = db.query(Imam).filter(Imam.id == imam_id).first()
    if not imam:
        raise HTTPException(status_code=404, detail="Imam not found")
    
    if name is not None:
        imam.name = name
    if expertise is not None:
        imam.expertise = expertise
    if bio is not None:
        imam.bio = bio
    if is_available is not None:
        imam.is_available = is_available
    
    db.commit()
    
    return {"message": "Imam updated", "id": imam_id}


@router.delete("/imams/{imam_id}")
async def delete_imam(
    imam_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    """Delete an imam (Admin only)"""
    imam = db.query(Imam).filter(Imam.id == imam_id).first()
    if not imam:
        raise HTTPException(status_code=404, detail="Imam not found")
    
    db.delete(imam)
    db.commit()
    
    return {"message": "Imam deleted", "id": imam_id}


# ============= EVENT MANAGEMENT =============

@router.get("/events")
async def list_all_events(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    verified_only: bool = False,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    """List all events including unverified (Admin only)"""
    query = db.query(Event)
    if verified_only:
        query = query.filter(Event.is_verified == True)
    
    total = query.count()
    events = query.order_by(Event.created_at.desc()).offset(skip).limit(limit).all()
    
    return {
        "total": total,
        "events": [
            {
                "id": e.id,
                "title": e.title,
                "city": e.city,
                "category": e.category,
                "event_date": str(e.event_date),
                "organizer_name": e.organizer_name,
                "is_verified": e.is_verified,
                "created_at": str(e.created_at) if e.created_at else None
            }
            for e in events
        ]
    }


@router.put("/events/{event_id}/verify")
async def verify_event(
    event_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    """Verify an event (Admin only)"""
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    event.is_verified = True
    db.commit()
    
    return {"message": "Event verified", "event_id": event_id}


@router.put("/events/{event_id}/unverify")
async def unverify_event(
    event_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    """Unverify an event (Admin only)"""
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    event.is_verified = False
    db.commit()
    
    return {"message": "Event unverified", "event_id": event_id}


@router.delete("/events/{event_id}")
async def delete_event(
    event_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    """Delete an event (Admin only)"""
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    db.delete(event)
    db.commit()
    
    return {"message": "Event deleted", "event_id": event_id}


# ============= STATISTICS =============

@router.get("/stats")
async def get_statistics(
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    """Get application statistics (Admin only)"""
    total_users = db.query(User).count()
    active_users = db.query(User).filter(User.is_active == True).count()
    verified_users = db.query(User).filter(User.is_verified == True).count()
    admin_users = db.query(User).filter(User.user_type == "admin").count()
    imam_users = db.query(User).filter(User.user_type == "imam").count()
    
    total_events = db.query(Event).count()
    verified_events = db.query(Event).filter(Event.is_verified == True).count()
    
    total_imams = db.query(Imam).count()
    available_imams = db.query(Imam).filter(Imam.is_available == True).count()
    
    total_conversations = db.query(Conversation).count()
    total_messages = db.query(Message).count()
    total_duas = db.query(DuaHistory).count()
    
    return {
        "users": {
            "total": total_users,
            "active": active_users,
            "verified": verified_users,
            "admins": admin_users,
            "imams": imam_users
        },
        "events": {
            "total": total_events,
            "verified": verified_events,
            "pending": total_events - verified_events
        },
        "imams": {
            "total": total_imams,
            "available": available_imams
        },
        "activity": {
            "conversations": total_conversations,
            "messages": total_messages,
            "duas_generated": total_duas
        }
    }


# ============= SYSTEM =============

from pydantic import BaseModel

class SeedAdminRequest(BaseModel):
    secret_key: str
    email: str = "admin@ramadan.app"
    password: str = "Admin123!"
    full_name: str = "System Admin"


@router.post("/seed-admin")
async def seed_initial_admin(
    request: SeedAdminRequest,
    db: Session = Depends(get_db)
):
    """
    Create initial admin user (one-time setup, requires secret key).
    This endpoint does NOT require authentication - only the secret key.
    
    Default secret key: ramadan-admin-seed-2026 (set ADMIN_SEED_SECRET env var to change)
    """
    import os
    expected_secret = os.getenv("ADMIN_SEED_SECRET", "ramadan-admin-seed-2026")
    
    if request.secret_key != expected_secret:
        raise HTTPException(status_code=403, detail="Invalid secret key")
    
    # Check if any admin exists
    existing_admin = db.query(User).filter(User.user_type == "admin").first()
    if existing_admin:
        raise HTTPException(status_code=400, detail="Admin user already exists. Use admin endpoints to manage users.")
    
    # Check if email already exists
    existing_user = db.query(User).filter(User.email == request.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail=f"User with email {request.email} already exists")
    
    admin = User(
        email=request.email,
        name=request.full_name,
        password_hash=get_password_hash(request.password),
        user_type="admin",
        is_verified=True,
        is_active=True
    )
    db.add(admin)
    db.commit()
    
    return {
        "message": "Initial admin created successfully",
        "email": request.email,
        "note": "You can now login with these credentials"
    }
