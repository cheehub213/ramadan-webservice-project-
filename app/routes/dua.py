from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.dua import DuaRequest, DuaCategory
from app.schemas.dua import (
    DuaGeneratorRequest,
    DuaGeneratedResponse,
    DuaGeneratorResponse,
    DuaFeedbackRequest,
    DuaCategoryResponse,
    DuaHistoryResponse,
)
from typing import List, Optional
from datetime import datetime
import json

# Import Deepseek Service
from app.services import DeepseekService

router = APIRouter(prefix="/api/v1/dua", tags=["dua-generator"])


# ==================== DUA GENERATOR ENDPOINTS ====================

@router.post("/generate", response_model=DuaGeneratedResponse)
async def generate_personalized_dua(
    request_data: DuaGeneratorRequest,
    db: Session = Depends(get_db)
) -> DuaGeneratedResponse:
    """
    Generate a personalized dua (supplication) based on user's problem
    
    This endpoint creates a heartfelt, personalized Islamic supplication tailored 
    to the user's specific situation and problem.
    
    Request Body:
    - problem_description: Detailed description of the problem/situation (required, min 20 chars)
    - problem_category: Category of problem (Family, Health, Work, Finance, Spiritual, Education, Relationships, Personal Growth)
    - user_email: User's email for history tracking (optional)
    - user_name: User's name (optional)
    - language: Language for response (default: "English", can be "Arabic" or "Bilingual")
    
    Returns:
    - Generated personalized dua tailored to the user's problem
    - How to recite it and when to use it
    - Stored in user's history for later reference
    
    Note: To get Quranic verses (Aya) and Hadiths, use the /api/v1/search/answer endpoint
    """
    try:
        # Validate problem description length
        if len(request_data.problem_description) < 20:
            raise HTTPException(
                status_code=400,
                detail="Problem description must be at least 20 characters long"
            )
        
        # Build prompt for Deepseek to generate a bilingual dua (English + Arabic)
        prompt = f"""Generate a personalized Islamic dua (supplication) based on this problem.
Produce both an English and an Arabic version.

Problem: {request_data.problem_description}
Category: {request_data.problem_category or 'General'}

Please provide EXACTLY in this JSON format (no other text):
{{
  "dua_text_en": "A heartfelt, personalized dua/supplication in English asking Allah for help. Make it personal and directly address the user's concern with specific words relevant to their problem.",
  "dua_text_ar": "A heartfelt, personalized dua/supplication in Arabic asking Allah for help. Make it personal and directly address the user's concern with specific words relevant to their problem.",
  "how_to_use_en": "Brief instructions in English on how and when to recite this dua (e.g., daily, after Fajr prayer, etc.)",
  "how_to_use_ar": "Brief instructions in Arabic on how and when to recite this dua"
}}

Guidelines:
- Make both versions authentic and respectful of Islamic teachings.
- Ensure the Arabic version uses clear, simple Modern Standard Arabic.
- Keep both versions concise and directly applicable to the user's problem.
"""

        # Get response from Deepseek
        deepseek_service = DeepseekService()
        try:
            deepseek_response_text = await deepseek_service._call_deepseek_api(prompt)
        except Exception as e:
            # Fallback response if API fails
            print(f"Deepseek API error: {e}")
            # Provide both English and Arabic fallback dua
            deepseek_response_text = json.dumps({
                "dua_text_en": f"O Allah, I turn to You seeking help with my concern about {request_data.problem_category or 'this matter'}. Grant me wisdom, patience, and strength to overcome these challenges. Help me with sincere intentions and make this an opportunity for growth. I trust in Your mercy and guidance. Ameen.",
                "dua_text_ar": f"اللهم إني ألجأ إليك في كربتي بشأن {request_data.problem_category or 'هذا الأمر'}. امنحني الحكمة والصبر والقوة لتجاوز هذه المحن. أعِنّي على نية صادقة واجعلها فرصة للنمو. إني أتوكّل على رحمتك وهدايتك، آمين.",
                "how_to_use_en": "Recite this dua daily, preferably after prayer. You may also recite it whenever you feel overwhelmed.",
                "how_to_use_ar": "كرر هذا الدعاء يومياً ويفضل بعد الصلاة. يمكنك ترديده عندما تشعر بالضغط أو القلق."
            })

        # Prepare fallback content
        fallback_dua_en = f"O Allah, I turn to You seeking help with my concern about {request_data.problem_category or 'this matter'}. Grant me wisdom, patience, and strength to overcome these challenges. Help me with sincere intentions and make this an opportunity for growth. I trust in Your mercy and guidance. Ameen."
        fallback_dua_ar = f"اللهم إني ألجأ إليك في كربتي بشأن {request_data.problem_category or 'هذا الأمر'}. امنحني الحكمة والصبر والقوة لتجاوز هذه المحن. أعِنّي على نية صادقة واجعلها فرصة للنمو. إني أتوكّل على رحمتك وهدايتك، آمين."
        fallback_how_en = "Recite this dua daily, preferably after prayer. You may also recite it whenever you feel overwhelmed."
        fallback_how_ar = "كرر هذا الدعاء يومياً ويفضل بعد الصلاة. يمكنك ترديده عندما تشعر بالضغط أو القلق."

        # Parse the response
        dua_en = ""
        dua_ar = ""
        how_en = fallback_how_en
        how_ar = fallback_how_ar

        try:
            # Extract JSON from response
            json_start = deepseek_response_text.find('{')
            json_end = deepseek_response_text.rfind('}') + 1
            if json_start >= 0 and json_end > json_start:
                json_str = deepseek_response_text[json_start:json_end]
                parsed_response = json.loads(json_str)
            else:
                parsed_response = json.loads(deepseek_response_text)

            dua_en = parsed_response.get('dua_text_en') or parsed_response.get('dua_text') or fallback_dua_en
            dua_ar = parsed_response.get('dua_text_ar') or '' or fallback_dua_ar
            how_en = parsed_response.get('how_to_use_en') or fallback_how_en
            how_ar = parsed_response.get('how_to_use_ar') or fallback_how_ar

        except (json.JSONDecodeError, KeyError, ValueError) as e:
            # Fallback if parsing fails
            dua_en = fallback_dua_en
            dua_ar = fallback_dua_ar
            how_en = fallback_how_en
            how_ar = fallback_how_ar

        # Store request in database - store bilingual dua as JSON string in generated_dua
        dua_request = DuaRequest(
            user_email=request_data.user_email or 'anonymous',
            user_name=request_data.user_name or 'User',
            problem_description=request_data.problem_description,
            problem_category=request_data.problem_category,
            language=request_data.language,
            generated_dua=json.dumps({"en": dua_en, "ar": dua_ar}),
            deepseek_prompt=prompt,
            deepseek_response=deepseek_response_text,
        )

        db.add(dua_request)
        db.commit()
        db.refresh(dua_request)

        return DuaGeneratedResponse(
            id=dua_request.id,
            user_email=dua_request.user_email,
            user_name=dua_request.user_name,
            problem_description=dua_request.problem_description,
            problem_category=dua_request.problem_category,
            language=dua_request.language,
            dua_text_en=dua_en,
            dua_text_ar=dua_ar,
            how_to_use_en=how_en,
            how_to_use_ar=how_ar,
            created_at=dua_request.created_at,
        )
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error generating dua: {str(e)}")


