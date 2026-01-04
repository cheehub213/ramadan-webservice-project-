from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import SearchRequest
from app.services import DeepseekService, MatchingService
from typing import Dict, List

router = APIRouter(prefix="/api/v1/search", tags=["search"])

@router.post("/answer")
async def find_answer(
    request: SearchRequest,
    db: Session = Depends(get_db)
) -> Dict:
    """
    Main endpoint: Accept user problem/prompt in English or Arabic and return relevant guidance
    
    Features:
    - Accepts prompts in English or Arabic (auto-detects language)
    - Returns responses in English, Arabic, or both (bilingual)
    - Includes explanations for why each verse/hadith was chosen
    - Shows relevance scores and matched keywords
    
    Process:
    1. Detect prompt language (English or Arabic)
    2. Send to Deepseek to analyze and extract topics/keywords
    3. Search database for matching Quran verses and/or Hadiths
    4. Generate explanations for selected results
    5. Return ranked results with detailed information
    """
    try:
        # Step 1: Analyze prompt with Deepseek (handles both languages)
        deepseek_service = DeepseekService()
        analysis = await deepseek_service.analyze_prompt(request.prompt)
        
        topics = analysis.get("topics", [])
        keywords = analysis.get("keywords", [])
        prompt_language = analysis.get("prompt_language", "en")
        
        quran_results = []
        hadith_results = []
        
        # Step 2: Match with Quran verses
        if request.include_quran:
            # Determine which language versions to retrieve
            verse_language = "both" if request.response_language == "bilingual" else request.response_language
            
            quran_results = MatchingService.match_quran_verses(
                db=db,
                topics=topics,
                keywords=keywords,
                language=verse_language,
                limit=3
            )
            
            # Rank by relevance
            quran_results = MatchingService.rank_by_relevance(
                quran_results,
                keywords,
                limit=3
            )
        
        # Step 3: Match with Hadiths
        if request.include_hadith:
            hadith_results = MatchingService.match_hadiths(
                db=db,
                topics=topics,
                keywords=keywords,
                limit=3
            )
            
            # Rank by relevance
            hadith_results = MatchingService.rank_by_relevance(
                hadith_results,
                keywords,
                limit=3
            )
        
        # Step 4: Generate explanations for each result
        quran_verse_responses = []
        for verse in quran_results:
            verse_text = verse.ayah_text
            explanation = await deepseek_service.generate_explanation(
                request.prompt,
                verse_text,
                "Quranic verse"
            )
            
            verse_response = {
                "surah_number": verse.surah_number,
                "surah_name": verse.surah_name,
                "ayah_number": verse.ayah_number,
            }
            
            if request.response_language in ["en", "bilingual"]:
                verse_response["ayah_text_english"] = verse_text
                verse_response["explanation_english"] = explanation.get("explanation_english", "")
            
            if request.response_language in ["ar", "bilingual"]:
                # Fetch Arabic version if not already loaded
                if hasattr(verse, 'ayah_text_arabic'):
                    verse_response["ayah_text_arabic"] = verse.ayah_text_arabic
                verse_response["explanation_arabic"] = explanation.get("explanation_arabic", "")
            
            verse_response["relevance_score"] = getattr(verse, 'relevance_score', 0.0)
            verse_response["matched_keywords"] = getattr(verse, 'matched_keywords', [])
            
            quran_verse_responses.append(verse_response)
        
        hadith_responses = []
        for hadith in hadith_results:
            hadith_text = hadith.hadith_text_english
            explanation = await deepseek_service.generate_explanation(
                request.prompt,
                hadith_text,
                "Hadith"
            )
            
            hadith_response = {
                "hadith_number": hadith.hadith_number,
                "narrator": hadith.narrator,
                "source": hadith.source,
            }
            
            if request.response_language in ["en", "bilingual"]:
                hadith_response["hadith_text_english"] = hadith.hadith_text_english
                hadith_response["explanation_english"] = explanation.get("explanation_english", "")
            
            if request.response_language in ["ar", "bilingual"]:
                hadith_response["hadith_text_arabic"] = hadith.hadith_text_arabic
                hadith_response["explanation_arabic"] = explanation.get("explanation_arabic", "")
            
            hadith_response["relevance_score"] = getattr(hadith, 'relevance_score', 0.0)
            hadith_response["matched_keywords"] = getattr(hadith, 'matched_keywords', [])
            
            hadith_responses.append(hadith_response)
        
        # Step 5: Build comprehensive response
        response = {
            "status": "success",
            "user_prompt": request.prompt,
            "prompt_language": prompt_language,
            "response_language": request.response_language,
            "analysis": {
                "topics": topics,
                "keywords": keywords,
                "emotion": analysis.get("emotion", "neutral"),
                "summary": analysis.get("summary", "")
            },
            "results": {
                "quran_verses": quran_verse_responses,
                "hadiths": hadith_responses
            }
        }
        
        return response
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"Error processing request: {str(e)}"
        )

