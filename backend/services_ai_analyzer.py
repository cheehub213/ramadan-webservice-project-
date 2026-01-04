"""
AI Analyzer Service - Personalized Islamic Guidance using AI
Enhanced with full Quran database access via API
"""
import json
import httpx
import os
from typing import Optional
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
env_path = Path(__file__).parent / ".env"
load_dotenv(env_path)

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "").strip()
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

# Import the Quran service for dynamic verse fetching
try:
    from services_quran import QuranService
    QURAN_SERVICE_AVAILABLE = True
except ImportError:
    QURAN_SERVICE_AVAILABLE = False
    print("[AIAnalyzer] Warning: QuranService not available, using fallback")

class AIAnalyzerService:
    """Service for AI-powered Islamic guidance and Quran/Hadith analysis"""

    # Quran Ayahs database - With proper topics
    QURAN_AYAHS = [
        {
            "id": 1,
            "reference": "Quran 2:155-156",
            "arabic": "ولنبلونكم بشيء من الخوف والجوع ونقص من الأموال والأنفس والثمرات",
            "translation": "And We will surely test you with something of fear and hunger and a loss of wealth and lives and fruits, but give good tidings to the patient",
            "explanation": "Allah tests believers with loss of wealth and hardship. These tests are meant to strengthen faith and patience.",
            "keywords": ["money", "wealth", "poverty", "loss", "test", "patience", "hardship", "financial"]
        },
        {
            "id": 2,
            "reference": "Quran 4:19",
            "arabic": "وعاشروهن بالمعروف",
            "translation": "Live with them in kindness and equity",
            "explanation": "This verse emphasizes the importance of treating spouses with kindness, respect, and fair treatment.",
            "keywords": ["marriage", "wife", "husband", "spouse", "kindness", "relationship", "equity", "love"]
        },
        {
            "id": 3,
            "reference": "Quran 94:5-6",
            "arabic": "فإن مع العسر يسرا * إن مع العسر يسرا",
            "translation": "For indeed, with hardship comes ease. Indeed, with hardship comes ease.",
            "explanation": "Allah guarantees that with every difficulty comes relief. This is repeated twice to emphasize certainty.",
            "keywords": ["ease", "difficulty", "relief", "hardship", "struggle", "challenge", "hope", "poverty", "money"]
        },
        {
            "id": 4,
            "reference": "Quran 2:286",
            "arabic": "لا يكلف الله نفسا إلا وسعها",
            "translation": "Allah does not burden any soul beyond its capacity",
            "explanation": "Allah will never give you more than you can handle. This is a promise of divine mercy.",
            "keywords": ["capability", "burden", "strength", "capacity", "mercy", "anxiety", "worry", "overwhelmed"]
        },
        {
            "id": 5,
            "reference": "Quran 39:53",
            "arabic": "قل يا عبادي الذين أسرفوا على أنفسهم لا تقنطوا من رحمة الله",
            "translation": "Say: O My servants who have transgressed against themselves! Do not despair of the mercy of Allah",
            "explanation": "No matter how many sins we commit, Allah's mercy is always available. Never lose hope.",
            "keywords": ["mercy", "forgiveness", "sin", "repentance", "hope", "despair", "guilt", "tawbah"]
        },
        {
            "id": 6,
            "reference": "Quran 65:2-3",
            "arabic": "ومن يتق الله يجعل له مخرجا * ويرزقه من حيث لا يحتسب",
            "translation": "And whoever fears Allah - He will make for him a way out. And will provide for him from where he does not expect.",
            "explanation": "Allah promises provision and solutions to those who are conscious of Him. Trust in Allah brings unexpected blessings.",
            "keywords": ["money", "wealth", "provision", "rizq", "financial", "poverty", "taqwa", "trust", "sustenance"]
        },
        {
            "id": 7,
            "reference": "Quran 3:139",
            "arabic": "ولا تهنوا ولا تحزنوا وأنتم الأعلون إن كنتم مؤمنين",
            "translation": "Do not lose heart or despair. You shall have the upper hand if you are believers",
            "explanation": "Faith in Allah brings strength and victory. Despair has no place in the heart of a true believer.",
            "keywords": ["faith", "belief", "victory", "strength", "despair", "confidence", "sadness", "depression"]
        },
        {
            "id": 8,
            "reference": "Quran 7:55",
            "arabic": "ادعوا ربكم تضرعا وخفية",
            "translation": "Call upon your Lord in humility and in secret",
            "explanation": "Make dua with sincerity, humility, and a humble heart. Allah loves sincere supplication.",
            "keywords": ["dua", "prayer", "supplication", "humility", "sincerity", "help", "need", "asking"]
        },
        {
            "id": 9,
            "reference": "Quran 4:36",
            "arabic": "واعبدوا الله ولا تشركوا به شيئا وبالوالدين إحسانا",
            "translation": "Worship Allah and associate nothing with Him, and be kind to parents",
            "explanation": "After worshipping Allah, showing kindness to parents is the most important duty.",
            "keywords": ["parents", "family", "kindness", "respect", "duty", "mother", "father", "elderly"]
        },
        {
            "id": 10,
            "reference": "Quran 49:10",
            "arabic": "إنما المؤمنون إخوة فأصلحوا بين أخويكم",
            "translation": "The believers are but brothers, so make peace between your brothers",
            "explanation": "Muslims are like a single family. Resolving conflicts is a sacred duty.",
            "keywords": ["community", "neighbors", "peace", "brotherhood", "conflict", "unity", "friends"]
        },
        {
            "id": 11,
            "reference": "Quran 2:177",
            "arabic": "وآتى المال على حبه ذوي القربى واليتامى والمساكين",
            "translation": "And gives wealth despite love for it to relatives, orphans, the needy",
            "explanation": "True virtue includes giving charity even when you need the money yourself.",
            "keywords": ["charity", "sadaqah", "poor", "needy", "orphan", "generosity", "giving", "zakat"]
        },
        {
            "id": 12,
            "reference": "Quran 25:63",
            "arabic": "وعباد الرحمن الذين يمشون على الأرض هونا",
            "translation": "The servants of the Most Merciful are those who walk on the earth with humility",
            "explanation": "The best believers are known for their humble, gentle demeanor.",
            "keywords": ["humility", "gentleness", "modesty", "character", "behavior", "arrogance", "pride"]
        },
        {
            "id": 13,
            "reference": "Quran 16:126",
            "arabic": "وإذا أصابتكم مصيبة قالوا إنا لله وإنا إليه راجعون",
            "translation": "Who, when afflicted with calamity, say: Truly we belong to Allah, and truly to Him we shall return",
            "explanation": "This verse teaches patience in hardship and remembering that all things come from Allah.",
            "keywords": ["patience", "hardship", "calamity", "affliction", "difficulty", "loss", "death", "grief"]
        },
        {
            "id": 14,
            "reference": "Quran 29:69",
            "arabic": "والذين جاهدوا فينا لنهدينهم سبلنا",
            "translation": "Those who strive in Our cause, We will surely guide them to Our paths",
            "explanation": "When you make genuine effort, Allah will guide you. Success comes to those who work hard.",
            "keywords": ["guidance", "effort", "struggle", "path", "success", "career", "work", "goals", "job"]
        },
        {
            "id": 15,
            "reference": "Quran 9:51",
            "arabic": "قل لن يصيبنا إلا ما كتب الله لنا هو مولانا",
            "translation": "Say: Nothing will happen to us except what Allah has decreed for us. He is our protector",
            "explanation": "Everything that happens is by Allah's decree. Trust in His plan brings peace.",
            "keywords": ["qadr", "destiny", "trust", "fate", "protection", "acceptance", "decree", "tawakkul"]
        }
    ]

    # Hadiths database
    HADITHS = [
        {
            "id": 1,
            "text_en": "The best of you are those who are best to their wives, and I am the best among you to my wives.",
            "text_ar": "خيركم خيركم لأهله وأنا خيركم لأهلي",
            "narrator": "At-Tirmidhi",
            "explanation": "The Prophet emphasized kindness to wives. Marriage is a mercy and partnership.",
            "keywords": ["marriage", "wife", "husband", "spouse", "family", "love", "kindness"]
        },
        {
            "id": 2,
            "text_en": "None of you believes until he loves for his brother what he loves for himself.",
            "text_ar": "لا يؤمن أحدكم حتى يحب لأخيه ما يحب لنفسه",
            "narrator": "Sahih Bukhari",
            "explanation": "True faith involves having compassion and wishing good for others.",
            "keywords": ["faith", "brotherhood", "compassion", "love", "empathy", "community", "neighbors"]
        },
        {
            "id": 3,
            "text_en": "The strongest among you is the one who controls his anger when he is provoked.",
            "text_ar": "ليس الشديد بالصرعة إنما الشديد الذي يملك نفسه عند الغضب",
            "narrator": "Sahih Bukhari",
            "explanation": "True strength is self-control and managing emotions wisely.",
            "keywords": ["anger", "control", "strength", "patience", "emotion", "self-discipline"]
        },
        {
            "id": 4,
            "text_en": "Whoever believes in Allah and the Last Day, let him speak good or remain silent.",
            "text_ar": "من كان يؤمن بالله واليوم الآخر فليقل خيرا أو ليصمت",
            "narrator": "Sahih Bukhari & Muslim",
            "explanation": "Guard your tongue. Speaking good or staying silent protects you from sin.",
            "keywords": ["speech", "silence", "tongue", "words", "gossip", "backbiting", "faith"]
        },
        {
            "id": 5,
            "text_en": "Richness is not having many possessions. Rather, true richness is the richness of the soul.",
            "text_ar": "ليس الغنى عن كثرة العرض ولكن الغنى غنى النفس",
            "narrator": "Sahih Bukhari & Muslim",
            "explanation": "True wealth is contentment. Be grateful for what you have rather than always wanting more.",
            "keywords": ["money", "wealth", "poverty", "contentment", "satisfaction", "gratitude", "richness", "financial"]
        },
        {
            "id": 6,
            "text_en": "Look at those below you and do not look at those above you, for it is more likely that you will not belittle the blessings of Allah.",
            "text_ar": "انظروا إلى من أسفل منكم ولا تنظروا إلى من هو فوقكم",
            "narrator": "Sahih Muslim",
            "explanation": "Comparing yourself to those with less helps you appreciate your blessings.",
            "keywords": ["money", "wealth", "gratitude", "comparison", "blessings", "contentment", "jealousy"]
        },
        {
            "id": 7,
            "text_en": "The best deed is to bring joy to a Muslim brother's heart, relieve him of worry, pay off his debt, or feed him.",
            "text_ar": "أحب الأعمال إلى الله سرور تدخله على مسلم",
            "narrator": "Tabarani",
            "explanation": "Helping others with their problems and needs is among the most beloved deeds to Allah.",
            "keywords": ["charity", "help", "debt", "feed", "poor", "kindness", "brotherhood", "money"]
        },
        {
            "id": 8,
            "text_en": "Patience is light. It illuminates the path through darkness.",
            "text_ar": "الصبر ضياء",
            "narrator": "Sahih Muslim",
            "explanation": "Patience guides us through dark times and deepens our connection to Allah.",
            "keywords": ["patience", "sabr", "endurance", "perseverance", "hardship", "difficulty"]
        },
        {
            "id": 9,
            "text_en": "Whoever relieves a believer of a hardship, Allah will relieve him of a hardship on the Day of Judgment.",
            "text_ar": "من نفس عن مؤمن كربة من كرب الدنيا نفس الله عنه كربة من كرب يوم القيامة",
            "narrator": "Sahih Muslim",
            "explanation": "Helping others through difficulties brings rewards in this life and the hereafter.",
            "keywords": ["help", "hardship", "relief", "reward", "charity", "brotherhood", "kindness"]
        },
        {
            "id": 10,
            "text_en": "The Muslim is the brother of the Muslim. He does not wrong him, forsake him, or despise him.",
            "text_ar": "المسلم أخو المسلم لا يظلمه ولا يخذله ولا يحقره",
            "narrator": "Sahih Muslim",
            "explanation": "Muslims must support each other and never abandon or look down upon fellow believers.",
            "keywords": ["brotherhood", "community", "support", "unity", "friendship", "neighbors"]
        },
        {
            "id": 11,
            "text_en": "Paradise is under the feet of mothers.",
            "text_ar": "الجنة تحت أقدام الأمهات",
            "narrator": "An-Nasai",
            "explanation": "Honoring and serving one's mother is a path to Paradise.",
            "keywords": ["mother", "parents", "family", "respect", "paradise", "honor", "duty"]
        },
        {
            "id": 12,
            "text_en": "With hardship comes ease. With hardship comes ease.",
            "text_ar": "فإن مع العسر يسرا إن مع العسر يسرا",
            "narrator": "Sahih Bukhari",
            "explanation": "This hadith affirms the Quranic promise that relief follows difficulty.",
            "keywords": ["ease", "hardship", "relief", "struggle", "hope", "patience", "poverty", "money"]
        },
        {
            "id": 13,
            "text_en": "Jibreel kept advising me to be good to neighbors until I thought he would make them heirs.",
            "text_ar": "ما زال جبريل يوصيني بالجار حتى ظننت أنه سيورثه",
            "narrator": "Sahih Bukhari & Muslim",
            "explanation": "The Prophet emphasized the immense importance of treating neighbors with kindness and respect.",
            "keywords": ["neighbor", "neighbors", "community", "kindness", "respect", "rights"]
        },
        {
            "id": 14,
            "text_en": "Allah says: O son of Adam, if your sins were to reach the clouds of the sky, then you sought forgiveness from Me, I would forgive you.",
            "text_ar": "يا ابن آدم لو بلغت ذنوبك عنان السماء ثم استغفرتني غفرت لك",
            "narrator": "At-Tirmidhi",
            "explanation": "No matter how many sins you have committed, Allah's mercy is always greater. Seek forgiveness sincerely.",
            "keywords": ["forgiveness", "tawba", "repentance", "sin", "mercy", "guilt", "mistake", "regret"]
        }
    ]

    # Available topics for user guidance
    AVAILABLE_TOPICS = [
        "Marriage & relationships",
        "Money & financial hardship",
        "Patience & perseverance", 
        "Family & parents",
        "Forgiveness & repentance",
        "Anger management",
        "Community & neighbors",
        "Charity & giving",
        "Faith & trust in Allah",
        "Grief & loss",
        "Work & career success"
    ]

    @staticmethod
    async def analyze_prompt_with_ai(user_prompt: str) -> dict:
        """Use AI to match user's question to relevant Quran verse and Hadith"""
        
        if not GROQ_API_KEY:
            print("[AI Analyzer] No Groq API key - using default response")
            return AIAnalyzerService.get_default_response()

        # Build the options list for AI with IDs clearly labeled
        ayahs_list = "\n".join([
            f"AYAH_ID_{ayah['id']}: {ayah['reference']} - {ayah['translation']} [Topics: {', '.join(ayah['keywords'][:5])}]"
            for ayah in AIAnalyzerService.QURAN_AYAHS
        ])

        hadiths_list = "\n".join([
            f"HADITH_ID_{hadith['id']}: {hadith['narrator']} - {hadith['text_en'][:100]}... [Topics: {', '.join(hadith['keywords'][:5])}]"
            for hadith in AIAnalyzerService.HADITHS
        ])

        system_prompt = f"""You are an Islamic scholar AI assistant. Your task is to match user questions to the MOST RELEVANT Quranic verse and Hadith from the database.

AVAILABLE QURAN VERSES:
{ayahs_list}

AVAILABLE HADITHS:
{hadiths_list}

INSTRUCTIONS:
1. Carefully read the user's question
2. Find the verse and hadith that BEST match their topic
3. If the topic is about MONEY, POVERTY, or FINANCIAL issues, use AYAH_ID_6 (provision from Allah) and HADITH_ID_5 (true richness)
4. If the topic is about MARRIAGE or SPOUSE, use AYAH_ID_2 (live with kindness) and HADITH_ID_1 (best to wives)
5. If the topic is about NEIGHBORS or COMMUNITY, use AYAH_ID_10 (believers are brothers) and HADITH_ID_13 (Jibreel advising about neighbors)
6. If the topic is about PARENTS or FAMILY, use AYAH_ID_9 (kindness to parents) and HADITH_ID_11 (paradise under mothers feet)
7. If the topic is about PATIENCE or HARDSHIP, use AYAH_ID_3 (with hardship comes ease) and HADITH_ID_8 (patience is light)
8. If the topic is about ANGER, use AYAH_ID_12 (walk with humility) and HADITH_ID_3 (controlling anger)
9. If NO relevant match exists, respond with NO_MATCH

RESPONSE FORMAT (JSON only):
For a match:
{{"ayah_id": <number>, "hadith_id": <number>, "ai_explanation": "<Your personalized explanation connecting the verse and hadith to their specific question>"}}

For no match:
{{"response": "NO_MATCH", "explanation": "Your question is about [topic]. We have guidance on: {', '.join(AIAnalyzerService.AVAILABLE_TOPICS)}"}}

IMPORTANT: Return ONLY valid JSON, no markdown or extra text."""

        user_message = f"User's question: \"{user_prompt}\"\n\nFind the most relevant Quran verse and Hadith for this specific question."

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    GROQ_API_URL,
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {GROQ_API_KEY}"
                    },
                    json={
                        "model": "llama-3.3-70b-versatile",
                        "messages": [
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": user_message}
                        ],
                        "temperature": 0.3,
                        "max_tokens": 600
                    }
                )

                if response.status_code == 200:
                    result = response.json()
                    ai_response = result["choices"][0]["message"]["content"]
                    
                    # Clean the response
                    cleaned = ai_response.strip()
                    if cleaned.startswith("```json"):
                        cleaned = cleaned[7:]
                    if cleaned.startswith("```"):
                        cleaned = cleaned[3:]
                    if cleaned.endswith("```"):
                        cleaned = cleaned[:-3]
                    cleaned = cleaned.strip()

                    try:
                        data = json.loads(cleaned)
                    except json.JSONDecodeError:
                        # Try to extract with regex
                        import re
                        if "NO_MATCH" in cleaned.upper():
                            return {
                                "response": "NO_MATCH",
                                "message": f"We don't have specific guidance on this topic. Available topics: {', '.join(AIAnalyzerService.AVAILABLE_TOPICS)}",
                                "available_topics": AIAnalyzerService.AVAILABLE_TOPICS,
                                "ai_generated": False
                            }
                        
                        ayah_match = re.search(r'"ayah_id"\s*:\s*(\d+)', cleaned)
                        hadith_match = re.search(r'"hadith_id"\s*:\s*(\d+)', cleaned)
                        explain_match = re.search(r'"ai_explanation"\s*:\s*"([^"]+)"', cleaned)
                        
                        if ayah_match and hadith_match:
                            data = {
                                "ayah_id": int(ayah_match.group(1)),
                                "hadith_id": int(hadith_match.group(1)),
                                "ai_explanation": explain_match.group(1) if explain_match else "See the verse and hadith below for guidance."
                            }
                        else:
                            return AIAnalyzerService.get_default_response()

                    # Check for NO_MATCH
                    if data.get("response") == "NO_MATCH":
                        return {
                            "response": "NO_MATCH",
                            "message": data.get("explanation", f"We don't have specific guidance on this topic. Available topics: {', '.join(AIAnalyzerService.AVAILABLE_TOPICS)}"),
                            "available_topics": AIAnalyzerService.AVAILABLE_TOPICS,
                            "ai_generated": False
                        }

                    # Get the selected ayah and hadith by ID
                    ayah_id = int(data.get("ayah_id", 1))
                    hadith_id = int(data.get("hadith_id", 1))
                    
                    # Find ayah by ID (not index!)
                    selected_ayah = None
                    for ayah in AIAnalyzerService.QURAN_AYAHS:
                        if ayah["id"] == ayah_id:
                            selected_ayah = ayah
                            break
                    if not selected_ayah:
                        selected_ayah = AIAnalyzerService.QURAN_AYAHS[0]
                    
                    # Find hadith by ID (not index!)
                    selected_hadith = None
                    for hadith in AIAnalyzerService.HADITHS:
                        if hadith["id"] == hadith_id:
                            selected_hadith = hadith
                            break
                    if not selected_hadith:
                        selected_hadith = AIAnalyzerService.HADITHS[0]

                    return {
                        "ai_explanation": data.get("ai_explanation", ""),
                        "ayah": selected_ayah,
                        "hadith": selected_hadith,
                        "ai_generated": True
                    }
                else:
                    print(f"Groq API error: {response.status_code}")
                    return AIAnalyzerService.get_default_response()

        except Exception as e:
            print(f"Error calling Groq API: {str(e)}")
            return AIAnalyzerService.get_default_response()

    @staticmethod
    async def analyze_with_semantic_search(user_prompt: str) -> dict:
        """Use semantic search to find the most relevant Quran verse"""
        from services_quran_semantic import QuranSemanticSearch
        
        # Check safety layer
        if not QuranSemanticSearch.is_safe_match(user_prompt):
            return {
                "response": "SAFETY_CHECK",
                "message": "We cannot provide guidance on that topic. Please ask about Islamic teachings on positive topics.",
                "ayah": None,
                "hadith": None,
                "ai_generated": False
            }
        
        # Find the most semantically similar verse
        best_match = QuranSemanticSearch.find_best_verse(user_prompt)
        
        if not best_match:
            return {
                "response": "LOW_CONFIDENCE",
                "message": "Your question doesn't match any verses closely. Try rewording your question.",
                "ayah": None,
                "hadith": None,
                "ai_generated": False
            }
        
        # Return just the verse (no AI explanation, no hadith)
        return {
            "ayah": {
                "reference": best_match["ref"],
                "surah_number": best_match["surah"],
                "ayah_number": best_match["ayah"],
                "translation": best_match["text_en"],
                "similarity_score": best_match["similarity_score"]
            },
            "hadith": None,
            "ai_explanation": None,
            "ai_generated": False,
            "source": "semantic_search"
        }

    @staticmethod
    async def analyze_with_full_quran(user_prompt: str) -> dict:
        """
        Enhanced AI analysis using the full Quran database via API
        This method:
        1. Uses AI to identify the best Surah:Ayah reference for the user's question
        2. Fetches the actual verse from the Quran API with Arabic + English
        3. Returns a more comprehensive response
        """
        if not GROQ_API_KEY:
            return AIAnalyzerService.get_default_response()
        
        if not QURAN_SERVICE_AVAILABLE:
            return await AIAnalyzerService.analyze_prompt_with_ai(user_prompt)
        
        # First, use AI to identify the best verse reference
        system_prompt = """You are an expert Islamic scholar AI. Your task is to recommend the MOST RELEVANT Quranic verse AND matching Hadith for the user's question.

You have access to the ENTIRE Quran (114 Surahs, 6236 verses). Choose the verse that DIRECTLY addresses their concern.

=== BEST VERSE REFERENCES BY TOPIC ===
ANGER/EMOTIONS:
- 3:134 (Those who restrain anger and pardon people)
- 41:34 (Repel evil with good)
- 7:199 (Take what is given freely, enjoin good, turn away from ignorant)

MARRIAGE/SPOUSE/WIFE/HUSBAND:
- 30:21 (He created mates for you to find tranquility - BEST for marriage)
- 4:19 (Live with wives in kindness)
- 2:187 (They are clothing for you and you for them)
- 25:74 (Grant us spouses who are comfort to our eyes)

MONEY/POVERTY/FINANCIAL/PROVISION/RIZQ:
- 65:3 (Whoever fears Allah, He will provide from unexpected sources - BEST for money)
- 2:261 (Those who spend in Allah's cause multiply their reward)
- 51:22 (In heaven is your provision)
- 2:155 (We test you with loss of wealth)

PATIENCE/HARDSHIP/DIFFICULTY:
- 94:5-6 (With hardship comes ease - BEST for hardship)
- 2:155 (We test you with fear, hunger, loss)
- 2:286 (Allah does not burden a soul beyond capacity)
- 3:139 (Do not lose hope)

PARENTS/FAMILY/MOTHER/FATHER:
- 17:23-24 (Be kind to parents, lower the wing of humility)
- 31:14 (Be grateful to parents)
- 46:15 (Kindness to parents)

FORGIVENESS/SIN/REPENTANCE:
- 39:53 (Do not despair of Allah's mercy - BEST for forgiveness)
- 4:110 (Whoever does wrong then seeks forgiveness)
- 25:70 (Allah will change sins to good deeds)

SADNESS/DEPRESSION/ANXIETY/WORRY:
- 94:5-6 (With hardship comes ease)
- 13:28 (Hearts find rest in remembrance of Allah)
- 93:3-5 (Your Lord has not forsaken you)
- 12:87 (Never despair of Allah's mercy)

PRAYER/DUA:
- 2:186 (I respond to the caller when he calls)
- 40:60 (Call upon Me, I will respond)

=== HADITH IDS AND THEIR TOPICS ===
ID 1: Marriage/Wife/Spouse - "Best of you are best to wives"
ID 2: Brotherhood/Community - "Love for brother what you love for yourself"  
ID 3: ANGER - "Strongest is one who controls anger" (USE FOR ANGER!)
ID 4: Speech/Words - "Speak good or remain silent"
ID 5: Money/Poverty/Wealth - "True richness is richness of soul" (USE FOR MONEY!)
ID 6: Money/Gratitude - "Look at those below you"
ID 7: Charity/Helping - "Best deed is to bring joy to Muslim's heart"
ID 8: Patience/Hardship - "Patience is light" (USE FOR HARDSHIP!)
ID 9: Helping others - "Relieve hardship, Allah relieves yours"
ID 10: Brotherhood - "Muslim is brother of Muslim"
ID 11: Parents/Mother - "Paradise under feet of mothers" (USE FOR PARENTS!)
ID 12: Hardship/Ease - "With hardship comes ease"
ID 13: Neighbors - "Jibreel advised about neighbors"
ID 14: FORGIVENESS/SIN/REPENTANCE - "Allah forgives sins reaching the sky" (USE FOR FORGIVENESS!)

=== YOUR RESPONSE (JSON only) ===
{
    "verse_ref": "<surah:ayah>",
    "topic_identified": "<topic>",
    "hadith_id": <number 1-14>,
    "ai_explanation": "<2-3 sentences connecting verse+hadith to their question>"
}

CRITICAL MATCHING RULES:
- ANGER questions → verse 3:134 + hadith_id 3
- MARRIAGE/WIFE questions → verse 30:21 + hadith_id 1
- MONEY/POVERTY questions → verse 65:3 + hadith_id 5
- PATIENCE/HARDSHIP → verse 94:5-6 + hadith_id 8 or 12
- PARENTS/MOTHER → verse 17:23-24 + hadith_id 11
- SADNESS/DEPRESSION → verse 94:5-6 or 13:28 + hadith_id 8
- FORGIVENESS/SIN/GUILT → verse 39:53 + hadith_id 14"""

        user_message = f"User's question: \"{user_prompt}\"\n\nChoose the BEST matching verse and hadith. Return JSON only."

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    GROQ_API_URL,
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {GROQ_API_KEY}"
                    },
                    json={
                        "model": "llama-3.3-70b-versatile",
                        "messages": [
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": user_message}
                        ],
                        "temperature": 0.3,
                        "max_tokens": 500
                    }
                )

                if response.status_code == 200:
                    result = response.json()
                    ai_response = result["choices"][0]["message"]["content"]
                    
                    # Clean the response
                    cleaned = ai_response.strip()
                    if cleaned.startswith("```json"):
                        cleaned = cleaned[7:]
                    if cleaned.startswith("```"):
                        cleaned = cleaned[3:]
                    if cleaned.endswith("```"):
                        cleaned = cleaned[:-3]
                    cleaned = cleaned.strip()

                    try:
                        data = json.loads(cleaned)
                    except json.JSONDecodeError:
                        # Fallback to original method
                        return await AIAnalyzerService.analyze_prompt_with_ai(user_prompt)
                    
                    verse_ref = data.get("verse_ref", "2:155")
                    topic = data.get("topic_identified", "general guidance")
                    hadith_id_raw = data.get("hadith_id")
                    hadith_id = int(hadith_id_raw) if hadith_id_raw is not None else 1
                    ai_explanation = data.get("ai_explanation", "")
                    
                    # Fetch the actual verse from Quran API
                    verse_data = await QuranService.get_verse(verse_ref)
                    
                    if verse_data:
                        # Build the ayah response
                        ayah = {
                            "id": 0,  # API-fetched verse
                            "reference": verse_data["reference"],
                            "arabic": verse_data["arabic"],
                            "translation": verse_data["translation"],
                            "explanation": f"From Surah {verse_data['surah_name_en']} ({verse_data['surah_name_ar']})",
                            "keywords": [topic],
                            "source": "quran_api"
                        }
                    else:
                        # Fallback to local database
                        ayah = AIAnalyzerService.QURAN_AYAHS[0]
                    
                    # Get hadith from local database
                    selected_hadith = None
                    for hadith in AIAnalyzerService.HADITHS:
                        if hadith["id"] == hadith_id:
                            selected_hadith = hadith
                            break
                    if not selected_hadith:
                        selected_hadith = AIAnalyzerService.HADITHS[0]

                    return {
                        "ai_explanation": ai_explanation,
                        "ayah": ayah,
                        "hadith": selected_hadith,
                        "topic_identified": topic,
                        "verse_source": "quran_api" if verse_data else "local",
                        "ai_generated": True
                    }
                else:
                    print(f"Groq API error: {response.status_code}")
                    return await AIAnalyzerService.analyze_prompt_with_ai(user_prompt)

        except Exception as e:
            print(f"Error in full Quran analysis: {str(e)}")
            return await AIAnalyzerService.analyze_prompt_with_ai(user_prompt)

    @staticmethod
    def get_default_response() -> dict:
        """Return a default response when AI is unavailable"""
        return {
            "ai_explanation": "Trust in Allah and remember that every challenge is an opportunity for growth.",
            "ayah": AIAnalyzerService.QURAN_AYAHS[2],  # Surah 94:5-6
            "hadith": AIAnalyzerService.HADITHS[7],  # Patience hadith
            "ai_generated": False
        }

    @staticmethod
    def get_all_ayahs():
        return AIAnalyzerService.QURAN_AYAHS

    @staticmethod  
    def get_all_hadiths():
        return AIAnalyzerService.HADITHS
