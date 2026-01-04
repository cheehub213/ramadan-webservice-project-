from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.imam import Imam, Consultation
from app.schemas.imam import (
    ImamCreate,
    ImamResponse,
    ImamListResponse,
    ConsultationRequest,
    ConsultationResponse,
    ConsultationDetailResponse,
    ConsultationListResponse,
    ConsultationRatingRequest,
    ConsultationConfirmRequest,
    ConsultationCompleteRequest,
)
from typing import List, Optional
from datetime import datetime

router = APIRouter(prefix="/api/v1/imam", tags=["imam-consultation"])


# ==================== IMAM ENDPOINTS ====================

@router.get("/imams", response_model=List[ImamListResponse])
async def list_imams(
    specialization: Optional[str] = Query(None, description="Filter by specialization"),
    madhab: Optional[str] = Query(None, description="Filter by madhab"),
    available_only: bool = Query(True, description="Show only available imams"),
    min_rating: float = Query(0.0, ge=0.0, le=5.0, description="Minimum rating filter"),
    db: Session = Depends(get_db)
) -> List[ImamListResponse]:
    """
    Get list of available imams for consultation
    
    Query Parameters:
    - specialization: Filter by expertise (general, fiqh, quran, hadith, family, youth, business, spirituality, madhab)
    - madhab: Filter by Islamic school (Hanafi, Maliki, Shafi'i, Hanbali)
    - available_only: Show only currently available imams (default: true)
    - min_rating: Filter by minimum rating (0.0 - 5.0)
    
    Example:
    GET /api/v1/imam/imams?specialization=family&madhab=Hanafi&min_rating=4.5
    """
    try:
        query = db.query(Imam)
        
        if available_only:
            query = query.filter(Imam.is_available == True)
        
        if specialization:
            query = query.filter(Imam.specializations.ilike(f"%{specialization}%"))
        
        if madhab:
            query = query.filter(Imam.madhab == madhab)
        
        if min_rating > 0:
            query = query.filter(Imam.average_rating >= min_rating)
        
        imams = query.order_by(Imam.average_rating.desc()).all()
        
        return imams
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching imams: {str(e)}")


@router.post("/imams", response_model=ImamResponse)
async def register_imam(imam_data: ImamCreate, db: Session = Depends(get_db)) -> ImamResponse:
    """
    Register a new imam to the platform
    
    Request Body:
    - name: Imam's full name (required)
    - title: Title (e.g., "Dr.", "Mufti", "Sheikh") (optional)
    - specializations: Comma-separated specializations (required)
      Examples: "general", "fiqh", "quran", "hadith", "family", "youth", "business", "spirituality", "madhab"
    - madhab: Islamic school (Hanafi, Maliki, Shafi'i, Hanbali) (optional)
    - bio: Biography/description of imam (optional)
    - years_experience: Years of Islamic knowledge (optional)
    - qualifications: Educational qualifications (optional)
    - email: Email address - must be unique (required)
    - phone: Phone number (optional)
    - website: Personal website (optional)
    - consultation_methods: Comma-separated methods offered (required)
      Examples: "phone", "email", "video", "in_person", "messaging"
    - consultation_fee: Hourly or per-session fee (optional, default: 0)
    - currency: Currency for consultation fee (default: USD)
    - languages: Comma-separated languages spoken (required)
      Examples: "English", "Arabic", "Urdu", "French"
    - timezone: Imam's timezone for scheduling (optional)
    - is_available: Currently available for consultations (optional, default: true)
    - verified: Admin-verified badge (optional, default: false)
    """
    try:
        # Check if email already exists
        existing_imam = db.query(Imam).filter(Imam.email == imam_data.email).first()
        if existing_imam:
            raise HTTPException(
                status_code=400,
                detail=f"Imam with email '{imam_data.email}' already registered"
            )
        
        # Create new imam
        new_imam = Imam(
            name=imam_data.name,
            title=imam_data.title,
            specializations=imam_data.specializations,
            madhab=imam_data.madhab,
            bio=imam_data.bio,
            years_experience=imam_data.years_experience,
            qualifications=imam_data.qualifications,
            email=imam_data.email,
            phone=imam_data.phone,
            website=imam_data.website,
            consultation_methods=imam_data.consultation_methods,
            consultation_fee=imam_data.consultation_fee or 0.0,
            currency=imam_data.currency or "USD",
            is_available=imam_data.is_available if imam_data.is_available is not None else True,
            languages=imam_data.languages,
            timezone=imam_data.timezone,
            verified=imam_data.verified or False,
            average_rating=5.0,  # New imams start with perfect rating
            total_consultations=0,
            total_reviews=0,
        )
        
        db.add(new_imam)
        db.commit()
        db.refresh(new_imam)
        
        return new_imam
    
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error registering imam: {str(e)}")


