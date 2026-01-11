"""
AI Analyzer Service - Personalized Islamic Guidance using AI
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

# Import Quran Semantic Search
try:
    from services_quran_search import search_quran_by_topic, get_quran_search
    SEMANTIC_SEARCH_AVAILABLE = True
except ImportError:
    SEMANTIC_SEARCH_AVAILABLE = False
    print("Warning: Quran semantic search not available")

class AIAnalyzerService:
    """Service for AI-powered Islamic guidance and Quran/Hadith analysis"""
    
    # Quran Ayahs database - EXPANDED for better coverage
    QURAN_AYAHS = [
        {
            "id": 1,
            "reference": "Quran 16:126",
            "arabic": "وَإِذَا أَصَابَكُم مُصِيبَةٌ قَالُواْ إِنَّا لِلَّهِ وَإِنَّآ إِلَيْهِ رَاجِعُون",
            "translation": "Who, when afflicted with calamity, say: 'Truly we belong to Allah, and truly to Him we shall return'",
            "explanation": "This verse teaches us that patience in hardship is a virtue, and we should remember that all things come from Allah and return to Him.",
            "keywords": ["patience", "hardship", "calamity", "affliction", "difficulty", "loss", "death"]
        },
        {
            "id": 2,
            "reference": "Quran 4:19",
            "arabic": "وَعَاشِرُوهُنَّ بِالْمَعْرُوفِ",
            "translation": "Live with them in kindness and equity",
            "explanation": "This verse emphasizes the importance of treating spouses with kindness, respect, and fair treatment. Marriage is a partnership based on mutual love and compassion.",
            "keywords": ["marriage", "wife", "husband", "spouse", "kindness", "relationship", "equity"]
        },
        {
            "id": 3,
            "reference": "Quran 94:5-6",
            "arabic": "فَإِنَّ مَعَ الْعُسْرِ يُسْرًا * إِنَّ مَعَ الْعُسْرِ يُسْرًا",
            "translation": "For indeed, with hardship comes ease. Indeed, with hardship comes ease.",
            "explanation": "Allah guarantees that with every difficulty comes relief. This verse is repeated twice to emphasize the certainty of this promise.",
            "keywords": ["ease", "difficulty", "relief", "hardship", "struggle", "challenge", "hope"]
        },
        {
            "id": 4,
            "reference": "Quran 2:286",
            "arabic": "لَا يُكَلِّفُ اللَّهُ نَفْسًا إِلَّا وُسْعَهَا",
            "translation": "Allah does not burden any soul beyond its capacity",
            "explanation": "Allah will never give you more than you can handle. This is a promise of divine mercy and understanding of human limitations.",
            "keywords": ["capability", "burden", "strength", "capacity", "mercy", "anxiety", "worry", "overwhelmed"]
        },
        {
            "id": 5,
            "reference": "Quran 39:53",
            "arabic": "قُلْ يَا عِبَادِيَ الَّذِينَ أَسْرَفُوا عَلَىٰ أَنفُسِهِمْ لَا تَقْنَطُوا مِن رَّحْمَةِ اللَّهِ",
            "translation": "Say: 'O My servants who have transgressed against themselves! Do not despair of the mercy of Allah'",
            "explanation": "No matter how many sins we commit, Allah's mercy is always available. Never lose hope in Allah's forgiveness.",
            "keywords": ["mercy", "forgiveness", "sin", "repentance", "hope", "despair", "guilt"]
        },
        {
            "id": 6,
            "reference": "Quran 29:69",
            "arabic": "وَالَّذِينَ جَاهَدُوا فِينَا لَنَهْدِيَنَّهُمْ سُبُلَنَا",
            "translation": "Those who strive in Our cause, We will surely guide them to Our paths",
            "explanation": "When you make genuine effort, Allah will guide you. Success comes to those who work hard and trust in Allah.",
            "keywords": ["guidance", "effort", "struggle", "path", "success", "career", "work", "goals"]
        },
        {
            "id": 7,
            "reference": "Quran 3:139",
            "arabic": "وَلَا تَهِنُوا وَلَا تَحْزَنُوا وَأَنتُمُ الْأَعْلَوْنَ إِن كُنتُم مُّؤْمِنِينَ",
            "translation": "So do not lose heart or despair. You shall have the upper hand if you are believers",
            "explanation": "Faith in Allah brings strength and victory. Despair has no place in the heart of a true believer.",
            "keywords": ["faith", "belief", "victory", "strength", "despair", "confidence", "sadness"]
        },
        {
            "id": 8,
            "reference": "Quran 7:55",
            "arabic": "ادْعُوا رَبَّكُمْ تَضَرُّعًا وَخُفْيَةً",
            "translation": "Call upon your Lord in humility and in secret",
            "explanation": "Make dua with sincerity, humility, and a humble heart. Allah loves sincere supplication from His servants.",
            "keywords": ["dua", "prayer", "supplication", "humility", "sincerity", "help", "need"]
        },
        {
            "id": 9,
            "reference": "Quran 4:36",
            "arabic": "وَاعْبُدُوا اللَّهَ وَلَا تُشْرِكُوا بِهِ شَيْئًا وَبِالْوَالِدَيْنِ إِحْسَانًا",
            "translation": "Worship Allah and associate nothing with Him, and be kind to parents with kindness and equity",
            "explanation": "After worshipping Allah, showing kindness to parents is emphasized as one of the most important duties. Respect and care for parents are fundamental Islamic values.",
            "keywords": ["parents", "family", "kindness", "respect", "duty", "mother", "father", "elderly"]
        },
        {
            "id": 10,
            "reference": "Quran 49:10",
            "arabic": "إِنَّمَا الْمُؤْمِنُونَ إِخْوَةٌ فَأَصْلِحُوا بَيْنَ أَخَوَيْكُمْ",
            "translation": "The believers are but brothers, so make peace between your brothers",
            "explanation": "Muslims are like a single family. Resolving conflicts and maintaining peace among community members is a sacred duty.",
            "keywords": ["community", "neighbors", "peace", "brotherhood", "conflict", "unity", "reconciliation"]
        },
        {
            "id": 11,
            "reference": "Quran 2:177",
            "arabic": "لَيْسَ الْبِرُّ أَن تُولُّوا وُجُوهَكُمْ قِبَلَ الْمَشْرِقِ وَالْمَغْرِبِ وَلَكِنَّ الْبِرَّ مَن آمَنَ بِاللَّهِ",
            "translation": "Righteousness is not in turning your faces to the east and west, but righteousness is in believing in Allah and helping others",
            "explanation": "True virtue comes from sincere belief and good actions towards others - charity, honesty, and compassion are the real measures of faith.",
            "keywords": ["charity", "righteousness", "kindness", "honesty", "integrity", "good deeds", "generosity"]
        },
        {
            "id": 12,
            "reference": "Quran 25:63",
            "arabic": "وَعِبَادُ الرَّحْمَٰنِ الَّذِينَ يَمْشُونَ عَلَى الْأَرْضِ هَوْنًا",
            "translation": "The servants of the Most Merciful are those who walk on the earth with humility and gentleness",
            "explanation": "The best believers are known for their humble, gentle demeanor. Arrogance and rudeness have no place among those who truly worship Allah.",
            "keywords": ["humility", "gentleness", "modesty", "character", "behavior", "arrogance"]
        },
        {
            "id": 13,
            "reference": "Quran 5:48",
            "arabic": "وَأَنزَلْنَا إِلَيْكَ الْكِتَابَ بِالْحَقِّ مُصَدِّقًا لِّمَا بَيْنَ يَدَيْهِ",
            "translation": "We have sent down to you the Book with truth, confirming what came before it",
            "explanation": "Knowledge and learning are honored in Islam. The Quran builds upon and confirms previous wisdom, teaching us to seek knowledge continuously.",
            "keywords": ["knowledge", "learning", "education", "wisdom", "understanding", "growth"]
        },
        {
            "id": 14,
            "reference": "Quran 76:8-9",
            "arabic": "وَيُطْعِمُونَ الطَّعَامَ عَلَىٰ حُبِّهِ مِسْكِينًا وَيَتِيمًا وَأَسِيرًا",
            "translation": "They give food despite their need to the poor, the orphan, and the captive",
            "explanation": "Caring for the vulnerable - the poor, orphans, and those in hardship - is a sign of true faith and compassion.",
            "keywords": ["charity", "poor", "orphan", "needy", "compassion", "generosity", "care"]
        },
        {
            "id": 15,
            "reference": "Quran 37:100",
            "arabic": "رَبِّ اغْفِرْ لِي وَلِوَالِدَيَّ وَلِمَن دَخَلَ بَيْتِيَ مُؤْمِنًا",
            "translation": "My Lord, forgive me and my parents and whoever enters my house as a believer",
            "explanation": "Making supplication for family, loved ones, and believers shows compassion and spiritual concern for others' spiritual wellbeing.",
            "keywords": ["family", "forgiveness", "dua", "parents", "loved ones", "intercession"]
        },
        # === MONEY, WEALTH & PROVISION (RIZQ) VERSES ===
        {
            "id": 16,
            "reference": "Quran 65:2-3",
            "arabic": "وَمَن يَتَّقِ اللَّهَ يَجْعَل لَّهُ مَخْرَجًا * وَيَرْزُقْهُ مِنْ حَيْثُ لَا يَحْتَسِبُ",
            "translation": "And whoever fears Allah - He will make for him a way out and will provide for him from where he does not expect",
            "explanation": "Allah promises that those who are mindful of Him will find unexpected solutions to their problems and provision from sources they never imagined. Trust in Allah's plan for your sustenance.",
            "keywords": ["money", "provision", "rizq", "wealth", "income", "sustenance", "financial", "poverty", "broke", "poor", "need money", "lack of money", "bills", "expenses", "debt", "struggling financially"]
        },
        {
            "id": 17,
            "reference": "Quran 11:6",
            "arabic": "وَمَا مِن دَابَّةٍ فِي الْأَرْضِ إِلَّا عَلَى اللَّهِ رِزْقُهَا",
            "translation": "There is no creature on earth but that upon Allah is its provision",
            "explanation": "Allah guarantees provision for every living being. If He provides for the birds and animals, He will certainly provide for you. Never lose hope in Allah's sustenance.",
            "keywords": ["provision", "rizq", "sustenance", "money", "wealth", "food", "poor", "poverty", "broke", "financial hardship", "struggling", "need help", "hungry"]
        },
        {
            "id": 18,
            "reference": "Quran 2:268",
            "arabic": "الشَّيْطَانُ يَعِدُكُمُ الْفَقْرَ وَيَأْمُرُكُم بِالْفَحْشَاءِ وَاللَّهُ يَعِدُكُم مَّغْفِرَةً مِّنْهُ وَفَضْلًا",
            "translation": "Satan threatens you with poverty and orders you to immorality, while Allah promises you forgiveness from Him and bounty",
            "explanation": "Fear of poverty often comes from Shaytan to make us desperate. Allah promises His bounty and blessings to those who trust Him and remain righteous, even in financial difficulty.",
            "keywords": ["poverty", "money", "fear", "poor", "broke", "financial", "wealth", "bounty", "desperation", "lack of money", "scared", "worried about money"]
        },
        {
            "id": 19,
            "reference": "Quran 3:26",
            "arabic": "قُلِ اللَّهُمَّ مَالِكَ الْمُلْكِ تُؤْتِي الْمُلْكَ مَن تَشَاءُ وَتَنزِعُ الْمُلْكَ مِمَّن تَشَاءُ",
            "translation": "Say, 'O Allah, Owner of Sovereignty, You give sovereignty to whom You will and You take sovereignty away from whom You will'",
            "explanation": "All wealth and power belong to Allah alone. He gives and takes as He wills. Trust that your financial situation is in His hands, and He knows what is best for you.",
            "keywords": ["wealth", "money", "power", "sovereignty", "rich", "poor", "financial", "prosperity", "success", "business"]
        },
        {
            "id": 20,
            "reference": "Quran 28:77",
            "arabic": "وَابْتَغِ فِيمَا آتَاكَ اللَّهُ الدَّارَ الْآخِرَةَ وَلَا تَنسَ نَصِيبَكَ مِنَ الدُّنْيَا",
            "translation": "Seek through what Allah has given you the home of the Hereafter, and do not forget your share of the world",
            "explanation": "Islam encourages balance - seek worldly provisions while keeping focus on the eternal reward. Work hard for your livelihood while maintaining your spiritual priorities.",
            "keywords": ["balance", "world", "work", "money", "career", "livelihood", "job", "provision", "success", "business", "earnings"]
        },
        {
            "id": 21,
            "reference": "Quran 17:30",
            "arabic": "إِنَّ رَبَّكَ يَبْسُطُ الرِّزْقَ لِمَن يَشَاءُ وَيَقْدِرُ",
            "translation": "Indeed, your Lord extends provision for whom He wills and restricts it",
            "explanation": "Allah controls all provision - sometimes He gives abundantly, sometimes He tests us with less. Both are tests of faith. The poor are tested with patience, the rich with gratitude.",
            "keywords": ["provision", "rizq", "wealth", "money", "rich", "poor", "test", "patience", "financial", "income"]
        },
        {
            "id": 22,
            "reference": "Quran 9:105",
            "arabic": "وَقُلِ اعْمَلُوا فَسَيَرَى اللَّهُ عَمَلَكُمْ وَرَسُولُهُ وَالْمُؤْمِنُونَ",
            "translation": "Say, 'Work, for Allah will see your deeds, and so will His Messenger and the believers'",
            "explanation": "Allah encourages hard work and effort. While you trust in Allah for provision, you must also take action. Work hard and Allah will bless your efforts.",
            "keywords": ["work", "job", "career", "effort", "deeds", "employment", "business", "success", "action", "hustle"]
        },
        # === ANXIETY & WORRY VERSES ===
        {
            "id": 23,
            "reference": "Quran 13:28",
            "arabic": "أَلَا بِذِكْرِ اللَّهِ تَطْمَئِنُّ الْقُلُوبُ",
            "translation": "Verily, in the remembrance of Allah do hearts find rest",
            "explanation": "When anxiety overwhelms you, especially about money or life problems, the remembrance of Allah brings peace to the heart. Dhikr is the cure for worried souls.",
            "keywords": ["anxiety", "worry", "stress", "peace", "calm", "mental health", "depression", "fear", "panic", "overwhelmed", "scared"]
        },
        {
            "id": 24,
            "reference": "Quran 2:153",
            "arabic": "يَا أَيُّهَا الَّذِينَ آمَنُوا اسْتَعِينُوا بِالصَّبْرِ وَالصَّلَاةِ إِنَّ اللَّهَ مَعَ الصَّابِرِينَ",
            "translation": "O you who believe, seek help through patience and prayer. Indeed, Allah is with the patient",
            "explanation": "In times of financial difficulty or any hardship, seek refuge in patience and prayer. Allah is with those who patiently persevere through their struggles.",
            "keywords": ["patience", "prayer", "help", "difficulty", "hardship", "struggle", "sabr", "salah", "support"]
        },
        # === DEBT & FINANCIAL OBLIGATIONS ===
        {
            "id": 25,
            "reference": "Quran 2:280",
            "arabic": "وَإِن كَانَ ذُو عُسْرَةٍ فَنَظِرَةٌ إِلَىٰ مَيْسَرَةٍ",
            "translation": "And if someone is in hardship, then postpone (the debt) until a time of ease",
            "explanation": "Islam teaches mercy in financial dealings. If you owe money and are struggling, seek patience from those you owe. Allah acknowledges financial hardship.",
            "keywords": ["debt", "loan", "owe money", "bills", "payment", "financial hardship", "credit", "money owed", "borrowing"]
        }
    ]
    
    # Hadiths database - EXPANDED for better coverage
    HADITHS = [
        {
            "id": 1,
            "text_en": "The best of you are those who are best to their wives, and I am the best among you to my wives.",
            "text_ar": "خَيْرُكُمْ خَيْرُكُمْ لِأَهْلِهِ، وَأَنَا خَيْرُكُمْ لِأَهْلِي",
            "narrator": "At-Tirmidhi",
            "explanation": "The Prophet Muhammad specifically emphasized kindness to wives. Marriage is a mercy and partnership where both partners deserve respect and kind treatment.",
            "keywords": ["marriage", "wife", "husband", "spouse", "family", "love", "kindness"]
        },
        {
            "id": 2,
            "text_en": "None of you believes until he loves for his brother what he loves for himself.",
            "text_ar": "لَا يُؤْمِنُ أَحَدُكُمْ حَتَّىٰ يُحِبَّ لِأَخِيهِ مَا يُحِبُّ لِنَفْسِهِ",
            "narrator": "Sahih Bukhari",
            "explanation": "True faith involves having compassion and wishing good for others as you wish for yourself. This applies to all relationships including neighbors.",
            "keywords": ["faith", "brotherhood", "compassion", "love", "empathy", "community", "neighbors"]
        },
        {
            "id": 3,
            "text_en": "The strongest among you is the one who controls his anger when he is provoked.",
            "text_ar": "لَيْسَ الشَّدِيدُ بِالصَّرْعَةِ، إِنَّمَا الشَّدِيدُ الَّذِي يَمْلِكُ نَفْسَهُ عِنْدَ الْغَضَبِ",
            "narrator": "Sahih Bukhari",
            "explanation": "True strength is self-control and managing emotions wisely. Controlling anger, especially in difficult relationships, is a mark of true strength.",
            "keywords": ["anger", "control", "strength", "patience", "emotion", "self-discipline"]
        },
        {
            "id": 4,
            "text_en": "Patience is the light of faith. The grateful are those who are patient.",
            "text_ar": "الصَّبْرُ ضِيَاءُ الإِيمَانِ",
            "narrator": "At-Tirmidhi",
            "explanation": "Patience is inseparable from faith. It guides us through dark times, strengthens relationships, and deepens our connection to Allah.",
            "keywords": ["patience", "faith", "endurance", "perseverance", "gratitude", "hardship"]
        },
        {
            "id": 5,
            "text_en": "The best deed is to bring joy to a Muslim brother's heart, and to relieve him of worry.",
            "text_ar": "أَفْضَلُ الْأَعْمَالِ أَنْ تَدْخِلَ عَلَىٰ أَخِيكَ الْمُسْلِمِ السُّرُورَ",
            "narrator": "At-Tabarani",
            "explanation": "Making others happy and easing their burdens is among the noblest actions. This includes supporting your neighbors and community emotionally.",
            "keywords": ["joy", "happiness", "kindness", "good deeds", "brotherhood", "support", "neighbors"]
        },
        {
            "id": 6,
            "text_en": "Whoever shows mercy will be shown mercy by Allah on the Day of Judgment.",
            "text_ar": "الرَّاحِمُونَ يَرْحَمُهُمُ الرَّحْمَٰنُ",
            "narrator": "Sunan At-Tirmidhi",
            "explanation": "Mercy and compassion towards others, especially those closest to us, will be rewarded by Allah. Show kindness to your family and community.",
            "keywords": ["mercy", "compassion", "kindness", "reward", "judgment", "family", "neighbors"]
        },
        {
            "id": 7,
            "text_en": "The best among you are those with the best character and manners.",
            "text_ar": "أَكْمَلُ الْمُؤْمِنِينَ إِيمَانًا أَحْسَنُهُمْ خُلُقًا",
            "narrator": "At-Tirmidhi",
            "explanation": "Good character, respectful communication, and excellent manners are the foundation of all healthy relationships, especially in marriage and community.",
            "keywords": ["character", "manners", "behavior", "virtue", "communication", "family"]
        },
        {
            "id": 8,
            "text_en": "Every soul will taste death, and you will only receive your reward in full on the Day of Judgment.",
            "text_ar": "كُلُّ نَفْسٍ ذَائِقَةُ الْمَوْتِ",
            "narrator": "Sahih Muslim",
            "explanation": "Remember that life is temporary, and what truly matters is how we treat others and live our faith. This perspective helps us prioritize kindness and compassion.",
            "keywords": ["mortality", "perspective", "kindness", "charity", "faith", "death"]
        },
        {
            "id": 9,
            "text_en": "A good neighbor is one whose neighbor is safe from his harm.",
            "text_ar": "الجار الصالح من آمن جاره بوائقه",
            "narrator": "Sunan Ibn Majah",
            "explanation": "The Prophet emphasized that a good neighbor is someone who ensures their neighbor's safety and well-being. Respecting and protecting neighbors is essential.",
            "keywords": ["neighbors", "safety", "protection", "respect", "community", "kindness"]
        },
        {
            "id": 10,
            "text_en": "Whoever is kind to the creatures of God is kind to himself.",
            "text_ar": "مَنْ رَحِمَ وَلَوْ ذَبِيحَةً رَحِمَهُ اللَّهُ يَوْمَ الْقِيَامَةِ",
            "narrator": "Sahih Bukhari",
            "explanation": "Compassion and mercy extend to all - people and creatures. Allah rewards mercy with mercy, and the merciful will find mercy on the Day of Judgment.",
            "keywords": ["mercy", "compassion", "kindness", "creatures", "reward", "charity"]
        },
        {
            "id": 11,
            "text_en": "The best of you are those who are best to their families.",
            "text_ar": "خيركم خيركم لأهليكم",
            "narrator": "At-Tirmidhi",
            "explanation": "Character is best reflected in how you treat those closest to you. Being good to your family is a fundamental measure of your faith.",
            "keywords": ["family", "parents", "children", "kindness", "respect", "duty"]
        },
        {
            "id": 12,
            "text_en": "Verily, with hardship comes ease. With hardship comes ease.",
            "text_ar": "فَإِنَّ مَعَ الْعُسْرِ يُسْرًا * إِنَّ مَعَ الْعُسْرِ يُسْرًا",
            "narrator": "Sahih Bukhari",
            "explanation": "This hadith affirms the Quranic promise that relief follows difficulty. No hardship is permanent, and Allah provides ease after every struggle.",
            "keywords": ["ease", "hardship", "relief", "struggle", "Allah's promise", "hope"]
        },
        {
            "id": 13,
            "text_en": "He is not a believer whose neighbor is not safe from his harm.",
            "text_ar": "لا يؤمن أحدكم حتى يحب لأخيه ما يحب لنفسه",
            "narrator": "Sahih Muslim",
            "explanation": "True faith means ensuring your neighbors and community members are safe, respected, and treated well. Neighbors have rights upon you.",
            "keywords": ["faith", "neighbors", "safety", "rights", "respect", "community"]
        },
        {
            "id": 14,
            "text_en": "The most beloved people to Allah are those who are most beneficial to others.",
            "text_ar": "أحب الناس إلى الله تعالى أنفعهم للناس",
            "narrator": "Al-Tabarani",
            "explanation": "Being helpful and beneficial to others - whether family, neighbors, or community - is highly valued in Islam and brings you closer to Allah.",
            "keywords": ["charity", "helpfulness", "service", "community", "benefit", "kindness"]
        },
        {
            "id": 15,
            "text_en": "Whoever believes in Allah and the Last Day should speak good words or remain silent.",
            "text_ar": "من كان يؤمن بالله واليوم الآخر فليقل خيرا أو ليصمت",
            "narrator": "Sahih Bukhari",
            "explanation": "The Prophet taught that if you cannot say something good and helpful, it's better to remain silent. This prevents harm and maintains peaceful relations.",
            "keywords": ["speech", "kindness", "respect", "neighbors", "community", "words"]
        },
        # === MONEY, WEALTH & PROVISION (RIZQ) HADITHS ===
        {
            "id": 16,
            "text_en": "If you put your trust completely in Allah, He will provide for you as He provides for the birds - they go out early in the morning empty and return full.",
            "text_ar": "لو أنكم تتوكلون على الله حق توكله لرزقكم كما يرزق الطير تغدو خماصاً وتروح بطاناً",
            "narrator": "At-Tirmidhi",
            "explanation": "Trust in Allah (tawakkul) combined with effort brings provision. Like birds who work for their food but trust Allah, we should make effort while relying on Allah for success.",
            "keywords": ["provision", "rizq", "trust", "tawakkul", "money", "wealth", "sustenance", "income", "poor", "broke", "financial", "struggle"]
        },
        {
            "id": 17,
            "text_en": "O Allah! I seek refuge in You from anxiety and grief, and I seek refuge in You from incapacity and laziness, and I seek refuge in You from debt and being overpowered by men.",
            "text_ar": "اللَّهُمَّ إِنِّي أَعُوذُ بِكَ مِنْ الْهَمِّ وَالْحَزَنِ، وَالْعَجْزِ وَالْكَسَلِ، وَالْبُخْلِ وَالْجُبْنِ، وَضَلَعِ الدَّيْنِ وَغَلَبَةِ الرِّجَالِ",
            "narrator": "Sahih Bukhari",
            "explanation": "The Prophet (ﷺ) taught this dua specifically for financial worries and debt. Recite it regularly when facing money problems or anxiety about finances.",
            "keywords": ["debt", "anxiety", "money", "worry", "financial", "poor", "loan", "bills", "stress", "dua for money", "broke"]
        },
        {
            "id": 18,
            "text_en": "Wealth is not in having many possessions, but rather wealth is the richness of the soul.",
            "text_ar": "ليس الغنى عن كثرة العرض ولكن الغنى غنى النفس",
            "narrator": "Sahih Bukhari and Muslim",
            "explanation": "True wealth is contentment and inner peace, not material possessions. Even if you have little money, a content heart is richer than a million dollars with a troubled soul.",
            "keywords": ["wealth", "contentment", "money", "rich", "poor", "peace", "soul", "happiness", "materialism"]
        },
        {
            "id": 19,
            "text_en": "Be in this world as if you were a stranger or a traveler.",
            "text_ar": "كن في الدنيا كأنك غريب أو عابر سبيل",
            "narrator": "Sahih Bukhari",
            "explanation": "Don't be too attached to worldly wealth. Money comes and goes, but your faith and good deeds remain. Focus on what truly matters for your eternal success.",
            "keywords": ["world", "attachment", "money", "wealth", "materialism", "perspective", "priorities", "dunya"]
        },
        {
            "id": 20,
            "text_en": "The upper hand (the giving hand) is better than the lower hand (the receiving hand).",
            "text_ar": "اليد العليا خير من اليد السفلى",
            "narrator": "Sahih Bukhari and Muslim",
            "explanation": "It's better to give than receive. Even in financial difficulty, look for ways to give - even a smile is charity. Generosity brings blessings and opens doors to provision.",
            "keywords": ["charity", "giving", "generosity", "money", "poor", "sadaqah", "blessing", "provision"]
        },
        {
            "id": 21,
            "text_en": "No one eats better food than that which he earns from the work of his own hands.",
            "text_ar": "ما أكل أحد طعاماً قط خيراً من أن يأكل من عمل يده",
            "narrator": "Sahih Bukhari",
            "explanation": "Halal earnings from your own hard work are the most blessed. Don't be ashamed of any honest work - it's noble and blessed by Allah.",
            "keywords": ["work", "job", "earnings", "halal", "employment", "career", "money", "income", "business", "labor"]
        },
        {
            "id": 22,
            "text_en": "Whoever Allah wants good for, He tests him with hardship.",
            "text_ar": "من يرد الله به خيراً يصب منه",
            "narrator": "Sahih Bukhari",
            "explanation": "Financial hardship may be a sign that Allah wants good for you. Tests purify our souls and elevate our rank. Stay patient - better times are coming.",
            "keywords": ["hardship", "test", "trial", "patience", "difficulty", "struggle", "poor", "broke", "financial problems"]
        },
        {
            "id": 23,
            "text_en": "Take advantage of five before five: your youth before your old age, your health before your sickness, your wealth before your poverty, your free time before your busyness, and your life before your death.",
            "text_ar": "اغتنم خمساً قبل خمس: شبابك قبل هرمك، وصحتك قبل سقمك، وغناك قبل فقرك، وفراغك قبل شغلك، وحياتك قبل موتك",
            "narrator": "Al-Hakim",
            "explanation": "When you have money, use it wisely for good. If you're currently struggling, know that circumstances change. Plan wisely and be grateful for what you have.",
            "keywords": ["time", "youth", "health", "wealth", "opportunity", "planning", "money", "gratitude"]
        }
    ]
    
    @staticmethod
    async def analyze_prompt_with_ai(user_prompt: str) -> dict:
        """
        Use Groq AI to analyze the user's prompt and find relevant Quran verses and hadiths
        """
        
        # Build a formatted list of available ayahs and hadiths for the AI with keywords
        ayahs_list = "\n".join([
            f"{i+1}. Quran {ayah['reference']}: {ayah['translation']} [Keywords: {', '.join(ayah['keywords'])}]"
            for i, ayah in enumerate(AIAnalyzerService.QURAN_AYAHS)
        ])
        
        hadiths_list = "\n".join([
            f"{i+1}. {hadith['narrator']}: {hadith['text_en']} [Keywords: {', '.join(hadith['keywords'])}]"
            for i, hadith in enumerate(AIAnalyzerService.HADITHS)
        ])
        
        system_prompt = f"""You are an Islamic scholar AI. When given a user's problem or question, you will:

