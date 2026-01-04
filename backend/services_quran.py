"""
Quran Service - Access to complete Quran database via AlQuran.cloud API
"""
import httpx
import json
from typing import Optional, Dict, List, Any
from pathlib import Path
import os

# Cache file for offline access
CACHE_FILE = Path(__file__).parent / "quran_cache.json"

class QuranService:
    """Service for accessing Quran verses with Arabic and English translations"""
    
    BASE_URL = "https://api.alquran.cloud/v1"
    
    # Pre-loaded surah info for quick reference
    SURAHS = {
        1: {"name_ar": "الفاتحة", "name_en": "Al-Fatiha", "verses": 7},
        2: {"name_ar": "البقرة", "name_en": "Al-Baqarah", "verses": 286},
        3: {"name_ar": "آل عمران", "name_en": "Ali 'Imran", "verses": 200},
        4: {"name_ar": "النساء", "name_en": "An-Nisa", "verses": 176},
        5: {"name_ar": "المائدة", "name_en": "Al-Ma'idah", "verses": 120},
        6: {"name_ar": "الأنعام", "name_en": "Al-An'am", "verses": 165},
        7: {"name_ar": "الأعراف", "name_en": "Al-A'raf", "verses": 206},
        8: {"name_ar": "الأنفال", "name_en": "Al-Anfal", "verses": 75},
        9: {"name_ar": "التوبة", "name_en": "At-Tawbah", "verses": 129},
        10: {"name_ar": "يونس", "name_en": "Yunus", "verses": 109},
        11: {"name_ar": "هود", "name_en": "Hud", "verses": 123},
        12: {"name_ar": "يوسف", "name_en": "Yusuf", "verses": 111},
        13: {"name_ar": "الرعد", "name_en": "Ar-Ra'd", "verses": 43},
        14: {"name_ar": "إبراهيم", "name_en": "Ibrahim", "verses": 52},
        15: {"name_ar": "الحجر", "name_en": "Al-Hijr", "verses": 99},
        16: {"name_ar": "النحل", "name_en": "An-Nahl", "verses": 128},
        17: {"name_ar": "الإسراء", "name_en": "Al-Isra", "verses": 111},
        18: {"name_ar": "الكهف", "name_en": "Al-Kahf", "verses": 110},
        19: {"name_ar": "مريم", "name_en": "Maryam", "verses": 98},
        20: {"name_ar": "طه", "name_en": "Taha", "verses": 135},
        21: {"name_ar": "الأنبياء", "name_en": "Al-Anbiya", "verses": 112},
        22: {"name_ar": "الحج", "name_en": "Al-Hajj", "verses": 78},
        23: {"name_ar": "المؤمنون", "name_en": "Al-Mu'minun", "verses": 118},
        24: {"name_ar": "النور", "name_en": "An-Nur", "verses": 64},
        25: {"name_ar": "الفرقان", "name_en": "Al-Furqan", "verses": 77},
        26: {"name_ar": "الشعراء", "name_en": "Ash-Shu'ara", "verses": 227},
        27: {"name_ar": "النمل", "name_en": "An-Naml", "verses": 93},
        28: {"name_ar": "القصص", "name_en": "Al-Qasas", "verses": 88},
        29: {"name_ar": "العنكبوت", "name_en": "Al-'Ankabut", "verses": 69},
        30: {"name_ar": "الروم", "name_en": "Ar-Rum", "verses": 60},
        31: {"name_ar": "لقمان", "name_en": "Luqman", "verses": 34},
        32: {"name_ar": "السجدة", "name_en": "As-Sajdah", "verses": 30},
        33: {"name_ar": "الأحزاب", "name_en": "Al-Ahzab", "verses": 73},
        34: {"name_ar": "سبأ", "name_en": "Saba", "verses": 54},
        35: {"name_ar": "فاطر", "name_en": "Fatir", "verses": 45},
        36: {"name_ar": "يس", "name_en": "Ya-Sin", "verses": 83},
        37: {"name_ar": "الصافات", "name_en": "As-Saffat", "verses": 182},
        38: {"name_ar": "ص", "name_en": "Sad", "verses": 88},
        39: {"name_ar": "الزمر", "name_en": "Az-Zumar", "verses": 75},
        40: {"name_ar": "غافر", "name_en": "Ghafir", "verses": 85},
        41: {"name_ar": "فصلت", "name_en": "Fussilat", "verses": 54},
        42: {"name_ar": "الشورى", "name_en": "Ash-Shura", "verses": 53},
        43: {"name_ar": "الزخرف", "name_en": "Az-Zukhruf", "verses": 89},
        44: {"name_ar": "الدخان", "name_en": "Ad-Dukhan", "verses": 59},
        45: {"name_ar": "الجاثية", "name_en": "Al-Jathiyah", "verses": 37},
        46: {"name_ar": "الأحقاف", "name_en": "Al-Ahqaf", "verses": 35},
        47: {"name_ar": "محمد", "name_en": "Muhammad", "verses": 38},
        48: {"name_ar": "الفتح", "name_en": "Al-Fath", "verses": 29},
        49: {"name_ar": "الحجرات", "name_en": "Al-Hujurat", "verses": 18},
        50: {"name_ar": "ق", "name_en": "Qaf", "verses": 45},
        51: {"name_ar": "الذاريات", "name_en": "Adh-Dhariyat", "verses": 60},
        52: {"name_ar": "الطور", "name_en": "At-Tur", "verses": 49},
        53: {"name_ar": "النجم", "name_en": "An-Najm", "verses": 62},
        54: {"name_ar": "القمر", "name_en": "Al-Qamar", "verses": 55},
        55: {"name_ar": "الرحمن", "name_en": "Ar-Rahman", "verses": 78},
        56: {"name_ar": "الواقعة", "name_en": "Al-Waqi'ah", "verses": 96},
        57: {"name_ar": "الحديد", "name_en": "Al-Hadid", "verses": 29},
        58: {"name_ar": "المجادلة", "name_en": "Al-Mujadilah", "verses": 22},
        59: {"name_ar": "الحشر", "name_en": "Al-Hashr", "verses": 24},
        60: {"name_ar": "الممتحنة", "name_en": "Al-Mumtahanah", "verses": 13},
        61: {"name_ar": "الصف", "name_en": "As-Saf", "verses": 14},
        62: {"name_ar": "الجمعة", "name_en": "Al-Jumu'ah", "verses": 11},
        63: {"name_ar": "المنافقون", "name_en": "Al-Munafiqun", "verses": 11},
        64: {"name_ar": "التغابن", "name_en": "At-Taghabun", "verses": 18},
        65: {"name_ar": "الطلاق", "name_en": "At-Talaq", "verses": 12},
        66: {"name_ar": "التحريم", "name_en": "At-Tahrim", "verses": 12},
        67: {"name_ar": "الملك", "name_en": "Al-Mulk", "verses": 30},
        68: {"name_ar": "القلم", "name_en": "Al-Qalam", "verses": 52},
        69: {"name_ar": "الحاقة", "name_en": "Al-Haqqah", "verses": 52},
        70: {"name_ar": "المعارج", "name_en": "Al-Ma'arij", "verses": 44},
        71: {"name_ar": "نوح", "name_en": "Nuh", "verses": 28},
        72: {"name_ar": "الجن", "name_en": "Al-Jinn", "verses": 28},
        73: {"name_ar": "المزمل", "name_en": "Al-Muzzammil", "verses": 20},
        74: {"name_ar": "المدثر", "name_en": "Al-Muddathir", "verses": 56},
        75: {"name_ar": "القيامة", "name_en": "Al-Qiyamah", "verses": 40},
        76: {"name_ar": "الإنسان", "name_en": "Al-Insan", "verses": 31},
        77: {"name_ar": "المرسلات", "name_en": "Al-Mursalat", "verses": 50},
        78: {"name_ar": "النبأ", "name_en": "An-Naba", "verses": 40},
        79: {"name_ar": "النازعات", "name_en": "An-Nazi'at", "verses": 46},
        80: {"name_ar": "عبس", "name_en": "'Abasa", "verses": 42},
        81: {"name_ar": "التكوير", "name_en": "At-Takwir", "verses": 29},
        82: {"name_ar": "الانفطار", "name_en": "Al-Infitar", "verses": 19},
        83: {"name_ar": "المطففين", "name_en": "Al-Mutaffifin", "verses": 36},
        84: {"name_ar": "الانشقاق", "name_en": "Al-Inshiqaq", "verses": 25},
        85: {"name_ar": "البروج", "name_en": "Al-Buruj", "verses": 22},
        86: {"name_ar": "الطارق", "name_en": "At-Tariq", "verses": 17},
        87: {"name_ar": "الأعلى", "name_en": "Al-A'la", "verses": 19},
        88: {"name_ar": "الغاشية", "name_en": "Al-Ghashiyah", "verses": 26},
        89: {"name_ar": "الفجر", "name_en": "Al-Fajr", "verses": 30},
        90: {"name_ar": "البلد", "name_en": "Al-Balad", "verses": 20},
        91: {"name_ar": "الشمس", "name_en": "Ash-Shams", "verses": 15},
        92: {"name_ar": "الليل", "name_en": "Al-Layl", "verses": 21},
        93: {"name_ar": "الضحى", "name_en": "Ad-Duha", "verses": 11},
        94: {"name_ar": "الشرح", "name_en": "Ash-Sharh", "verses": 8},
        95: {"name_ar": "التين", "name_en": "At-Tin", "verses": 8},
        96: {"name_ar": "العلق", "name_en": "Al-'Alaq", "verses": 19},
        97: {"name_ar": "القدر", "name_en": "Al-Qadr", "verses": 5},
        98: {"name_ar": "البينة", "name_en": "Al-Bayyinah", "verses": 8},
        99: {"name_ar": "الزلزلة", "name_en": "Az-Zalzalah", "verses": 8},
        100: {"name_ar": "العاديات", "name_en": "Al-'Adiyat", "verses": 11},
        101: {"name_ar": "القارعة", "name_en": "Al-Qari'ah", "verses": 11},
        102: {"name_ar": "التكاثر", "name_en": "At-Takathur", "verses": 8},
        103: {"name_ar": "العصر", "name_en": "Al-'Asr", "verses": 3},
        104: {"name_ar": "الهمزة", "name_en": "Al-Humazah", "verses": 9},
        105: {"name_ar": "الفيل", "name_en": "Al-Fil", "verses": 5},
        106: {"name_ar": "قريش", "name_en": "Quraysh", "verses": 4},
        107: {"name_ar": "الماعون", "name_en": "Al-Ma'un", "verses": 7},
        108: {"name_ar": "الكوثر", "name_en": "Al-Kawthar", "verses": 3},
        109: {"name_ar": "الكافرون", "name_en": "Al-Kafirun", "verses": 6},
        110: {"name_ar": "النصر", "name_en": "An-Nasr", "verses": 3},
        111: {"name_ar": "المسد", "name_en": "Al-Masad", "verses": 5},
        112: {"name_ar": "الإخلاص", "name_en": "Al-Ikhlas", "verses": 4},
        113: {"name_ar": "الفلق", "name_en": "Al-Falaq", "verses": 5},
        114: {"name_ar": "الناس", "name_en": "An-Nas", "verses": 6}
    }
    
    # Famous verses indexed by topic for quick recommendation
    FAMOUS_VERSES = {
        # Patience & Hardship
        "patience": ["2:153", "2:155", "3:200", "94:5-6", "2:286", "39:10"],
        "hardship": ["2:155", "94:5-6", "2:286", "65:7", "12:87", "3:139"],
        "difficulty": ["94:5-6", "65:2-3", "2:286", "12:87", "3:139"],
        
        # Marriage & Family
        "marriage": ["4:19", "30:21", "2:187", "25:74", "4:1", "24:32"],
        "wife": ["4:19", "30:21", "2:187", "4:34", "2:228", "65:6"],
        "husband": ["4:19", "30:21", "2:228", "4:34", "2:187"],
        "spouse": ["4:19", "30:21", "2:187", "25:74"],
        "children": ["25:74", "17:24", "46:15", "64:15", "8:28"],
        "parents": ["17:23-24", "31:14", "46:15", "29:8", "4:36"],
        "family": ["25:74", "64:14", "17:23-24", "4:1", "30:21"],
        
        # Money & Provision
        "money": ["2:155", "65:2-3", "3:180", "9:103", "2:261", "2:267"],
        "wealth": ["65:2-3", "3:180", "2:261", "17:26-27", "64:16"],
        "poverty": ["65:2-3", "2:155", "93:8", "94:5-6", "3:180"],
        "rizq": ["65:2-3", "51:22", "11:6", "29:60", "2:212"],
        "provision": ["65:2-3", "51:22", "11:6", "29:60", "67:15"],
        
        # Faith & Guidance
        "faith": ["2:285", "49:14", "3:139", "8:2", "9:124"],
        "guidance": ["1:6", "2:2", "2:185", "3:8", "10:57"],
        "belief": ["2:285", "4:136", "2:177", "49:15"],
        
        # Prayer & Worship
        "prayer": ["2:45", "29:45", "2:238", "11:114", "17:78-79"],
        "dua": ["2:186", "40:60", "7:55-56", "2:201", "3:8"],
        "worship": ["51:56", "4:36", "2:21", "7:29", "39:11"],
        
        # Sin & Forgiveness
        "sin": ["39:53", "4:110", "3:135", "42:25", "4:17-18"],
        "forgiveness": ["39:53", "4:110", "3:135", "4:17-18", "25:70"],
        "repentance": ["39:53", "66:8", "4:17-18", "25:70", "3:135"],
        "mercy": ["39:53", "7:156", "6:54", "21:107", "39:9"],
        
        # Anger & Emotions
        "anger": ["3:134", "41:34", "7:199", "25:63", "42:37"],
        "sadness": ["93:3-4", "12:86", "3:139", "94:5-6", "9:40"],
        "depression": ["94:5-6", "93:3-4", "12:87", "3:139", "39:53"],
        "anxiety": ["2:286", "65:2-3", "94:5-6", "3:139", "13:28"],
        "fear": ["2:155", "3:139", "2:286", "41:30", "10:62"],
        "hope": ["39:53", "12:87", "15:56", "3:139", "93:4-5"],
        
        # Success & Good Deeds
        "success": ["23:1", "91:9", "87:14", "3:104", "64:16"],
        "good_deeds": ["2:261", "99:7-8", "18:30", "6:160", "4:85"],
        "charity": ["2:261", "2:267", "3:92", "9:103", "2:271"],
        
        # Death & Afterlife
        "death": ["3:185", "29:57", "4:78", "62:8", "50:19"],
        "afterlife": ["3:185", "2:281", "4:134", "45:21", "6:32"],
        "paradise": ["3:185", "9:72", "13:23-24", "39:73", "36:55-58"],
        
        # Work & Striving
        "work": ["53:39", "94:7-8", "3:200", "9:105", "18:30"],
        "strive": ["29:69", "22:78", "25:52", "53:39"],
        
        # Truth & Justice
        "truth": ["2:42", "3:71", "17:81", "4:135", "5:8"],
        "justice": ["4:135", "5:8", "16:90", "4:58", "57:25"],
        
        # Health & Healing
        "health": ["26:80", "16:69", "10:57", "17:82", "41:44"],
        "healing": ["26:80", "10:57", "16:69", "17:82"],
        
        # Community & Brotherhood
        "community": ["49:10", "3:103", "49:13", "5:2", "8:63"],
        "brotherhood": ["49:10", "3:103", "49:13", "59:9"],
        "unity": ["3:103", "49:10", "8:63", "21:92"],
    }
    
    @classmethod
    async def get_verse(cls, verse_key: str) -> Optional[Dict]:
        """
        Fetch a specific verse from the API
        verse_key format: "surah:ayah" e.g., "2:155" or "2:155-156"
        """
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                url = f"{cls.BASE_URL}/ayah/{verse_key}/editions/quran-uthmani,en.sahih"
                response = await client.get(url)
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get("code") == 200 and data.get("data"):
                        verses = data["data"]
                        # Combine Arabic and English
                        arabic = verses[0] if len(verses) > 0 else {}
                        english = verses[1] if len(verses) > 1 else {}
                        
                        return {
                            "reference": f"Quran {arabic.get('surah', {}).get('number', '')}:{arabic.get('numberInSurah', '')}",
                            "arabic": arabic.get("text", ""),
                            "translation": english.get("text", ""),
                            "surah_name_ar": arabic.get("surah", {}).get("name", ""),
                            "surah_name_en": arabic.get("surah", {}).get("englishName", ""),
                            "surah_number": arabic.get("surah", {}).get("number", 0),
                            "verse_number": arabic.get("numberInSurah", 0),
                        }
        except Exception as e:
            print(f"[QuranService] Error fetching verse {verse_key}: {e}")
        
        return None
    
    @classmethod
    async def search_verses_by_topic(cls, topic: str) -> List[Dict]:
        """
        Search for relevant verses based on topic keywords
        Returns a list of verse references that match the topic
        """
        topic_lower = topic.lower()
        matching_verses = []
        
        # Check all topic mappings
        for keyword, verses in cls.FAMOUS_VERSES.items():
            if keyword in topic_lower or topic_lower in keyword:
                for verse_ref in verses:
                    if verse_ref not in matching_verses:
                        matching_verses.append(verse_ref)
        
        return matching_verses[:10]  # Return top 10 matches
    
    @classmethod
    async def get_verses_for_topic(cls, topic: str) -> List[Dict]:
        """
        Get full verse data for a topic
        """
        verse_refs = await cls.search_verses_by_topic(topic)
        verses = []
        
        for ref in verse_refs[:3]:  # Limit to 3 verses for performance
            verse = await cls.get_verse(ref)
            if verse:
                verses.append(verse)
        
        return verses
    
    @classmethod
    async def get_surah(cls, surah_number: int) -> Optional[Dict]:
        """
        Fetch a complete surah with Arabic and English
        """
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                url = f"{cls.BASE_URL}/surah/{surah_number}/editions/quran-uthmani,en.sahih"
                response = await client.get(url)
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get("code") == 200:
                        return data["data"]
        except Exception as e:
            print(f"[QuranService] Error fetching surah {surah_number}: {e}")
        
        return None
    
    @classmethod
    def get_surah_info(cls, surah_number: int) -> Optional[Dict]:
        """Get surah information from local cache"""
        return cls.SURAHS.get(surah_number)
    
    @classmethod
    async def get_random_verse(cls) -> Optional[Dict]:
        """Get a random verse for inspiration"""
        import random
        # Pick from famous verses
        all_verses = []
        for verses in cls.FAMOUS_VERSES.values():
            all_verses.extend(verses)
        
        if all_verses:
            verse_ref = random.choice(list(set(all_verses)))
            return await cls.get_verse(verse_ref)
        
        return None


# Test the service
if __name__ == "__main__":
    import asyncio
    
    async def test():
        print("Testing QuranService...")
        
        # Test fetching a verse
        verse = await QuranService.get_verse("2:155")
        if verse:
            print(f"\n✓ Verse 2:155:")
            print(f"  Arabic: {verse['arabic']}")
            print(f"  English: {verse['translation']}")
        
        # Test topic search
        verses = await QuranService.search_verses_by_topic("patience hardship")
        print(f"\n✓ Verses for 'patience hardship': {verses}")
        
        # Test getting verses for topic
        topic_verses = await QuranService.get_verses_for_topic("marriage")
        print(f"\n✓ Found {len(topic_verses)} verses for 'marriage'")
        for v in topic_verses:
            print(f"  - {v['reference']}: {v['translation'][:60]}...")
    
    asyncio.run(test())
