"""
AI Analyzer Service - Handles Islamic guidance questions
"""
from datetime import datetime

class AnalyzerService:
    
    # Islamic knowledge database
    ISLAMIC_DATABASE = {
        "ayahs": [
            {
                "text_en": "Do not despair of the mercy of Allah. Indeed, Allah forgives all sins.",
                "text_ar": "لا تقنطوا من رحمة الله إن الله يغفر الذنوب جميعا",
                "reference": "Quran 39:53",
                "keywords": ["despair", "mercy", "forgive", "sin", "hope", "faith"]
            },
            {
                "text_en": "With hardship comes ease. Indeed, with hardship comes ease.",
                "text_ar": "فإن مع العسر يسرا إن مع العسر يسرا",
                "reference": "Quran 94:5-6",
                "keywords": ["hardship", "difficulty", "ease", "struggle", "problem", "challenge"]
            },
            {
                "text_en": "Indeed, Allah is with those who are patient.",
                "text_ar": "إن الله مع الصابرين",
                "reference": "Quran 2:153",
                "keywords": ["patient", "patience", "endure", "persist", "strong"]
            },
            {
                "text_en": "Call upon Me; I will respond to you.",
                "text_ar": "ادعوني أستجب لكم",
                "reference": "Quran 40:60",
                "keywords": ["dua", "pray", "call", "ask", "request", "supplication"]
            },
            {
                "text_en": "Indeed, with you is mercy; use it to guide the people.",
                "text_ar": "بك هدى الناس",
                "reference": "Quran 2:185",
                "keywords": ["guidance", "mercy", "compassion", "guide", "help"]
            },
            {
                "text_en": "Take life as it comes and don't worry about tomorrow.",
                "text_ar": "لا تهتم بالغد فاليوم عندك",
                "reference": "Islamic Teaching",
                "keywords": ["worry", "anxiety", "future", "fear", "trust"]
            },
            {
                "text_en": "The best among you are those who are best to their families.",
                "text_ar": "خيركم خير لأهليكم",
                "reference": "Hadith",
                "keywords": ["family", "relationship", "kindness", "parent", "spouse"]
            },
            {
                "text_en": "Seeking knowledge is an obligation on every Muslim.",
                "text_ar": "طلب العلم فريضة على كل مسلم",
                "reference": "Hadith",
                "keywords": ["knowledge", "learning", "education", "study", "wisdom"]
            }
        ],
        "hadiths": [
            {
                "text_en": "The strongest person is the one who controls himself in anger.",
                "text_ar": "الرجل القوي الذي يملك نفسه عند الغضب",
                "reference": "Hadith",
                "keywords": ["anger", "control", "strength", "emotion", "patience"]
            },
            {
                "text_en": "None of you truly believes until he wishes for his brother what he wishes for himself.",
                "text_ar": "لا يؤمن أحدكم حتى يحب لأخيه ما يحب لنفسه",
                "reference": "Hadith",
                "keywords": ["faith", "brother", "love", "equality", "compassion"]
            },
            {
                "text_en": "The best of you are those who have the best character.",
                "text_ar": "أحسنكم أخلاقا",
                "reference": "Hadith",
                "keywords": ["character", "morality", "ethics", "good", "behavior"]
            },
            {
                "text_en": "Take up good deeds only as much as you are able to do, for the best deeds are those done constantly.",
                "text_ar": "خذوا من الأعمال ما تطيقون",
                "reference": "Hadith",
                "keywords": ["deeds", "action", "effort", "capability", "consistency"]
            },
            {
                "text_en": "The Prophet was the most generous, the most brave, and the best of people.",
                "text_ar": "كان أجود الناس وأشجع الناس",
                "reference": "Hadith",
                "keywords": ["prophet", "generous", "brave", "example", "leadership"]
            },
            {
                "text_en": "Whoever is merciful will be shown mercy by Allah on the Day of Judgment.",
                "text_ar": "من لم يرحم لم يرحم",
                "reference": "Hadith",
                "keywords": ["mercy", "compassion", "kindness", "judgment", "reward"]
            }
        ]
    }
    
    @staticmethod
    def analyze_question(question: str):
        """Analyze question and return relevant Ayah and Hadith"""
        question_lower = question.lower()
        
        # Find best matching Ayah
        best_ayah = None
        best_ayah_score = 0
        for ayah in AnalyzerService.ISLAMIC_DATABASE["ayahs"]:
            score = 0
            for keyword in ayah["keywords"]:
                if keyword in question_lower:
                    score += 1
            if score > best_ayah_score:
                best_ayah_score = score
                best_ayah = ayah
        
        # Find best matching Hadith
        best_hadith = None
        best_hadith_score = 0
        for hadith in AnalyzerService.ISLAMIC_DATABASE["hadiths"]:
            score = 0
            for keyword in hadith["keywords"]:
                if keyword in question_lower:
                    score += 1
            if score > best_hadith_score:
                best_hadith_score = score
                best_hadith = hadith
        
        # Provide fallback if no matches
        if not best_ayah:
            best_ayah = AnalyzerService.ISLAMIC_DATABASE["ayahs"][0]
        if not best_hadith:
            best_hadith = AnalyzerService.ISLAMIC_DATABASE["hadiths"][0]
        
        # Generate explanation (in real app, use AI like DeepSeek)
        explanation = AnalyzerService._generate_explanation(question, best_ayah, best_hadith)
        
        return {
            "ayah": best_ayah,
            "hadith": best_hadith,
            "explanation": explanation,
            "timestamp": datetime.now().isoformat()
        }
    
    @staticmethod
    def _generate_explanation(question: str, ayah: dict, hadith: dict) -> str:
        """Generate AI-like explanation combining Ayah and Hadith"""
        explanation = f"""
Based on Islamic teachings and your question about: "{question}"

The Quran guides us through the verse: "{ayah['text_en']}" ({ayah['reference']})

This is further reinforced by the wisdom of the Prophet: "{hadith['text_en']}"

In Islam, we are taught that every challenge in life brings with it an opportunity for growth and spiritual development. 
The above teachings emphasize that with patience and trust in Allah, we can overcome any difficulty. 
It is important to:
1. Make sincere dua (supplication) to Allah
2. Take practical steps to address the issue
3. Trust in Allah's wisdom and timing
4. Seek knowledge and guidance from Islamic scholars when needed
5. Remember that Allah is always with those who turn to Him

May Allah grant you wisdom, patience, and the right guidance in your situation.
        """
        return explanation.strip()
    
    @staticmethod
    def get_all_ayahs():
        """Get all Quranic verses"""
        return AnalyzerService.ISLAMIC_DATABASE["ayahs"]
    
    @staticmethod
    def get_all_hadiths():
        """Get all Hadiths"""
        return AnalyzerService.ISLAMIC_DATABASE["hadiths"]