1. Understand their specific situation and concerns
2. Match the user's problem to the MOST relevant Quran verse and Hadith from the available options
3. Only select a verse/hadith if it's GENUINELY RELEVANT to their problem
4. If NO suitable match exists, respond with "NO_MATCH" and explain what topics are available

AVAILABLE QURAN VERSES:
{ayahs_list}

AVAILABLE HADITHS:
{hadiths_list}

IMPORTANT: 
- ONLY choose verses/hadiths that are GENUINELY relevant to the user's specific problem
- Do NOT force a match if it's not related
- If you cannot find a good match, return {{"response": "NO_MATCH", "explanation": "Your question is about [specific topic]. We currently have guidance available on: marriage relationships, dealing with anger, family relations, neighbors/community, patience, hardship, forgiveness, wealth/charity, knowledge, grief/loss, and compassion. Would you like guidance on one of these topics instead?"}}
- Otherwise, return JSON in this format:
{{
    "ayah_id": <number from list>,
    "hadith_id": <number from list>,
    "ai_explanation": "A personalized explanation that mentions the specific verse and hadith you selected, showing how they apply to the user's situation",
    "response": "MATCH"
}}

Your explanation must specifically reference the Quran verse and Hadith you selected."""
        
        user_message = f"""The user is asking about this issue:

