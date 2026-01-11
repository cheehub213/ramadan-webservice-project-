"""
Dua Generator Service - AI-Powered Personalized Dua Generation using Groq
"""
from sqlalchemy.orm import Session
from datetime import datetime
import json
import httpx
import os
import random
from typing import Optional
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file in the same directory
env_path = Path(__file__).parent / ".env"
load_dotenv(env_path)

# Groq API Configuration
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "").strip()
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

# Debug: Print if API key is loaded
if not GROQ_API_KEY:
    print("[WARNING] Groq API key not found. Using intelligent fallback.")
else:
    print(f"[OK] Groq API key loaded: {GROQ_API_KEY[:20]}...")

class DuaService:
    
    # Dua categories for reference
    DUA_CATEGORIES = [
        "Fear & Anxiety",
        "Financial Hardship", 
        "Health Issues",
        "Family Problems",
        "Career Guidance",
        "Spiritual Growth",
        "Relationship Issues",
        "Personal Challenges"
    ]
    
    # Different styles/tones for variety
    DUA_STYLES = [
        "humble and desperate plea",
        "confident trust in Allah's mercy",
        "reflective and contemplative",
        "urgent and heartfelt",
        "peaceful and accepting"
    ]
    
    # Different opening phrases
    OPENINGS = [
        "O Allah, the Most Merciful",
        "Ya Rahman, Ya Raheem",
        "O Lord of the Worlds",
        "O Allah, the All-Hearing, All-Knowing",
        "Ya Hayyu Ya Qayyum",
        "O the Turner of Hearts",
        "Ya Rabb",
        "O Allah, my Lord and the Lord of all creation"
    ]
    
    OPENINGS_AR = [
        "اللهم يا أرحم الراحمين",
        "يا رحمن يا رحيم",
        "يا رب العالمين",
        "اللهم يا سميع يا عليم",
        "يا حي يا قيوم",
        "يا مقلب القلوب",
        "يا رب",
        "اللهم ربي ورب كل شيء"
    ]
    
    @staticmethod
    def get_categories():
        """Get all dua categories"""
        return DuaService.DUA_CATEGORIES
    
    @staticmethod
    async def generate_dua(category: str, context: str) -> dict:
        """
        Generate a truly personalized dua using Groq AI.
        Each call generates a unique dua based on the user's specific situation.
        """
        
        # Select random style and opening for variety
        style = random.choice(DuaService.DUA_STYLES)
        opening_idx = random.randint(0, len(DuaService.OPENINGS) - 1)
        opening_en = DuaService.OPENINGS[opening_idx]
        opening_ar = DuaService.OPENINGS_AR[opening_idx]
        
        # Random elements for variety
        structure_type = random.choice([
            "Start with praise, then the specific request, then trust in Allah",
            "Start with acknowledging weakness, then seeking strength",
            "Start with the urgent need, then hope in Allah's mercy",
            "Start with Allah's names relevant to the need, then the request"
        ])
        
        # Create a unique prompt for truly personalized dua
        system_prompt = f"""You are a compassionate Islamic scholar creating duas (supplications to Allah).

FOR THE ENGLISH DUA:
- Maximum 3-4 sentences
- Start with: "{opening_en}"
- Use a {style} tone
- Address the person's situation directly

FOR THE ARABIC DUA (دعاء بالعربية):
- ABSOLUTELY NO ENGLISH WORDS - أي كلمة إنجليزية ممنوعة تماماً
- Write ONLY Arabic letters (ا ب ت ث ج ح خ...)
- Maximum 3-4 sentences
- Start with: "{opening_ar}"
- Use classical Arabic (فصحى)
- End with آمين

⚠️ ARABIC MUST BE 100% ARABIC SCRIPT ONLY ⚠️
❌ FORBIDDEN: Any Latin/English letters in Arabic dua
✅ CORRECT: اللهم ارزقني الصبر والقوة آمين
❌ WRONG: اللهم help me أو grant me رزق

OUTPUT - Return ONLY this JSON format:
{{
    "dua_text_en": "English dua here...",
    "dua_text_ar": "الدعاء بالعربية فقط هنا...",
    "how_to_use_en": "Brief guidance...",
    "how_to_use_ar": "إرشادات مختصرة..."
}}"""

        user_prompt = f"""Create a personalized dua for someone facing: {category} - {context}

IMPORTANT:
- English dua: 3-4 sentences, ends with "Ameen"
- Arabic dua: 3-4 sentences, ONLY ARABIC LETTERS (no English at all), ends with آمين

Generate the JSON now:"""

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
                            {"role": "user", "content": user_prompt}
                        ],
                        "temperature": 0.8,
                        "max_tokens": 800
                    }
                )
                
                if response.status_code == 200:
                    result = response.json()
                    ai_response = result["choices"][0]["message"]["content"]
                    
                    # Parse the JSON response from AI
                    try:
                        # Clean the response - sometimes AI adds markdown code blocks
                        cleaned_response = ai_response.strip()
                        if cleaned_response.startswith("```json"):
                            cleaned_response = cleaned_response[7:]
                        if cleaned_response.startswith("```"):
                            cleaned_response = cleaned_response[3:]
                        if cleaned_response.endswith("```"):
                            cleaned_response = cleaned_response[:-3]
                        cleaned_response = cleaned_response.strip()
                        
                        dua_data = json.loads(cleaned_response)
                        
                        return {
                            "category": category,
                            "context": context,
                            "dua_text_en": dua_data.get("dua_text_en", ""),
                            "dua_text_ar": dua_data.get("dua_text_ar", ""),
                            "how_to_use_en": dua_data.get("how_to_use_en", "Recite with sincere intention after prayers."),
                            "how_to_use_ar": dua_data.get("how_to_use_ar", "اقرأ بنية صادقة بعد الصلاة."),
                            "ai_generated": True,
                            "style_used": style,
                            "timestamp": datetime.now().isoformat()
                        }
                    except json.JSONDecodeError:
                        # If AI didn't return valid JSON, use the response as-is
                        return {
                            "category": category,
                            "context": context,
                            "dua_text_en": ai_response,
                            "dua_text_ar": "",
                            "how_to_use_en": "Recite with sincere intention.",
                            "how_to_use_ar": "اقرأ بنية صادقة.",
                            "ai_generated": True,
                            "timestamp": datetime.now().isoformat()
                        }
                else:
                    # API error - fall back to intelligent template
                    print(f"Groq API error: {response.status_code} - {response.text}")
                    return DuaService._generate_intelligent_fallback(category, context)
                    
        except Exception as e:
            print(f"Error calling Groq API: {str(e)}")
            return DuaService._generate_intelligent_fallback(category, context)
    
    @staticmethod
    def _generate_intelligent_fallback(category: str, context: str) -> dict:
        """
        Generate an intelligent, context-aware dua when AI is unavailable.
        This analyzes keywords in the context to create truly personalized duas.
        """
        
        context_lower = context.lower()
        
        # Intelligent keyword mapping for specific contexts
        specific_duas = {
            # Hell/Afterlife fears
            ("hell", "jahannam", "hellfire", "punishment", "afterlife"): {
                "en": f"""O Allah, the Most Merciful, I come to You with a heart filled with fear of Your punishment and the hellfire. 
I acknowledge my sins and shortcomings, and I turn to You in sincere repentance.
O Allah, You have said "Do not despair of the mercy of Allah" - I hold onto this promise.
Protect me from the torment of the grave and the punishment of hellfire.
Grant me death upon faith, and admit me into Your Paradise by Your mercy, not by my deeds.
Make my good deeds heavy on my scale, and forgive my sins, for You are the Most Forgiving.
O Allah, save me from the fire and grant me Jannah. Ameen.""",
                "ar": """اللهم يا أرحم الراحمين، أتيتك بقلب مملوء بالخوف من عذابك ومن النار.
أعترف بذنوبي وتقصيري، وأتوب إليك توبة نصوحاً.
اللهم قلت "لا تقنطوا من رحمة الله" وأنا متمسك بهذا الوعد.
أعذني من عذاب القبر وعذاب النار.
توفني على الإيمان وأدخلني جنتك برحمتك لا بعملي.
ثقّل ميزاني بالحسنات واغفر سيئاتي يا غفور.
اللهم أجرني من النار وأدخلني الجنة. آمين."""
            },
            # Death fears
            ("death", "dying", "die", "mortality"): {
                "en": f"""O Allah, make the moment of my death easy upon me and grant me a good ending.
I know that death is certain, but I fear not being prepared to meet You.
Grant me time to repent, to do good deeds, and to seek Your forgiveness.
When my time comes, let me die with "La ilaha illallah" on my tongue.
Make my grave spacious and filled with light, and make it a garden from the gardens of Paradise.
O Allah, I seek refuge in You from a bad death and from dying upon other than Islam. Ameen.""",
                "ar": """اللهم هوّن عليّ سكرات الموت وارزقني حسن الخاتمة.
أعلم أن الموت حق، لكنني أخاف ألا أكون مستعداً للقائك.
أمهلني لأتوب وأعمل صالحاً وأستغفرك.
عند الموت، اجعل لا إله إلا الله آخر كلامي.
وسّع قبري ونوّره واجعله روضة من رياض الجنة.
اللهم أعوذ بك من سوء الخاتمة ومن الموت على غير الإسلام. آمين."""
            },
            # Exam/Test anxiety
            ("exam", "test", "study", "studying", "school", "university", "grades"): {
                "en": f"""O Allah, the All-Knowing, I am anxious about {context}.
Grant me focus, clarity of mind, and excellent memory.
Help me recall everything I have studied when I need it most.
Remove anxiety from my heart and replace it with confidence in Your help.
O Allah, make this test easy for me and grant me success.
Let this be a means of opening doors of knowledge and opportunity for me.
I trust in You and rely upon You. Ameen.""",
                "ar": f"""اللهم يا عليم، أنا قلق من {context}.
ارزقني التركيز وصفاء الذهن وقوة الذاكرة.
ساعدني أتذكر كل ما درسته عند الحاجة.
أزل القلق من قلبي واستبدله بالثقة بعونك.
اللهم يسّر لي هذا الامتحان ووفقني فيه.
اجعله سبباً لفتح أبواب العلم والفرص لي.
توكلت عليك واعتمدت عليك. آمين."""
            },
            # Job/Interview
            ("job", "interview", "work", "employment", "hired", "career", "promotion"): {
                "en": f"""O Allah, the Provider, I seek Your help regarding {context}.
Open for me doors of halal provision and grant me a job that pleases You.
Give me confidence, eloquence, and wisdom during my job search and interviews.
Guide my words and actions to impress those who can help me.
If this job is good for me, make it easy; if not, replace it with something better.
Grant me work that benefits me, my family, and my community. Ameen.""",
                "ar": f"""اللهم يا رزاق، أستعينك في {context}.
افتح لي أبواب الرزق الحلال وارزقني عملاً يرضيك.
امنحني الثقة والفصاحة والحكمة في بحثي عن العمل ومقابلاتي.
سدد أقوالي وأفعالي لأحظى برضا من يستطيع مساعدتي.
إن كان هذا العمل خيراً لي فيسّره، وإلا فعوّضني خيراً منه.
ارزقني عملاً ينفعني وينفع أهلي ومجتمعي. آمين."""
            },
            # Health/Sickness
            ("sick", "illness", "disease", "pain", "health", "hospital", "surgery", "doctor"): {
                "en": f"""O Allah, the Healer, I come to You seeking cure from {context}.
You are the One who heals, and there is no cure except Your cure.
Grant me complete healing that leaves no illness behind.
Give strength to my body, peace to my mind, and faith to my heart.
Bless the doctors and medicine treating me, and make them a means of cure.
O Allah, this illness is testing me - help me bear it with patience and reward me for it.
I believe that You can heal what no doctor can. Heal me, Ya Shafi. Ameen.""",
                "ar": f"""اللهم يا شافي، أتيتك أطلب الشفاء من {context}.
أنت الشافي ولا شفاء إلا شفاؤك، شفاءً لا يغادر سقماً.
اشفني شفاءً تاماً لا يترك مرضاً.
قوِّ جسدي وهدّئ نفسي وثبّت إيماني.
بارك في الأطباء والدواء واجعلهم سبباً للشفاء.
اللهم هذا المرض ابتلاء - أعني على الصبر وأجرني عليه.
أؤمن أنك تشفي ما لا يشفيه طبيب. اشفني يا شافي. آمين."""
            },
            # Relationship/Marriage
            ("marriage", "spouse", "wife", "husband", "relationship", "love", "partner"): {
                "en": f"""O Allah, the Uniter of hearts, I seek Your help regarding {context}.
If this person is good for my religion, my life, and my hereafter, make it easy.
If not, remove them from my heart and replace them with someone better.
Grant me a spouse who will be the coolness of my eyes and help me on the path to Jannah.
Bless our relationship with love, mercy, and understanding.
Protect us from the whispers of Shaytan and the evil eye. Ameen.""",
                "ar": f"""اللهم يا جامع القلوب، أستعينك في {context}.
إن كان هذا الشخص خيراً لديني ودنياي وآخرتي فيسّره لي.
وإلا فاصرف قلبي عنه وعوّضني خيراً منه.
ارزقني زوجاً يكون قرة عيني ويعينني على طريق الجنة.
بارك في علاقتنا بالمودة والرحمة والتفاهم.
احفظنا من وساوس الشيطان ومن العين. آمين."""
            }
        }
        
        # Find matching specific dua based on keywords
        dua_en = None
        dua_ar = None
        
        for keywords, duas in specific_duas.items():
            if any(keyword in context_lower for keyword in keywords):
                dua_en = duas["en"]
                dua_ar = duas["ar"]
                break
        
        # If no specific match, use the general personalized template
        if not dua_en:
            dua_en = f"""O Allah, the Most Merciful and Most Compassionate, 
I come to You with a heart troubled by: {context}. 
You alone know the depth of my concern and the weight it carries in my heart.
I seek Your guidance, Your mercy, and Your help in this matter.
Grant me patience to bear this difficulty and wisdom to handle it.
Replace my worry with peace, my fear with faith, and my difficulty with ease.
Show me the way forward and grant me the best outcome.
You are the All-Hearing, the All-Knowing, and nothing is beyond Your power.
I place my complete trust in You alone. Ameen."""

            dua_ar = f"""اللهم يا رحمن يا رحيم، 
أتيتك بقلب مثقل بـ: {context}. 
أنت وحدك تعلم عمق قلقي وثقل هذا الهم على قلبي.
أسألك الهداية والرحمة والعون في هذا الأمر.
ارزقني الصبر على هذه الصعوبة والحكمة في التعامل معها.
بدّل قلقي سلاماً وخوفي إيماناً وصعوبتي يسراً.
أرِني الطريق وارزقني أفضل النتائج.
أنت السميع العليم ولا شيء يعجزك.
توكلت عليك وحدك. آمين."""

        how_to_en = f"""This dua is specifically crafted for your situation: "{context}"
Recite it with complete sincerity and trust in Allah, preferably:
- After the obligatory prayers (especially Fajr and Tahajjud)
- During the last third of the night when Allah descends to the lowest heaven
- While in sujood (prostration) - the closest you are to Allah
- On Friday between Asr and Maghrib - a blessed time for dua
- With raised hands and facing the Qibla

Remember: Allah responds to the dua of the distressed. Keep making this dua consistently."""

        how_to_ar = f"""هذا الدعاء مصمم خصيصاً لموقفك: "{context}"
اقرأه بإخلاص كامل وتوكل على الله، ويفضل:
- بعد الصلوات المفروضة (خاصة الفجر والتهجد)
- في الثلث الأخير من الليل عندما ينزل الله إلى السماء الدنيا
- وأنت ساجد - أقرب ما تكون من الله
- يوم الجمعة بين العصر والمغرب - وقت مبارك للدعاء
- رافعاً يديك ومستقبلاً القبلة

تذكر: الله يستجيب دعوة المضطر. استمر في هذا الدعاء بانتظام."""

        return {
            "category": category,
            "context": context,
            "dua_text_en": dua_en,
            "dua_text_ar": dua_ar,
            "how_to_use_en": how_to_en,
            "how_to_use_ar": how_to_ar,
            "ai_generated": False,
            "timestamp": datetime.now().isoformat()
        }
    
    @staticmethod
    def save_dua_to_history(db: Session, user_email: str, dua_data: dict):
        """Save generated dua to user's history"""
        from models_extended import DuaHistory
        
        dua_record = DuaHistory(
            email=user_email,
            category=dua_data['category'],
            context=dua_data['context'],
            dua_text_en=dua_data['dua_text_en'],
            dua_text_ar=dua_data['dua_text_ar'],
            how_to_use_en=dua_data.get('how_to_use_en', ''),
            how_to_use_ar=dua_data.get('how_to_use_ar', '')
        )
        db.add(dua_record)
        db.commit()
        db.refresh(dua_record)
        return dua_record
    
    @staticmethod
    def get_user_dua_history(db: Session, user_email: str):
        """Get all duas generated for a user"""
        from models_extended import DuaHistory
        return db.query(DuaHistory).filter(DuaHistory.email == user_email).order_by(DuaHistory.created_at.desc()).all()
    
    @staticmethod
    def submit_feedback(db: Session, dua_id: int, helpful: bool, notes: str = ""):
        """Submit feedback for a dua"""
        from models_extended import DuaHistory
        dua = db.query(DuaHistory).filter(DuaHistory.id == dua_id).first()
        if dua:
            dua.helpful = helpful
            dua.feedback_notes = notes
            db.commit()
            return True
        return False