@router.get("/history/{user_email}", response_model=List[DuaHistoryResponse])
async def get_dua_history(
    user_email: str,
    limit: int = Query(10, ge=1, le=100, description="Number of records to return"),
    db: Session = Depends(get_db)
) -> List[DuaHistoryResponse]:
    """
    Get user's dua generation history
    
    Parameters:
    - user_email: User's email address
    - limit: Number of records to return (default: 10, max: 100)
    """
    try:
        requests = db.query(DuaRequest).filter(
            DuaRequest.user_email == user_email
        ).order_by(DuaRequest.created_at.desc()).limit(limit).all()
        
        history = []
        for req in requests:
            # Parse stored generated_dua JSON (en/ar)
            dua_en = ""
            dua_ar = ""
            try:
                parsed = json.loads(req.generated_dua or '{}')
                dua_en = parsed.get('en', '')
                dua_ar = parsed.get('ar', '')
            except Exception:
                dua_en = req.generated_dua or ''
                dua_ar = ''

            history.append(
                DuaHistoryResponse(
                    id=req.id,
                    problem_description=req.problem_description,
                    problem_category=req.problem_category,
                    generated_dua_en=dua_en,
                    generated_dua_ar=dua_ar,
                    is_helpful=req.is_helpful,
                    created_at=req.created_at,
                )
            )
        return history
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching history: {str(e)}")


@router.post("/feedback")
async def submit_dua_feedback(
    feedback: DuaFeedbackRequest,
    db: Session = Depends(get_db)
) -> dict:
    """
    Submit feedback on a generated dua
    
    Request Body:
    - dua_request_id: ID of the dua request
    - is_helpful: "yes" or "no"
    - feedback: Additional comments (optional)
    """
    try:
        dua_request = db.query(DuaRequest).filter(
            DuaRequest.id == feedback.dua_request_id
        ).first()
        
        if not dua_request:
            raise HTTPException(status_code=404, detail="Dua request not found")
        
        dua_request.is_helpful = feedback.is_helpful
        dua_request.user_feedback = feedback.feedback
        dua_request.updated_at = datetime.utcnow()
        
        db.commit()
        
        return {"status": "success", "message": "Feedback recorded"}
    
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error submitting feedback: {str(e)}")