"{user_prompt}"

Match this to the most relevant Quran verse and Hadith from the available options ONLY IF they are genuinely related. 
If they don't match any available topics, respond with NO_MATCH."""
        
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
                        "temperature": 0.7,
                        "max_tokens": 800
                    }
                )
                
                if response.status_code == 200:
                    result = response.json()
                    ai_response = result["choices"][0]["message"]["content"]
                    
                    try:
                        # Clean response
                        cleaned = ai_response.strip()
                        if cleaned.startswith("```json"):
                            cleaned = cleaned[7:]
                        if cleaned.startswith("```"):
                            cleaned = cleaned[3:]
                        if cleaned.endswith("```"):
                            cleaned = cleaned[:-3]
                        cleaned = cleaned.strip()
                        
                        # Try to parse JSON
                        try:
                            data = json.loads(cleaned)
                        except json.JSONDecodeError:
                            # If JSON parsing fails, extract values using regex
                            import re
                            # Check for NO_MATCH response
                            if "NO_MATCH" in cleaned or "no_match" in cleaned.lower():
                                return {
                                    "response": "NO_MATCH",
                                    "message": "We don't have specific Islamic guidance available for this topic. Our available guidance covers: marriage relationships, dealing with anger, family relations, neighbors/community, patience, hardship, forgiveness, wealth/charity, knowledge, grief/loss, and compassion. Would you like guidance on one of these topics instead?",
                                    "available_topics": ["Marriage relationships", "Anger management", "Family relations", "Neighbors/Community", "Patience", "Hardship & difficulty", "Forgiveness & hope", "Wealth & charity", "Knowledge & learning", "Grief & loss", "Compassion & mercy"],
                                    "ai_generated": False
                                }
                            
                            ayah_match = re.search(r'"ayah_id"\s*:\s*(\d+)', cleaned)
                            hadith_match = re.search(r'"hadith_id"\s*:\s*(\d+)', cleaned)
                            explain_match = re.search(r'"ai_explanation"\s*:\s*"(.*?)"(?:,|\})', cleaned, re.DOTALL)
                            
                            if ayah_match and hadith_match and explain_match:
                                data = {
                                    "ayah_id": int(ayah_match.group(1)),
                                    "hadith_id": int(hadith_match.group(1)),
                                    "ai_explanation": explain_match.group(1),
                                    "response": "MATCH"
                                }
                            else:
                                # If we can't extract, use default
                                raise json.JSONDecodeError("Could not parse AI response", cleaned, 0)
                        
                        # Check if NO_MATCH was returned
                        if data.get("response") == "NO_MATCH":
                            return {
                                "response": "NO_MATCH",
                                "message": data.get("explanation", "We don't have specific guidance on this topic. Please try asking about: marriage, family, neighbors, anger management, patience, or forgiveness."),
                                "available_topics": ["Marriage relationships", "Anger management", "Family relations", "Neighbors/Community", "Patience", "Hardship & difficulty", "Forgiveness & hope", "Wealth & charity", "Knowledge & learning", "Grief & loss", "Compassion & mercy"],
                                "ai_generated": False
                            }
                        
                        # Get the selected ayah and hadith
                        ayah_id = int(data.get("ayah_id", 1)) - 1
                        hadith_id = int(data.get("hadith_id", 1)) - 1
                        
                        # Ensure indices are valid
                        ayah_id = max(0, min(ayah_id, len(AIAnalyzerService.QURAN_AYAHS) - 1))
                        hadith_id = max(0, min(hadith_id, len(AIAnalyzerService.HADITHS) - 1))
                        
                        selected_ayah = AIAnalyzerService.QURAN_AYAHS[ayah_id]
                        selected_hadith = AIAnalyzerService.HADITHS[hadith_id]
                        
                        return {
                            "ai_explanation": data.get("ai_explanation", ""),
                            "ayah": selected_ayah,
                            "hadith": selected_hadith,
                            "ai_generated": True
                        }
                    except (json.JSONDecodeError, ValueError, KeyError) as e:
                        print(f"Error parsing AI response: {str(e)}")
                        # Return default response
                        return AIAnalyzerService.get_default_response()
                else:
                    print(f"Groq API error: {response.status_code}")
                    return AIAnalyzerService.get_default_response()
                    
        except Exception as e:
            print(f"Error calling Groq API: {str(e)}")
            return AIAnalyzerService.get_default_response()
    
    @staticmethod
    def get_default_response() -> dict:
        """Return a default response when AI is unavailable"""
        return {
            "ai_explanation": "Trust in Allah and remember that every challenge is an opportunity for growth and spiritual development.",
            "ayah": AIAnalyzerService.QURAN_AYAHS[2],  # Surah Al-Inshirah (with hardship comes ease)
            "hadith": AIAnalyzerService.HADITHS[3],  # Patience hadith
            "ai_generated": False
        }
    
    async def analyze(self, question: str) -> dict:
        """
        Main analyze method - uses semantic search to find relevant Quran verses
        and AI to generate explanations
        """
        # Available topics for user guidance
        available_topics = [
            "money/provision/wealth", "marriage/spouse", "family/parents", 
            "patience/hardship", "anxiety/stress", "forgiveness", "death/grief",
            "gratitude/thankfulness", "charity/giving", "health/sickness",
            "dua/supplication", "tawbah/repentance", "trust in Allah/tawakkul"
        ]
        
        # First, try semantic search for Quran verses
        quran_result = None
        if SEMANTIC_SEARCH_AVAILABLE:
            try:
                quran_result = await search_quran_by_topic(question)
                print(f"Semantic search found: {quran_result.get('reference', 'N/A')} (score: {quran_result.get('score', 0):.2f})")
            except Exception as e:
                print(f"Semantic search error: {e}")
        
        # Check if semantic search found a good match (score > 0.25 is reasonable)
        MIN_MATCH_SCORE = 0.25
        
        if quran_result and quran_result.get("score", 0) >= MIN_MATCH_SCORE:
            # Good match found - generate full response
            ai_explanation = await self._generate_explanation(question, quran_result)
            
            # Get a relevant hadith
            hadith = self._find_best_hadith_by_keywords(question)
            
            return {
                "match_found": True,
                "ai_explanation": ai_explanation,
                "ayah": {
                    "arabic": quran_result.get("arabic", ""),
                    "reference": quran_result.get("reference", ""),
                    "translation": quran_result.get("translation", ""),
                    "explanation": f"This verse from Surah {quran_result.get('surah_name', '')} addresses themes of: {', '.join(quran_result.get('topics', [])[:5])}"
                },
                "hadith": {
                    "text": hadith.get("text_en", hadith.get("text", "")),
                    "narrator": hadith.get("narrator", ""),
                    "explanation": hadith.get("explanation", "")
                },
                "ai_generated": True,
                "search_score": quran_result.get("score", 0)
            }
        
        # No good match found - return guidance message without verse/hadith
        return {
            "match_found": False,
            "ai_explanation": f"We couldn't find a specific match for your question in our database. Please try rephrasing your question or ask about one of these topics:\n\n• {chr(10).join(['• ' + topic for topic in available_topics])}",
            "ayah": None,
            "hadith": None,
            "ai_generated": False,
            "available_topics": available_topics,
            "search_score": quran_result.get("score", 0) if quran_result else 0
        }
    
    async def _generate_explanation(self, question: str, quran_result: dict) -> str:
        """Generate an AI explanation for the found Quran verse"""
        if not GROQ_API_KEY:
            return f"Based on your concern about '{question[:50]}...', Allah guides us in {quran_result.get('reference', 'the Quran')}: '{quran_result.get('translation', '')}'. This verse reminds us to trust in Allah's wisdom and mercy."
        
        try:
            prompt = f"""The user asked: "{question}"

I found this relevant Quran verse:
{quran_result.get('reference', 'Quran')}: "{quran_result.get('translation', '')}"

Please write a brief, compassionate 2-3 sentence explanation of how this verse addresses the user's concern. Be warm and supportive. Do not repeat the verse translation, just explain its relevance."""

            async with httpx.AsyncClient(timeout=15.0) as client:
                response = await client.post(
                    GROQ_API_URL,
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {GROQ_API_KEY}"
                    },
                    json={
                        "model": "llama-3.3-70b-versatile",
                        "messages": [
                            {"role": "system", "content": "You are a compassionate Islamic scholar providing brief, supportive guidance."},
                            {"role": "user", "content": prompt}
                        ],
                        "temperature": 0.7,
                        "max_tokens": 200
                    }
                )
                
                if response.status_code == 200:
                    result = response.json()
                    return result["choices"][0]["message"]["content"].strip()
        except Exception as e:
            print(f"Error generating explanation: {e}")
        
        return f"This verse from {quran_result.get('reference', 'the Quran')} directly addresses your concern. Allah's words provide comfort and guidance for exactly this situation."
    
    def _find_best_hadith_by_keywords(self, question: str) -> dict:
        """Find the best matching hadith using keywords"""
        question_lower = question.lower()
        
        best_hadith = None
        best_score = 0
        for hadith in AIAnalyzerService.HADITHS:
            score = sum(1 for kw in hadith.get("keywords", []) if kw.lower() in question_lower)
            if score > best_score:
                best_score = score
                best_hadith = hadith
        
        if best_hadith:
            return best_hadith
        
        # Return a general hadith if no match
        return AIAnalyzerService.HADITHS[3] if len(AIAnalyzerService.HADITHS) > 3 else AIAnalyzerService.HADITHS[0]
    
    @staticmethod
    def find_best_match_by_keywords(question: str) -> dict:
        """
        Fallback keyword-based matching when AI is unavailable
        """
        question_lower = question.lower()
        
        # Score each ayah based on keyword matches
        best_ayah = None
        best_ayah_score = 0
        for ayah in AIAnalyzerService.QURAN_AYAHS:
            score = sum(1 for kw in ayah["keywords"] if kw.lower() in question_lower)
            if score > best_ayah_score:
                best_ayah_score = score
                best_ayah = ayah
        
        # Score each hadith based on keyword matches
        best_hadith = None
        best_hadith_score = 0
        for hadith in AIAnalyzerService.HADITHS:
            score = sum(1 for kw in hadith["keywords"] if kw.lower() in question_lower)
            if score > best_hadith_score:
                best_hadith_score = score
                best_hadith = hadith
        
        # Use defaults if no matches found
        if not best_ayah or best_ayah_score == 0:
            best_ayah = AIAnalyzerService.QURAN_AYAHS[2]  # With hardship comes ease
        if not best_hadith or best_hadith_score == 0:
            best_hadith = AIAnalyzerService.HADITHS[3]  # Patience hadith
        
        return {
            "ayah": best_ayah,
            "hadith": best_hadith,
            "ai_explanation": f"Based on your question about '{question[:50]}...', here is guidance from the Quran and Sunnah.",
            "ai_generated": False
        }