@router.get("/imams/{imam_id}", response_model=ImamResponse)
async def get_imam(imam_id: int, db: Session = Depends(get_db)) -> ImamResponse:
    """
    Get detailed information about a specific imam
    
    Parameters:
    - imam_id: ID of the imam to retrieve
    """
    try:
        imam = db.query(Imam).filter(Imam.id == imam_id).first()
        
        if not imam:
            raise HTTPException(status_code=404, detail="Imam not found")
        
        return imam
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching imam: {str(e)}")


@router.get("/imams/by-specialization/{specialization}")
async def get_imams_by_specialization(
    specialization: str,
    db: Session = Depends(get_db)
) -> List[ImamListResponse]:
    """
    Get imams specialized in a specific area
    
    Parameters:
    - specialization: Area of expertise (general, fiqh, quran, hadith, family, youth, business, spirituality, madhab)
    
    Example:
    GET /api/v1/imam/imams/by-specialization/family
    """
    try:
        imams = db.query(Imam).filter(
            Imam.specializations.ilike(f"%{specialization}%"),
            Imam.is_available == True
        ).order_by(Imam.average_rating.desc()).all()
        
        if not imams:
            raise HTTPException(status_code=404, detail=f"No imams found for specialization: {specialization}")
        
        return imams
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


# ==================== CONSULTATION ENDPOINTS ====================

@router.post("/consultations/book", response_model=ConsultationResponse)
async def book_consultation(
    request: ConsultationRequest,
    db: Session = Depends(get_db)
) -> ConsultationResponse:
    """
    Book a consultation with an imam
    
    This endpoint allows users to book direct consultations with imams when:
    - The Deepseek AI response is confusing
    - The answer differs from their Islamic madhab
    - They need more personalized guidance
    
    Request body includes:
    - imam_id: ID of the imam to consult
    - title: Brief title of the concern
    - description: Detailed description of the issue
    - user_email: User's email for contact
    - preferred_method: Consultation method (phone, email, video, in_person, messaging)
    - preferred_date: Preferred date/time (optional)
    - reason_for_consultation: Why seeking imam instead of AI response
    - deepseek_response: The AI response they found insufficient (optional)
    
    Returns the consultation booking with initial status 'pending'
    """
    try:
        # Verify imam exists
        imam = db.query(Imam).filter(Imam.id == request.imam_id).first()
        if not imam:
            raise HTTPException(status_code=404, detail="Imam not found")
        
        # Verify imam is available
        if not imam.is_available:
            raise HTTPException(status_code=400, detail="This imam is not currently available")
        
        # Create consultation booking
        consultation = Consultation(
            imam_id=request.imam_id,
            user_id=request.user_email,
            title=request.title,
            description=request.description,
            category=request.category,
            madhab_preference=request.madhab_preference,
            original_prompt=request.original_prompt,
            deepseek_response=request.deepseek_response,
            reason_for_consultation=request.reason_for_consultation,
            preferred_method=request.preferred_method,
            preferred_date=request.preferred_date,
            duration_minutes=request.duration_minutes,
            status="pending"
        )
        
        db.add(consultation)
        db.commit()
        db.refresh(consultation)
        
        return consultation
    
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error booking consultation: {str(e)}")


@router.get("/consultations/{consultation_id}", response_model=ConsultationDetailResponse)
async def get_consultation(
    consultation_id: int,
    db: Session = Depends(get_db)
) -> ConsultationDetailResponse:
    """
    Get details of a specific consultation booking
    
    Parameters:
    - consultation_id: ID of the consultation
    
    Returns full consultation details including imam notes and resolution
    """
    try:
        consultation = db.query(Consultation).filter(Consultation.id == consultation_id).first()
        
        if not consultation:
            raise HTTPException(status_code=404, detail="Consultation not found")
        
        return consultation
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching consultation: {str(e)}")


@router.get("/consultations/user/{user_email}", response_model=List[ConsultationListResponse])
async def get_user_consultations(
    user_email: str,
    db: Session = Depends(get_db)
) -> List[ConsultationListResponse]:
    """
    Get all consultations for a specific user
    
    Parameters:
    - user_email: User's email address
    
    Returns list of all consultations (past and pending)
    """
    try:
        consultations = db.query(Consultation).filter(
            Consultation.user_id == user_email
        ).order_by(Consultation.created_at.desc()).all()
        
        return consultations
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching consultations: {str(e)}")