@router.get("/quran")
async def search_quran(
    keywords: str,
    response_language: str = "en",
    limit: int = 5,
    db: Session = Depends(get_db)
) -> Dict:
    """
    Direct Quran search by keywords
    
    Parameters:
    - keywords: Comma-separated keywords to search for
    - response_language: "en", "ar", or "bilingual" (default: "en")
    - limit: Maximum number of results (default: 5)
    """
    try:
        keyword_list = keywords.split(",")
        language = "both" if response_language == "bilingual" else response_language
        
        results = MatchingService.match_quran_verses(
            db=db,
            topics=[],
            keywords=keyword_list,
            language=language,
            limit=limit
        )
        
        # Rank by relevance
        results = MatchingService.rank_by_relevance(results, keyword_list, limit=limit)
        
        formatted_results = []
        for verse in results:
            result_item = {
                "surah": verse.surah_name,
                "surah_number": verse.surah_number,
                "ayah_number": verse.ayah_number,
                "matched_keywords": getattr(verse, 'matched_keywords', []),
                "relevance_score": getattr(verse, 'relevance_score', 0.0)
            }
            
            if response_language in ["en", "bilingual"]:
                result_item["text_english"] = verse.ayah_text
            
            if response_language in ["ar", "bilingual"] and hasattr(verse, 'ayah_text_arabic'):
                result_item["text_arabic"] = verse.ayah_text_arabic
            
            formatted_results.append(result_item)
        
        return {
            "status": "success",
            "query": keywords,
            "response_language": response_language,
            "total_results": len(formatted_results),
            "results": formatted_results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/hadith")
async def search_hadith(
    keywords: str,
    response_language: str = "bilingual",
    limit: int = 5,
    db: Session = Depends(get_db)
) -> Dict:
    """
    Direct Hadith search by keywords
    
    Parameters:
    - keywords: Comma-separated keywords to search for
    - response_language: "en", "ar", or "bilingual" (default: "bilingual")
    - limit: Maximum number of results (default: 5)
    """
    try:
        keyword_list = keywords.split(",")
        results = MatchingService.match_hadiths(
            db=db,
            topics=[],
            keywords=keyword_list,
            limit=limit
        )
        
        # Rank by relevance
        results = MatchingService.rank_by_relevance(results, keyword_list, limit=limit)
        
        formatted_results = []
        for hadith in results:
            result_item = {
                "hadith_number": hadith.hadith_number,
                "narrator": hadith.narrator,
                "source": hadith.source,
                "matched_keywords": getattr(hadith, 'matched_keywords', []),
                "relevance_score": getattr(hadith, 'relevance_score', 0.0)
            }
            
            if response_language in ["en", "bilingual"]:
                result_item["text_english"] = hadith.hadith_text_english
            
            if response_language in ["ar", "bilingual"]:
                result_item["text_arabic"] = hadith.hadith_text_arabic
            
            formatted_results.append(result_item)
        
        return {
            "status": "success",
            "query": keywords,
            "response_language": response_language,
            "total_results": len(formatted_results),
            "results": formatted_results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
