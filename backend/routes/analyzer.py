"""
AI Analyzer Routes - Protected endpoints requiring authentication
"""
from fastapi import APIRouter, HTTPException, Depends
from schemas.analyzer import AnalyzeRequest, AnalyzeResponse
from services_ai_analyzer import AIAnalyzerService
from .auth import get_current_user
from models_extended import User

router = APIRouter()

# Initialize the service
analyzer_service = AIAnalyzerService()


@router.post("/")
@router.post("/analyze")
async def analyze_text(
    request: AnalyzeRequest,
    current_user: User = Depends(get_current_user)
):
    """Analyze text using AI (requires authentication)"""
    try:
        result = await analyzer_service.analyze(request.question)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/semantic-search")
async def semantic_search(
    request: AnalyzeRequest,
    current_user: User = Depends(get_current_user)
):
    """Search Quran verses semantically (requires authentication)"""
    try:
        from services_quran_search import search_quran_by_topic
        results = await search_quran_by_topic(request.question)
        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