@router.put("/consultations/{consultation_id}/rate", response_model=ConsultationResponse)
async def rate_consultation(
    consultation_id: int,
    rating_request: ConsultationRatingRequest,
    db: Session = Depends(get_db)
) -> ConsultationResponse:
    """
    Rate and review a completed consultation
    
    Parameters:
    - consultation_id: ID of the consultation
    - rating: Rating from 1-5
    - review: Optional review text
    
    Updates consultation rating and updates imam's average rating
    """
    try:
        consultation = db.query(Consultation).filter(Consultation.id == consultation_id).first()
        
        if not consultation:
            raise HTTPException(status_code=404, detail="Consultation not found")
        
        if consultation.status != "completed":
            raise HTTPException(status_code=400, detail="Only completed consultations can be rated")
        
        if not (1 <= rating_request.rating <= 5):
            raise HTTPException(status_code=400, detail="Rating must be between 1 and 5")
        
        # Update consultation
        consultation.rating = rating_request.rating
        consultation.review = rating_request.review
        
        # Update imam's average rating
        imam = db.query(Imam).filter(Imam.id == consultation.imam_id).first()
        if imam:
            # Recalculate average rating
            all_ratings = db.query(Consultation.rating).filter(
                Consultation.imam_id == imam.id,
                Consultation.rating != None
            ).all()
            
            ratings = [r[0] for r in all_ratings]
            if ratings:
                imam.average_rating = sum(ratings) / len(ratings)
                imam.total_reviews = len(ratings)
        
        db.commit()
        db.refresh(consultation)
        
        return consultation
    
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error rating consultation: {str(e)}")


# ==================== IMAM MANAGEMENT ENDPOINTS ====================

@router.put("/consultations/{consultation_id}/confirm")
async def confirm_consultation(
    consultation_id: int,
    confirm_request: ConsultationConfirmRequest,
    db: Session = Depends(get_db)
) -> ConsultationResponse:
    """
    Imam confirms a consultation booking
    
    Parameters:
    - consultation_id: ID of the consultation
    - status: "confirmed" or "rescheduled"
    - actual_date: Actual date/time of consultation
    - imam_notes: Notes from imam (e.g., contact info, instructions)
    """
    try:
        consultation = db.query(Consultation).filter(Consultation.id == consultation_id).first()
        
        if not consultation:
            raise HTTPException(status_code=404, detail="Consultation not found")
        
        if consultation.status != "pending":
            raise HTTPException(status_code=400, detail="Only pending consultations can be confirmed")
        
        consultation.status = confirm_request.status
        if confirm_request.actual_date:
            consultation.actual_date = confirm_request.actual_date
        if confirm_request.imam_notes:
            consultation.imam_notes = confirm_request.imam_notes
        
        db.commit()
        db.refresh(consultation)
        
        return consultation
    
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error confirming consultation: {str(e)}")


@router.put("/consultations/{consultation_id}/complete")
async def complete_consultation(
    consultation_id: int,
    complete_request: ConsultationCompleteRequest,
    db: Session = Depends(get_db)
) -> ConsultationResponse:
    """
    Imam marks a consultation as completed
    
    Parameters:
    - consultation_id: ID of the consultation
    - imam_notes: Notes from the imam
    - resolution: The guidance/resolution provided
    """
    try:
        consultation = db.query(Consultation).filter(Consultation.id == consultation_id).first()
        
        if not consultation:
            raise HTTPException(status_code=404, detail="Consultation not found")
        
        if consultation.status not in ["pending", "confirmed"]:
            raise HTTPException(status_code=400, detail="Only pending/confirmed consultations can be completed")
        
        consultation.status = "completed"
        consultation.completed_at = datetime.now()
        if complete_request.imam_notes:
            consultation.imam_notes = complete_request.imam_notes
        consultation.resolution = complete_request.resolution
        
        # Increment imam's consultation count
        imam = db.query(Imam).filter(Imam.id == consultation.imam_id).first()
        if imam:
            imam.total_consultations += 1
        
        db.commit()
        db.refresh(consultation)
        
        return consultation
    
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error completing consultation: {str(e)}")


@router.put("/consultations/{consultation_id}/cancel")
async def cancel_consultation(
    consultation_id: int,
    db: Session = Depends(get_db)
) -> ConsultationResponse:
    """
    Cancel a consultation booking
    
    Parameters:
    - consultation_id: ID of the consultation
    """
    try:
        consultation = db.query(Consultation).filter(Consultation.id == consultation_id).first()
        
        if not consultation:
            raise HTTPException(status_code=404, detail="Consultation not found")
        
        if consultation.status == "completed":
            raise HTTPException(status_code=400, detail="Cannot cancel completed consultations")
        
        consultation.status = "cancelled"
        
        db.commit()
        db.refresh(consultation)
        
        return consultation
    
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error cancelling consultation: {str(e)}")
