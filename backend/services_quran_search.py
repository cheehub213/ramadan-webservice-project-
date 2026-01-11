"""
Quran Semantic Search Service
Uses sentence-transformers to find the most relevant Quran verses based on user's query
"""
import json
import os
import pickle
from pathlib import Path
from typing import List, Dict, Optional

# Try to import numpy and sentence-transformers, fallback if not available
try:
    import numpy as np
    from sentence_transformers import SentenceTransformer
    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    np = None
    SENTENCE_TRANSFORMERS_AVAILABLE = False
    print("Warning: sentence-transformers or numpy not installed. Using keyword-based fallback.")

try:
    import httpx
except ImportError:
    httpx = None

# Quran Data - Complete database of verses with translations and topics
# This is a comprehensive subset covering major themes
QURAN_DATABASE = [
    # === MONEY, WEALTH & PROVISION (RIZQ) ===
    {
        "surah": 65, "ayah": 2, "surah_name": "At-Talaq",
        "arabic": "وَمَن يَتَّقِ اللَّهَ يَجْعَل لَّهُ مَخْرَجًا",
        "translation": "And whoever fears Allah - He will make for him a way out",
        "topics": ["money", "provision", "taqwa", "way out", "solution", "escape", "hardship", "fear Allah", "piety"]
    },
    {
        "surah": 65, "ayah": 3, "surah_name": "At-Talaq",
        "arabic": "وَيَرْزُقْهُ مِنْ حَيْثُ لَا يَحْتَسِبُ وَمَن يَتَوَكَّلْ عَلَى اللَّهِ فَهُوَ حَسْبُهُ",
        "translation": "And will provide for him from where he does not expect. And whoever relies upon Allah - then He is sufficient for him.",
        "topics": ["money", "provision", "rizq", "wealth", "unexpected", "trust", "tawakkul", "reliance", "sufficient", "income", "sustenance"]
    },
    {
        "surah": 11, "ayah": 6, "surah_name": "Hud",
        "arabic": "وَمَا مِن دَابَّةٍ فِي الْأَرْضِ إِلَّا عَلَى اللَّهِ رِزْقُهَا",
        "translation": "And there is no creature on earth but that upon Allah is its provision",
        "topics": ["provision", "rizq", "sustenance", "money", "wealth", "creature", "guarantee", "food", "income"]
    },
    {
        "surah": 2, "ayah": 268, "surah_name": "Al-Baqarah",
        "arabic": "الشَّيْطَانُ يَعِدُكُمُ الْفَقْرَ وَيَأْمُرُكُم بِالْفَحْشَاءِ وَاللَّهُ يَعِدُكُم مَّغْفِرَةً مِّنْهُ وَفَضْلًا",
        "translation": "Satan threatens you with poverty and orders you to immorality, while Allah promises you forgiveness from Him and bounty.",
        "topics": ["poverty", "money", "satan", "fear", "wealth", "bounty", "forgiveness", "promise", "immorality"]
    },
    {
        "surah": 17, "ayah": 30, "surah_name": "Al-Isra",
        "arabic": "إِنَّ رَبَّكَ يَبْسُطُ الرِّزْقَ لِمَن يَشَاءُ وَيَقْدِرُ",
        "translation": "Indeed, your Lord extends provision for whom He wills and restricts it.",
        "topics": ["provision", "rizq", "money", "wealth", "restrict", "extend", "will", "test"]
    },
    {
        "surah": 28, "ayah": 77, "surah_name": "Al-Qasas",
        "arabic": "وَابْتَغِ فِيمَا آتَاكَ اللَّهُ الدَّارَ الْآخِرَةَ وَلَا تَنسَ نَصِيبَكَ مِنَ الدُّنْيَا",
        "translation": "But seek, through that which Allah has given you, the home of the Hereafter; and do not forget your share of the world.",
        "topics": ["wealth", "world", "hereafter", "balance", "money", "share", "dunya", "akhirah"]
    },
    {
        "surah": 2, "ayah": 280, "surah_name": "Al-Baqarah",
        "arabic": "وَإِن كَانَ ذُو عُسْرَةٍ فَنَظِرَةٌ إِلَىٰ مَيْسَرَةٍ",
        "translation": "And if someone is in hardship, then let there be postponement until a time of ease.",
        "topics": ["debt", "loan", "hardship", "ease", "money", "postpone", "difficulty", "financial", "bills"]
    },
    {
        "surah": 9, "ayah": 105, "surah_name": "At-Tawbah",
        "arabic": "وَقُلِ اعْمَلُوا فَسَيَرَى اللَّهُ عَمَلَكُمْ وَرَسُولُهُ وَالْمُؤْمِنُونَ",
        "translation": "And say, 'Do your work; for Allah will see your deeds, and so will His Messenger and the believers.'",
        "topics": ["work", "job", "deeds", "effort", "action", "career", "employment", "labor"]
    },
    # === PATIENCE & HARDSHIP ===
    {
        "surah": 94, "ayah": 5, "surah_name": "Ash-Sharh",
        "arabic": "فَإِنَّ مَعَ الْعُسْرِ يُسْرًا",
        "translation": "For indeed, with hardship comes ease.",
        "topics": ["hardship", "ease", "difficulty", "relief", "patience", "hope", "struggle", "challenge"]
    },
    {
        "surah": 94, "ayah": 6, "surah_name": "Ash-Sharh",
        "arabic": "إِنَّ مَعَ الْعُسْرِ يُسْرًا",
        "translation": "Indeed, with hardship comes ease.",
        "topics": ["hardship", "ease", "difficulty", "relief", "patience", "hope", "promise"]
    },
    {
        "surah": 2, "ayah": 286, "surah_name": "Al-Baqarah",
        "arabic": "لَا يُكَلِّفُ اللَّهُ نَفْسًا إِلَّا وُسْعَهَا",
        "translation": "Allah does not burden a soul beyond that it can bear.",
        "topics": ["burden", "capacity", "strength", "difficulty", "hardship", "test", "trial", "anxiety", "overwhelmed", "stress"]
    },
    {
        "surah": 2, "ayah": 153, "surah_name": "Al-Baqarah",
        "arabic": "يَا أَيُّهَا الَّذِينَ آمَنُوا اسْتَعِينُوا بِالصَّبْرِ وَالصَّلَاةِ إِنَّ اللَّهَ مَعَ الصَّابِرِينَ",
        "translation": "O you who have believed, seek help through patience and prayer. Indeed, Allah is with the patient.",
        "topics": ["patience", "prayer", "help", "sabr", "salah", "difficulty", "hardship", "support"]
    },
    {
        "surah": 3, "ayah": 139, "surah_name": "Al-Imran",
        "arabic": "وَلَا تَهِنُوا وَلَا تَحْزَنُوا وَأَنتُمُ الْأَعْلَوْنَ إِن كُنتُم مُّؤْمِنِينَ",
        "translation": "So do not weaken and do not grieve, and you will be superior if you are true believers.",
        "topics": ["grief", "sadness", "weakness", "strength", "faith", "believers", "superiority", "depression"]
    },
    # === ANXIETY & PEACE ===
    {
        "surah": 13, "ayah": 28, "surah_name": "Ar-Ra'd",
        "arabic": "أَلَا بِذِكْرِ اللَّهِ تَطْمَئِنُّ الْقُلُوبُ",
        "translation": "Verily, in the remembrance of Allah do hearts find rest.",
        "topics": ["anxiety", "peace", "calm", "heart", "rest", "remembrance", "dhikr", "tranquility", "stress", "worry", "mental health"]
    },
    {
        "surah": 39, "ayah": 53, "surah_name": "Az-Zumar",
        "arabic": "قُلْ يَا عِبَادِيَ الَّذِينَ أَسْرَفُوا عَلَىٰ أَنفُسِهِمْ لَا تَقْنَطُوا مِن رَّحْمَةِ اللَّهِ",
        "translation": "Say, 'O My servants who have transgressed against themselves, do not despair of the mercy of Allah.'",
        "topics": ["despair", "mercy", "hope", "forgiveness", "sin", "transgression", "repentance", "guilt", "depression"]
    },
    # === MARRIAGE & FAMILY ===
    {
        "surah": 4, "ayah": 19, "surah_name": "An-Nisa",
        "arabic": "وَعَاشِرُوهُنَّ بِالْمَعْرُوفِ",
        "translation": "And live with them in kindness.",
        "topics": ["marriage", "wife", "husband", "kindness", "spouse", "relationship", "family", "love"]
    },
    {
        "surah": 30, "ayah": 21, "surah_name": "Ar-Rum",
        "arabic": "وَمِنْ آيَاتِهِ أَنْ خَلَقَ لَكُم مِّنْ أَنفُسِكُمْ أَزْوَاجًا لِّتَسْكُنُوا إِلَيْهَا وَجَعَلَ بَيْنَكُم مَّوَدَّةً وَرَحْمَةً",
        "translation": "And of His signs is that He created for you from yourselves mates that you may find tranquility in them; and He placed between you affection and mercy.",
        "topics": ["marriage", "spouse", "love", "mercy", "affection", "tranquility", "mate", "wife", "husband", "relationship"]
    },
    {
        "surah": 4, "ayah": 36, "surah_name": "An-Nisa",
        "arabic": "وَاعْبُدُوا اللَّهَ وَلَا تُشْرِكُوا بِهِ شَيْئًا وَبِالْوَالِدَيْنِ إِحْسَانًا",
        "translation": "Worship Allah and associate nothing with Him, and to parents do good.",
        "topics": ["parents", "family", "worship", "kindness", "mother", "father", "good", "duty", "respect"]
    },
    {
        "surah": 17, "ayah": 23, "surah_name": "Al-Isra",
        "arabic": "وَقَضَىٰ رَبُّكَ أَلَّا تَعْبُدُوا إِلَّا إِيَّاهُ وَبِالْوَالِدَيْنِ إِحْسَانًا",
        "translation": "And your Lord has decreed that you not worship except Him, and to parents, good treatment.",
        "topics": ["parents", "worship", "kindness", "mother", "father", "treatment", "respect", "duty", "family"]
    },
    # === DUA & SUPPLICATION ===
    {
        "surah": 2, "ayah": 186, "surah_name": "Al-Baqarah",
        "arabic": "وَإِذَا سَأَلَكَ عِبَادِي عَنِّي فَإِنِّي قَرِيبٌ أُجِيبُ دَعْوَةَ الدَّاعِ إِذَا دَعَانِ",
        "translation": "And when My servants ask you concerning Me - indeed I am near. I respond to the invocation of the supplicant when he calls upon Me.",
        "topics": ["dua", "supplication", "prayer", "answer", "near", "call", "response", "ask", "help"]
    },
    {
        "surah": 40, "ayah": 60, "surah_name": "Ghafir",
        "arabic": "وَقَالَ رَبُّكُمُ ادْعُونِي أَسْتَجِبْ لَكُمْ",
        "translation": "And your Lord says, 'Call upon Me; I will respond to you.'",
        "topics": ["dua", "supplication", "prayer", "call", "response", "answer", "ask"]
    },
    # === GUIDANCE & FAITH ===
    {
        "surah": 29, "ayah": 69, "surah_name": "Al-Ankabut",
        "arabic": "وَالَّذِينَ جَاهَدُوا فِينَا لَنَهْدِيَنَّهُمْ سُبُلَنَا",
        "translation": "And those who strive for Us - We will surely guide them to Our ways.",
        "topics": ["guidance", "strive", "effort", "path", "ways", "struggle", "direction", "lost"]
    },
    {
        "surah": 1, "ayah": 6, "surah_name": "Al-Fatiha",
        "arabic": "اهْدِنَا الصِّرَاطَ الْمُسْتَقِيمَ",
        "translation": "Guide us to the straight path.",
        "topics": ["guidance", "path", "straight", "direction", "lost", "confused", "help"]
    },
    # === FORGIVENESS & REPENTANCE ===
    {
        "surah": 3, "ayah": 135, "surah_name": "Al-Imran",
        "arabic": "وَالَّذِينَ إِذَا فَعَلُوا فَاحِشَةً أَوْ ظَلَمُوا أَنفُسَهُمْ ذَكَرُوا اللَّهَ فَاسْتَغْفَرُوا لِذُنُوبِهِمْ",
        "translation": "And those who, when they commit an immorality or wrong themselves, remember Allah and seek forgiveness for their sins.",
        "topics": ["forgiveness", "sin", "repentance", "wrong", "remember", "istighfar", "tawbah", "guilt", "mistake", "error", "accidental", "unintentional", "ate", "food", "haram", "forbidden"]
    },
    {
        "surah": 4, "ayah": 110, "surah_name": "An-Nisa",
        "arabic": "وَمَن يَعْمَلْ سُوءًا أَوْ يَظْلِمْ نَفْسَهُ ثُمَّ يَسْتَغْفِرِ اللَّهَ يَجِدِ اللَّهَ غَفُورًا رَّحِيمًا",
        "translation": "And whoever does a wrong or wrongs himself but then seeks forgiveness of Allah will find Allah Forgiving and Merciful.",
        "topics": ["forgiveness", "sin", "mercy", "wrong", "repentance", "istighfar", "merciful", "mistake", "accident", "unintentional", "pork", "alcohol", "haram", "forbidden"]
    },
    # === HEALTH & HEALING ===
    {
        "surah": 26, "ayah": 80, "surah_name": "Ash-Shu'ara",
        "arabic": "وَإِذَا مَرِضْتُ فَهُوَ يَشْفِينِ",
        "translation": "And when I am ill, it is He who cures me.",
        "topics": ["health", "healing", "sick", "illness", "cure", "disease", "recovery", "medical"]
    },
    {
        "surah": 17, "ayah": 82, "surah_name": "Al-Isra",
        "arabic": "وَنُنَزِّلُ مِنَ الْقُرْآنِ مَا هُوَ شِفَاءٌ وَرَحْمَةٌ لِّلْمُؤْمِنِينَ",
        "translation": "And We send down of the Quran that which is healing and mercy for the believers.",
        "topics": ["healing", "quran", "mercy", "cure", "believers", "health", "shifa"]
    },
    # === DEATH & GRIEF ===
    {
        "surah": 2, "ayah": 156, "surah_name": "Al-Baqarah",
        "arabic": "الَّذِينَ إِذَا أَصَابَتْهُم مُّصِيبَةٌ قَالُوا إِنَّا لِلَّهِ وَإِنَّا إِلَيْهِ رَاجِعُونَ",
        "translation": "Who, when disaster strikes them, say, 'Indeed we belong to Allah, and indeed to Him we will return.'",
        "topics": ["death", "grief", "disaster", "loss", "calamity", "patience", "return", "belong", "innalillah"]
    },
    {
        "surah": 3, "ayah": 185, "surah_name": "Al-Imran",
        "arabic": "كُلُّ نَفْسٍ ذَائِقَةُ الْمَوْتِ",
        "translation": "Every soul will taste death.",
        "topics": ["death", "soul", "mortality", "life", "end", "taste"]
    },
    # === GRATITUDE ===
    {
        "surah": 14, "ayah": 7, "surah_name": "Ibrahim",
        "arabic": "لَئِن شَكَرْتُمْ لَأَزِيدَنَّكُمْ",
        "translation": "If you are grateful, I will surely increase you in favor.",
        "topics": ["gratitude", "thankful", "increase", "blessing", "favor", "shukr", "grateful"]
    },
    # === TRUST IN ALLAH (TAWAKKUL) ===
    {
        "surah": 3, "ayah": 159, "surah_name": "Al-Imran",
        "arabic": "فَإِذَا عَزَمْتَ فَتَوَكَّلْ عَلَى اللَّهِ إِنَّ اللَّهَ يُحِبُّ الْمُتَوَكِّلِينَ",
        "translation": "Then when you have taken a decision, put your trust in Allah. Indeed, Allah loves those who trust in Him.",
        "topics": ["trust", "tawakkul", "decision", "reliance", "love", "Allah"]
    },
    {
        "surah": 8, "ayah": 2, "surah_name": "Al-Anfal",
        "arabic": "إِنَّمَا الْمُؤْمِنُونَ الَّذِينَ إِذَا ذُكِرَ اللَّهُ وَجِلَتْ قُلُوبُهُمْ",
        "translation": "The believers are only those who, when Allah is mentioned, their hearts become fearful.",
        "topics": ["faith", "belief", "heart", "fear", "Allah", "mention", "iman"]
    },
    # === CHARITY ===
    {
        "surah": 2, "ayah": 261, "surah_name": "Al-Baqarah",
        "arabic": "مَّثَلُ الَّذِينَ يُنفِقُونَ أَمْوَالَهُمْ فِي سَبِيلِ اللَّهِ كَمَثَلِ حَبَّةٍ أَنبَتَتْ سَبْعَ سَنَابِلَ",
        "translation": "The example of those who spend their wealth in the way of Allah is like a seed which grows seven spikes.",
        "topics": ["charity", "spend", "wealth", "money", "sadaqah", "zakat", "reward", "multiply"]
    },
    {
        "surah": 2, "ayah": 274, "surah_name": "Al-Baqarah",
        "arabic": "الَّذِينَ يُنفِقُونَ أَمْوَالَهُم بِاللَّيْلِ وَالنَّهَارِ سِرًّا وَعَلَانِيَةً فَلَهُمْ أَجْرُهُمْ عِندَ رَبِّهِمْ",
        "translation": "Those who spend their wealth by night and by day, secretly and publicly - they will have their reward with their Lord.",
        "topics": ["charity", "spend", "wealth", "reward", "secret", "public", "sadaqah", "zakat"]
    },
    # === KNOWLEDGE & LEARNING ===
    {
        "surah": 96, "ayah": 1, "surah_name": "Al-Alaq",
        "arabic": "اقْرَأْ بِاسْمِ رَبِّكَ الَّذِي خَلَقَ",
        "translation": "Read in the name of your Lord who created.",
        "topics": ["read", "knowledge", "learning", "education", "study", "create", "lord"]
    },
    {
        "surah": 20, "ayah": 114, "surah_name": "Ta-Ha",
        "arabic": "وَقُل رَّبِّ زِدْنِي عِلْمًا",
        "translation": "And say, 'My Lord, increase me in knowledge.'",
        "topics": ["knowledge", "learning", "increase", "dua", "education", "wisdom"]
    },
    # === JUSTICE & FAIRNESS ===
    {
        "surah": 4, "ayah": 135, "surah_name": "An-Nisa",
        "arabic": "يَا أَيُّهَا الَّذِينَ آمَنُوا كُونُوا قَوَّامِينَ بِالْقِسْطِ",
        "translation": "O you who have believed, be persistently standing firm in justice.",
        "topics": ["justice", "fairness", "stand", "firm", "believers", "rights", "equality"]
    },
    # === ANGER & SELF-CONTROL ===
    {
        "surah": 3, "ayah": 134, "surah_name": "Al-Imran",
        "arabic": "وَالْكَاظِمِينَ الْغَيْظَ وَالْعَافِينَ عَنِ النَّاسِ",
        "translation": "And who restrain anger and who pardon the people.",
        "topics": ["anger", "control", "restrain", "pardon", "forgive", "people", "self-control", "rage"]
    },
    # === HUMILITY ===
    {
        "surah": 25, "ayah": 63, "surah_name": "Al-Furqan",
        "arabic": "وَعِبَادُ الرَّحْمَٰنِ الَّذِينَ يَمْشُونَ عَلَى الْأَرْضِ هَوْنًا",
        "translation": "And the servants of the Most Merciful are those who walk upon the earth easily.",
        "topics": ["humility", "humble", "walk", "earth", "servants", "merciful", "gentle", "arrogance"]
    },
    # === BROTHERHOOD & UNITY ===
    {
        "surah": 49, "ayah": 10, "surah_name": "Al-Hujurat",
        "arabic": "إِنَّمَا الْمُؤْمِنُونَ إِخْوَةٌ فَأَصْلِحُوا بَيْنَ أَخَوَيْكُمْ",
        "translation": "The believers are but brothers, so make settlement between your brothers.",
        "topics": ["brotherhood", "unity", "believers", "peace", "reconciliation", "brothers", "muslim", "ummah"]
    },
    # === FEAR OF ALLAH ===
    {
        "surah": 3, "ayah": 102, "surah_name": "Al-Imran",
        "arabic": "يَا أَيُّهَا الَّذِينَ آمَنُوا اتَّقُوا اللَّهَ حَقَّ تُقَاتِهِ",
        "translation": "O you who have believed, fear Allah as He should be feared.",
        "topics": ["fear", "taqwa", "Allah", "believers", "piety", "god-consciousness"]
    },
    # === SUCCESS ===
    {
        "surah": 23, "ayah": 1, "surah_name": "Al-Mu'minun",
        "arabic": "قَدْ أَفْلَحَ الْمُؤْمِنُونَ",
        "translation": "Certainly will the believers have succeeded.",
        "topics": ["success", "believers", "faith", "triumph", "victory", "achieve"]
    },
    # === TESTS & TRIALS ===
    {
        "surah": 2, "ayah": 155, "surah_name": "Al-Baqarah",
        "arabic": "وَلَنَبْلُوَنَّكُم بِشَيْءٍ مِّنَ الْخَوْفِ وَالْجُوعِ وَنَقْصٍ مِّنَ الْأَمْوَالِ وَالْأَنفُسِ وَالثَّمَرَاتِ",
        "translation": "And We will surely test you with something of fear and hunger and a loss of wealth and lives and fruits.",
        "topics": ["test", "trial", "fear", "hunger", "loss", "wealth", "money", "hardship", "patience"]
    },
    {
        "surah": 67, "ayah": 2, "surah_name": "Al-Mulk",
        "arabic": "الَّذِي خَلَقَ الْمَوْتَ وَالْحَيَاةَ لِيَبْلُوَكُمْ أَيُّكُمْ أَحْسَنُ عَمَلًا",
        "translation": "He who created death and life to test you as to which of you is best in deed.",
        "topics": ["test", "life", "death", "deeds", "trial", "best", "action"]
    },
    # === TIME ===
    {
        "surah": 103, "ayah": 1, "surah_name": "Al-Asr",
        "arabic": "وَالْعَصْرِ",
        "translation": "By time.",
        "topics": ["time", "oath", "importance", "life", "moment"]
    },
    {
        "surah": 103, "ayah": 2, "surah_name": "Al-Asr",
        "arabic": "إِنَّ الْإِنسَانَ لَفِي خُسْرٍ",
        "translation": "Indeed, mankind is in loss.",
        "topics": ["loss", "mankind", "time", "waste", "human"]
    },
    # === NEIGHBORS ===
    {
        "surah": 4, "ayah": 36, "surah_name": "An-Nisa",
        "arabic": "وَالْجَارِ ذِي الْقُرْبَىٰ وَالْجَارِ الْجُنُبِ",
        "translation": "And the neighbor who is near of kin and the neighbor who is a stranger.",
        "topics": ["neighbor", "kindness", "community", "near", "stranger", "rights"]
    },
    # === CONTENTMENT ===
    {
        "surah": 16, "ayah": 97, "surah_name": "An-Nahl",
        "arabic": "مَنْ عَمِلَ صَالِحًا مِّن ذَكَرٍ أَوْ أُنثَىٰ وَهُوَ مُؤْمِنٌ فَلَنُحْيِيَنَّهُ حَيَاةً طَيِّبَةً",
        "translation": "Whoever does righteousness, whether male or female, while being a believer - We will surely cause him to live a good life.",
        "topics": ["good life", "righteousness", "believer", "happiness", "contentment", "peace"]
    },
]


