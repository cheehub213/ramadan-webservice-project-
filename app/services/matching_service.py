from sqlalchemy.orm import Session
from sqlalchemy import or_, func
from app.models import QuranArabic, QuranEnglish, Hadith
from typing import List, Dict, Tuple, Optional
import difflib

class MatchingService:
    """Service to match user problems with relevant Quran verses and Hadiths"""
    
    @staticmethod
    def match_quran_verses(
        db: Session,
        topics: List[str],
        keywords: List[str],
        language: str = "en",
        limit: int = 5
    ) -> List:
        """
        Match user topics/keywords with Quran verses
        Returns verses most relevant to the identified topics
        Language can be "en", "ar", or "both"
        """
        
        if not topics and not keywords:
            return []
        
        results = []
        
        # If asking for both languages, search both models
        if language == "both":
            for lang in ["en", "ar"]:
                model = QuranEnglish if lang == "en" else QuranArabic
                
                if topics:
                    for topic in topics:
                        verses = db.query(model).filter(
                            func.lower(model.topic).contains(func.lower(topic))
                        ).limit(limit).all()
                        results.extend(verses)
                
                if keywords:
                    for keyword in keywords[:5]:
                        verses = db.query(model).filter(
                            or_(
                                func.lower(model.ayah_text).contains(func.lower(keyword)),
                                func.lower(model.surah_name).contains(func.lower(keyword))
                            )
                        ).limit(limit).all()
                        results.extend(verses)
        else:
            # Single language search
            model = QuranEnglish if language == "en" else QuranArabic
            
            if topics:
                for topic in topics:
                    verses = db.query(model).filter(
                        func.lower(model.topic).contains(func.lower(topic))
                    ).limit(limit).all()
                    results.extend(verses)
            
            if keywords:
                for keyword in keywords[:5]:
                    verses = db.query(model).filter(
                        or_(
                            func.lower(model.ayah_text).contains(func.lower(keyword)),
                            func.lower(model.surah_name).contains(func.lower(keyword))
                        )
                    ).limit(limit).all()
                    results.extend(verses)
        
        # Remove duplicates while preserving order
        seen = set()
        unique_results = []
        for verse in results:
            if verse.id not in seen:
                seen.add(verse.id)
                unique_results.append(verse)
        
        return unique_results[:limit]
    
    @staticmethod
    def match_hadiths(
        db: Session,
        topics: List[str],
        keywords: List[str],
        limit: int = 5
    ) -> List[Hadith]:
        """
        Match user topics/keywords with relevant Hadiths
        Returns hadiths most relevant to the identified topics
        """
        
        if not topics and not keywords:
            return []
        
        results = []
        
        # Search by topic first
        if topics:
            for topic in topics:
                hadiths = db.query(Hadith).filter(
                    func.lower(Hadith.topic).contains(func.lower(topic))
                ).limit(limit).all()
                results.extend(hadiths)
        
        # Also search in hadith text
        if keywords:
            for keyword in keywords[:5]:
                hadiths = db.query(Hadith).filter(
                    or_(
                        func.lower(Hadith.hadith_text_english).contains(func.lower(keyword)),
                        func.lower(Hadith.hadith_text_arabic).contains(func.lower(keyword))
                    )
                ).limit(limit).all()
                results.extend(hadiths)
        
        # Remove duplicates
        seen = set()
        unique_results = []
        for hadith in results:
            if hadith.id not in seen:
                seen.add(hadith.id)
                unique_results.append(hadith)
        
        return unique_results[:limit]
    
    @staticmethod
    def get_matched_keywords(
        text: str,
        keywords: List[str]
    ) -> List[str]:
        """Find which keywords actually matched in the text"""
        matched = []
        text_lower = text.lower()
        
        for keyword in keywords:
            if keyword.lower() in text_lower:
                matched.append(keyword)
        
        return matched
    
    @staticmethod
    def calculate_relevance_score(
        text: str,
        keywords: List[str],
        topic_matched: bool = False
    ) -> float:
        """
        Calculate relevance score (0-1) based on keyword matches
        topic_matched: if True, boosts score (topic-based matches are more relevant)
        """
        if not keywords or not text:
            return 0.0
        
        text_lower = text.lower()
        total_weight = len(keywords)
        matched_weight = 0
        
        for keyword in keywords:
            if keyword.lower() in text_lower:
                # Count occurrences for better scoring
                occurrences = text_lower.count(keyword.lower())
                matched_weight += min(occurrences, 3)  # Cap at 3 occurrences
        
        score = matched_weight / (total_weight * 3) if total_weight > 0 else 0
        
        # Boost score if topic was matched
        if topic_matched:
            score = min(score * 1.2, 1.0)
        
        return round(score, 3)
    
    @staticmethod
    def rank_by_relevance(
        items: List,
        keywords: List[str],
        limit: int = 3
    ) -> List:
        """
        Rank items by relevance to keywords using similarity scoring
        Returns items with attached scoring information
        """
        if not keywords or not items:
            return items[:limit]
        
        scored_items = []
        
        for item in items:
            # Get the text to compare
            if hasattr(item, 'ayah_text'):
                text = item.ayah_text
            elif hasattr(item, 'hadith_text_english'):
                text = item.hadith_text_english
            else:
                text = ""
            
            # Calculate relevance score and matched keywords
            matched_kw = MatchingService.get_matched_keywords(text, keywords)
            score = MatchingService.calculate_relevance_score(text, keywords, bool(matched_kw))
            
            # Attach metadata to item
            item.relevance_score = score
            item.matched_keywords = matched_kw
            
            scored_items.append((item, score))
        
        # Sort by score (descending) and return top items
        sorted_items = sorted(scored_items, key=lambda x: x[1], reverse=True)
        return [item for item, score in sorted_items[:limit]]