@router.get("/categories", response_model=List[DuaCategoryResponse])
async def get_dua_categories(db: Session = Depends(get_db)) -> List[DuaCategoryResponse]:
    """Get all available dua problem categories"""
    try:
        categories = db.query(DuaCategory).all()
        
        if not categories:
            # Create default categories if not exist
            default_categories = [
                DuaCategory(
                    name="Family",
                    description="Family relationships, marriage, children, parents",
                    icon="👨‍👩‍👧‍👦",
                    example_problems="Marital issues, communication problems, parenting challenges"
                ),
                DuaCategory(
                    name="Health",
                    description="Physical and mental health concerns",
                    icon="🏥",
                    example_problems="Illness, anxiety, stress, recovery"
                ),
                DuaCategory(
                    name="Work & Career",
                    description="Job, career, business, wealth",
                    icon="💼",
                    example_problems="Job search, career transition, business decisions"
                ),
                DuaCategory(
                    name="Finance",
                    description="Financial difficulties and decisions",
                    icon="💰",
                    example_problems="Debt, poverty, financial hardship"
                ),
                DuaCategory(
                    name="Spiritual",
                    description="Spiritual growth, faith, guidance",
                    icon="🤲",
                    example_problems="Weak faith, guidance, spiritual improvement"
                ),
                DuaCategory(
                    name="Education",
                    description="Studies, learning, academic challenges",
                    icon="📚",
                    example_problems="Exam anxiety, learning difficulties, knowledge"
                ),
                DuaCategory(
                    name="Relationships",
                    description="Friendships, social connections",
                    icon="👫",
                    example_problems="Friendship problems, loneliness, social anxiety"
                ),
                DuaCategory(
                    name="Personal Growth",
                    description="Self-improvement, character development",
                    icon="🌱",
                    example_problems="Building good habits, overcoming weaknesses"
                ),
            ]
            
            db.add_all(default_categories)
            db.commit()
            categories = default_categories
        
        return categories
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching categories: {str(e)}")


@router.get("/{dua_request_id}", response_model=DuaGeneratedResponse)
async def get_dua_request(dua_request_id: int, db: Session = Depends(get_db)) -> DuaGeneratedResponse:
    """Get a specific dua request with its generated content"""
    try:
        dua_request = db.query(DuaRequest).filter(
            DuaRequest.id == dua_request_id
        ).first()
        
        if not dua_request:
            raise HTTPException(status_code=404, detail="Dua request not found")
        
        # Parse stored bilingual dua JSON
        dua_en = ""
        dua_ar = ""
        how_en = "Recite with sincere intention"
        how_ar = "كرر هذا الدعاء بنية خالصة"

        try:
            parsed_dua = json.loads(dua_request.generated_dua or '{}')
            dua_en = parsed_dua.get('en', '')
            dua_ar = parsed_dua.get('ar', '')
        except Exception:
            dua_en = dua_request.generated_dua or ''
            dua_ar = ''

        try:
            parsed_resp = json.loads(dua_request.deepseek_response or '{}')
            how_en = parsed_resp.get('how_to_use_en', how_en)
            how_ar = parsed_resp.get('how_to_use_ar', how_ar)
        except Exception:
            pass

        return DuaGeneratedResponse(
            id=dua_request.id,
            user_email=dua_request.user_email,
            user_name=dua_request.user_name,
            problem_description=dua_request.problem_description,
            problem_category=dua_request.problem_category,
            language=dua_request.language or "English",
            dua_text_en=dua_en,
            dua_text_ar=dua_ar,
            how_to_use_en=how_en,
            how_to_use_ar=how_ar,
            created_at=dua_request.created_at,
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching dua request: {str(e)}")


@router.get("/stats/helpful")
async def get_helpful_duas_stats(db: Session = Depends(get_db)) -> dict:
    """Get statistics on helpful duas"""
    try:
        total = db.query(DuaRequest).count()
        helpful = db.query(DuaRequest).filter(DuaRequest.is_helpful == "yes").count()
        not_helpful = db.query(DuaRequest).filter(DuaRequest.is_helpful == "no").count()
        
        helpful_percentage = (helpful / total * 100) if total > 0 else 0
        
        return {
            "total_requests": total,
            "helpful": helpful,
            "not_helpful": not_helpful,
            "helpful_percentage": round(helpful_percentage, 2),
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching stats: {str(e)}")