class QuranSemanticSearch:
    """Semantic search for Quran verses using sentence embeddings"""
    
    def __init__(self):
        self.model = None
        self.embeddings = None
        self.embeddings_path = Path(__file__).parent / "quran_embeddings.pkl"
        self.database = QURAN_DATABASE
        
        if SENTENCE_TRANSFORMERS_AVAILABLE:
            self._initialize_model()
    
    def _initialize_model(self):
        """Initialize the sentence transformer model"""
        try:
            # Use a multilingual model that works well with both English and Arabic concepts
            self.model = SentenceTransformer('all-MiniLM-L6-v2')
            self._load_or_create_embeddings()
        except Exception as e:
            print(f"Error initializing model: {e}")
            self.model = None
    
    def _load_or_create_embeddings(self):
        """Load existing embeddings or create new ones"""
        if self.embeddings_path.exists():
            try:
                with open(self.embeddings_path, 'rb') as f:
                    self.embeddings = pickle.load(f)
                print(f"Loaded {len(self.embeddings)} Quran verse embeddings")
                return
            except Exception as e:
                print(f"Error loading embeddings: {e}")
        
        self._create_embeddings()
    
    def _create_embeddings(self):
        """Create embeddings for all Quran verses"""
        if not self.model:
            return
        
        print("Creating Quran verse embeddings...")
        
        # Create search text for each verse (translation + topics)
        search_texts = []
        for verse in self.database:
            # Combine translation with topics for better semantic matching
            search_text = f"{verse['translation']} {' '.join(verse['topics'])}"
            search_texts.append(search_text)
        
        # Generate embeddings
        self.embeddings = self.model.encode(search_texts, convert_to_numpy=True)
        
        # Save embeddings
        with open(self.embeddings_path, 'wb') as f:
            pickle.dump(self.embeddings, f)
        
        print(f"Created and saved {len(self.embeddings)} embeddings")
    
    def search(self, query: str, top_k: int = 3) -> List[Dict]:
        """
        Search for the most relevant Quran verses based on the query
        
        Args:
            query: The user's question or topic
            top_k: Number of results to return
            
        Returns:
            List of matching verses with scores
        """
        if not SENTENCE_TRANSFORMERS_AVAILABLE or not self.model or self.embeddings is None:
            # Fallback to keyword-based search
            return self._keyword_search(query, top_k)
        
        # Encode the query
        query_embedding = self.model.encode(query, convert_to_numpy=True)
        
        # Calculate cosine similarity
        similarities = np.dot(self.embeddings, query_embedding) / (
            np.linalg.norm(self.embeddings, axis=1) * np.linalg.norm(query_embedding)
        )
        
        # Get top-k indices
        top_indices = np.argsort(similarities)[-top_k:][::-1]
        
        results = []
        for idx in top_indices:
            verse = self.database[idx]
            results.append({
                "surah": verse["surah"],
                "ayah": verse["ayah"],
                "surah_name": verse["surah_name"],
                "arabic": verse["arabic"],
                "translation": verse["translation"],
                "reference": f"Quran {verse['surah']}:{verse['ayah']} ({verse['surah_name']})",
                "topics": verse["topics"],
                "score": float(similarities[idx])
            })
        
        return results
    
    def _keyword_search(self, query: str, top_k: int = 3) -> List[Dict]:
        """Fallback keyword-based search when semantic search is unavailable"""
        query_lower = query.lower()
        query_words = set(query_lower.split())
        
        scores = []
        for i, verse in enumerate(self.database):
            # Score based on topic matches
            topic_score = sum(1 for topic in verse["topics"] if topic.lower() in query_lower)
            
            # Score based on word overlap with translation
            translation_words = set(verse["translation"].lower().split())
            word_overlap = len(query_words & translation_words)
            
            # Combined score
            score = topic_score * 2 + word_overlap
            scores.append((i, score))
        
        # Sort by score and get top-k
        scores.sort(key=lambda x: x[1], reverse=True)
        top_indices = [idx for idx, _ in scores[:top_k]]
        
        results = []
        for idx in top_indices:
            verse = self.database[idx]
            results.append({
                "surah": verse["surah"],
                "ayah": verse["ayah"],
                "surah_name": verse["surah_name"],
                "arabic": verse["arabic"],
                "translation": verse["translation"],
                "reference": f"Quran {verse['surah']}:{verse['ayah']} ({verse['surah_name']})",
                "topics": verse["topics"],
                "score": scores[top_indices.index(idx)][1] / 10  # Normalize score
            })
        
        return results


# Global instance
_quran_search = None

def get_quran_search() -> QuranSemanticSearch:
    """Get or create the global QuranSemanticSearch instance"""
    global _quran_search
    if _quran_search is None:
        _quran_search = QuranSemanticSearch()
    return _quran_search


async def search_quran_by_topic(query: str, top_k: int = 1) -> Dict:
    """
    Main function to search for relevant Quran verses
    
    Args:
        query: The user's question or topic
        top_k: Number of results to return
        
    Returns:
        The most relevant verse(s)
    """
    search = get_quran_search()
    results = search.search(query, top_k)
    
    if results:
        return results[0]  # Return the top result
    
    # Fallback if no results
    return {
        "surah": 94,
        "ayah": 5,
        "surah_name": "Ash-Sharh",
        "arabic": "فَإِنَّ مَعَ الْعُسْرِ يُسْرًا",
        "translation": "For indeed, with hardship comes ease.",
        "reference": "Quran 94:5 (Ash-Sharh)",
        "topics": ["hardship", "ease", "patience"],
        "score": 0.5
    }
