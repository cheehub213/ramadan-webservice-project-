"""
Events Schemas (Tunisia-focused)
"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


# Tunisia cities list
TUNISIA_CITIES = [
    "Tunis", "Sfax", "Sousse", "Kairouan", "Bizerte",
    "Gabès", "Ariana", "Gafsa", "Monastir", "Ben Arous",
    "Kasserine", "Médenine", "Nabeul", "Tataouine", "Béja",
    "Jendouba", "Mahdia", "Sidi Bouzid", "Tozeur", "Siliana",
    "Kébili", "Zaghouan", "Manouba", "Le Kef"
]

EVENT_CATEGORIES = ["iftar", "tarawih", "charity", "lecture", "quran", "children", "other"]


class EventCreateRequest(BaseModel):
    """Request to create an event"""
    title: str
    description: Optional[str] = ""
    city: str
    location: Optional[str] = ""
    category: str
    event_date: str
    event_time: Optional[str] = None  # Frontend sends event_time
    start_time: Optional[str] = None  # Also accept start_time
    end_time: Optional[str] = None
    organizer_name: Optional[str] = None
    organizer_contact: Optional[str] = None  
    contact_info: Optional[str] = None  # Frontend sends contact_info
    contact_phone: Optional[str] = None
    is_featured: bool = False
    listing_type: str = "basic"  # "basic" or "featured"


class EventResponse(BaseModel):
    """Event response"""
    id: int
    title: str
    description: Optional[str] = ""
    city: str
    location: Optional[str] = ""
    category: str
    event_date: str
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    organizer_name: Optional[str] = None
    organizer_contact: Optional[str] = None
    is_verified: bool = False
    is_featured: bool = False
    created_at: Optional[str] = None  # String for JSON serialization

    class Config:
        from_attributes = True
