"""
AI Analyzer Routes
"""
from fastapi import APIRouter, HTTPException
from schemas.analyzer import AnalyzeRequest, AnalyzeResponse
from services_ai_analyzer import AIAnalyzerService

router = APIRouter()

# Initialize the service
analyzer_service = AIAnalyzerService()


@router.post("/")
@router.post("/analyze")
async def analyze_text(request: AnalyzeRequest):
    """Analyze text using AI - public endpoint"""
    try:
        result = await analyzer_service.analyze(request.question)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/semantic-search")
async def semantic_search(request: AnalyzeRequest):
    """Search Quran verses semantically - public endpoint"""
    try:
        from services_quran_search import search_quran_by_topic
        results = await search_quran_by_topic(request.question)
        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
