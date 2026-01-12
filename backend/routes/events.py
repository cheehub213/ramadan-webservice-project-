"""
Events Routes (Tunisia Local Events) - Protected endpoints requiring authentication
"""
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime, date
from typing import List, Optional

from database import SessionLocal
from models_extended import Event, User
from schemas.events import EventCreateRequest, EventResponse, TUNISIA_CITIES, EVENT_CATEGORIES
from .auth import get_current_user, get_current_user_optional

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/cities")
async def get_cities():
    """Get list of Tunisia cities for events (public)"""
    return {"cities": TUNISIA_CITIES}


@router.get("/categories")
async def get_categories():
    """Get list of event categories (public)"""
    return {"categories": EVENT_CATEGORIES}


@router.post("/", response_model=EventResponse)
@router.post("", response_model=EventResponse, include_in_schema=False)
async def create_event(
    request: EventCreateRequest, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new event (requires authentication)"""
    # Handle different field name variations from frontend
    start_time = request.start_time or request.event_time
    organizer_contact = request.organizer_contact or request.contact_info or request.contact_phone
    is_featured = request.is_featured or (request.listing_type == "featured")
    
    # Convert date string to date object
    try:
        event_date_obj = datetime.strptime(request.event_date, "%Y-%m-%d").date()
    except ValueError:
        event_date_obj = datetime.now().date()
    
    # Use authenticated user's info as organizer if not provided
    organizer_name = request.organizer_name or current_user.full_name or current_user.email
    
    event = Event(
        title=request.title,
        description=request.description or "",
        city=request.city,
        location=request.location or "",
        category=request.category,
        event_date=event_date_obj,
        start_time=start_time,
        end_time=request.end_time,
        organizer_name=organizer_name,
        organizer_contact=organizer_contact,
        is_verified=False
    )
    db.add(event)
    db.commit()
    db.refresh(event)
    
    # Convert date to string for response
    event_date_str = event.event_date.strftime("%Y-%m-%d") if hasattr(event.event_date, 'strftime') else str(event.event_date)
    created_at_str = event.created_at.isoformat() if hasattr(event.created_at, 'isoformat') else str(event.created_at)
    
    return EventResponse(
        id=event.id,
        title=event.title,
        description=event.description or "",
        city=event.city,
        location=event.location or "",
        category=event.category,
        event_date=event_date_str,
        start_time=event.start_time,
        end_time=event.end_time,
        organizer_name=event.organizer_name,
        organizer_contact=event.organizer_contact,
        is_verified=event.is_verified,
        is_featured=is_featured,
        created_at=created_at_str
    )


@router.get("/")
async def get_events(
    city: Optional[str] = None,
    category: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get events with optional filters"""
    query = db.query(Event)
    
    if city:
        query = query.filter(Event.city == city)
    if category:
        query = query.filter(Event.category == category)
    
    # Only show future events
    query = query.filter(Event.event_date >= datetime.now().date())
    events = query.order_by(Event.event_date).all()
    
    return {
        "events": [
            {
                "id": e.id,
                "title": e.title,
                "description": e.description,
                "city": e.city,
                "location": e.location,
                "category": e.category,
                "event_date": str(e.event_date),
                "start_time": e.start_time,
                "end_time": e.end_time,
                "organizer_name": e.organizer_name,
                "organizer_contact": e.organizer_contact,
                "is_verified": e.is_verified
            }
            for e in events
        ]
    }


@router.get("/{event_id}")
async def get_event(event_id: int, db: Session = Depends(get_db)):
    """Get a specific event by ID"""
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    return {
        "id": event.id,
        "title": event.title,
        "description": event.description,
        "city": event.city,
        "location": event.location,
        "category": event.category,
        "event_date": str(event.event_date),
        "start_time": event.start_time,
        "end_time": event.end_time,
        "organizer_name": event.organizer_name,
        "organizer_contact": event.organizer_contact,
        "is_verified": event.is_verified
    }


@router.delete("/{event_id}")
async def delete_event(event_id: int, db: Session = Depends(get_db)):
    """Delete an event"""
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    db.delete(event)
    db.commit()
    return {"success": True, "message": "Event deleted"}
