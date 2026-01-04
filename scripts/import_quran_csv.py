"""
Script to import Quran data from CSV files into the database.

CSV format:
- Columns: surah_number|ayah_number|ayah_text|...

Run this script to populate the database with complete Quran data:
    python scripts/import_quran_csv.py
"""

import sys
import os
import csv
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal, Base, engine
from app.models import QuranEnglish, QuranArabic

# Map surah numbers to surah names (English)
SURAH_NAMES_ENGLISH = {
    1: "Al-Fatiha",
    2: "Al-Baqarah",
    3: "Aal-e-Imran",
    4: "An-Nisa",
    5: "Al-Maidah",
    6: "Al-Anam",
    7: "Al-Araf",
    8: "Al-Anfal",
    9: "At-Taubah",
    10: "Yunus",
    11: "Hud",
    12: "Yusuf",
    13: "Ar-Rad",
    14: "Ibrahim",
    15: "Al-Hijr",
    16: "An-Nahl",
    17: "Al-Isra",
    18: "Al-Kahf",
    19: "Maryam",
    20: "Ta-Ha",
    21: "Al-Anbiya",
    22: "Al-Hajj",
    23: "Al-Muminun",
    24: "An-Nur",
    25: "Al-Furqan",
    26: "Ash-Shuara",
    27: "An-Naml",
    28: "Al-Qasas",
    29: "Al-Ankabut",
    30: "Ar-Rum",
    31: "Luqman",
    32: "As-Sajdah",
    33: "Al-Ahzab",
    34: "Saba",
    35: "Fatir",
    36: "Ya-Sin",
    37: "As-Saffat",
    38: "Sad",
    39: "Az-Zumar",
    40: "Ghafir",
    41: "Fussilat",
    42: "Ash-Shura",
    43: "Az-Zukhruf",
    44: "Ad-Dukhan",
    45: "Al-Jathiyah",
    46: "Al-Ahqaf",
    47: "Muhammad",
    48: "Al-Fath",
    49: "Al-Hujurat",
    50: "Qaf",
    51: "Ad-Dhariyat",
    52: "At-Tur",
    53: "An-Najm",
    54: "Al-Qamar",
    55: "Ar-Rahman",
    56: "Al-Waqiah",
    57: "Al-Hadid",
    58: "Al-Mujadilah",
    59: "Al-Hashr",
    60: "Al-Mumtahanah",
    61: "As-Saff",
    62: "Al-Jumu'ah",
    63: "Al-Munafiqun",
    64: "At-Taghabun",
    65: "At-Talaq",
    66: "At-Tahrim",
    67: "Al-Mulk",
    68: "Al-Qalam",
    69: "Al-Haqqah",
    70: "Al-Maarij",
    71: "Nuh",
    72: "Al-Jinn",
    73: "Al-Muzzammil",
    74: "Al-Muddathir",
    75: "Al-Qiyamah",
    76: "Al-Insan",
    77: "Al-Mursalat",
    78: "An-Naba",
    79: "An-Naziat",
    80: "Abasa",
    81: "At-Takwir",
    82: "Al-Infitar",
    83: "Al-Mutaffifin",
    84: "Al-Inshiqaq",
    85: "Al-Buruj",
    86: "At-Tariq",
    87: "Al-Ala",
    88: "Al-Ghashiyah",
    89: "Al-Fajr",
    90: "Al-Balad",
    91: "Ash-Shams",
    92: "Al-Lail",
    93: "Ad-Duha",
    94: "Ash-Sharh",
    95: "At-Tin",
    96: "Al-Alaq",
    97: "Al-Qadr",
    98: "Al-Bayyinah",
    99: "Az-Zalzalah",
    100: "Al-Adiyat",
    101: "Al-Qariah",
    102: "At-Takathur",
    103: "Al-Asr",
    104: "Al-Humazah",
    105: "Al-Fil",
    106: "Quraish",
    107: "Al-Maun",
    108: "Al-Kawthar",
    109: "Al-Kafirun",
    110: "An-Nasr",
    111: "Al-Lahab",
    112: "Al-Ikhlas",
    113: "Al-Falaq",
    114: "An-Nas"
}

# Map surah numbers to surah names (Arabic)
SURAH_NAMES_ARABIC = {
    1: "الفاتحة",
    2: "البقرة",
    3: "آل عمران",
    4: "النساء",
    5: "المائدة",
    6: "الأنعام",
    7: "الأعراف",
    8: "الأنفال",
    9: "التوبة",
    10: "يونس",
    11: "هود",
    12: "يوسف",
    13: "الرعد",
    14: "إبراهيم",
    15: "الحجر",
    16: "النحل",
    17: "الإسراء",
    18: "الكهف",
    19: "مريم",
    20: "طه",
    21: "الأنبياء",
    22: "الحج",
    23: "المؤمنون",
    24: "النور",
    25: "الفرقان",
    26: "الشعراء",
    27: "النمل",
    28: "القصص",
    29: "العنكبوت",
    30: "الروم",
    31: "لقمان",
    32: "السجدة",
    33: "الأحزاب",
    34: "سبأ",
    35: "فاطر",
    36: "يس",
    37: "الصافات",
    38: "ص",
    39: "الزمر",
    40: "غافر",
    41: "فصلت",
    42: "الشورى",
    43: "الزخرف",
    44: "الدخان",
    45: "الجاثية",
    46: "الأحقاف",
    47: "محمد",
    48: "الفتح",
    49: "الحجرات",
    50: "ق",
    51: "الذاريات",
    52: "الطور",
    53: "النجم",
    54: "القمر",
    55: "الرحمن",
    56: "الواقعة",
    57: "الحديد",
    58: "المجادلة",
    59: "الحشر",
    60: "الممتحنة",
    61: "الصف",
    62: "الجمعة",
    63: "المنافقون",
    64: "التغابن",
    65: "الطلاق",
    66: "التحريم",
    67: "الملك",
    68: "القلم",
    69: "الحاقة",
    70: "المعارج",
    71: "نوح",
    72: "الجن",
    73: "المزمل",
    74: "المدثر",
    75: "القيامة",
    76: "الإنسان",
    77: "المرسلات",
    78: "النبأ",
    79: "الناziات",
    80: "عبس",
    81: "التكوير",
    82: "الإنفطار",
    83: "المطففين",
    84: "الإنشقاق",
    85: "البروج",
    86: "الطارق",
    87: "الأعلى",
    88: "الغاشية",
    89: "الفجر",
    90: "البلد",
    91: "الشمس",
    92: "الليل",
    93: "الضحى",
    94: "الشرح",
    95: "التين",
    96: "العلق",
    97: "القدر",
    98: "البينة",
    99: "الزلزلة",
    100: "العاديات",
    101: "القارعة",
    102: "التكاثر",
    103: "العصر",
    104: "الهمزة",
    105: "الفيل",
    106: "قريش",
    107: "الماعون",
    108: "الكوثر",
    109: "الكافرون",
    110: "النصر",
    111: "اللهب",
    112: "الإخلاص",
    113: "الفلق",
    114: "الناس"
}

def import_quran_english(csv_path):
    """Import English Quran from CSV file"""
    db = SessionLocal()
    count = 0
    errors = 0
    
    try:
        # Try different encodings
        for encoding in ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']:
            try:
                with open(csv_path, 'r', encoding=encoding) as csvfile:
                    reader = csv.reader(csvfile, delimiter='|')
                    
                    for row in reader:
                        try:
                            if len(row) < 3 or not row[0].strip() or not row[1].strip():
                                continue
                            
                            surah_number = int(row[0].strip())
                            ayah_number = int(row[1].strip())
                            ayah_text = row[2].strip()
                            
                            if not ayah_text:
                                continue
                            
                            surah_name = SURAH_NAMES_ENGLISH.get(surah_number, f"Surah {surah_number}")
                            
                            # Check if already exists
                            existing = db.query(QuranEnglish).filter(
                                QuranEnglish.surah_number == surah_number,
                                QuranEnglish.ayah_number == ayah_number
                            ).first()
                            
                            if not existing:
                                verse = QuranEnglish(
                                    surah_number=surah_number,
                                    surah_name=surah_name,
                                    ayah_number=ayah_number,
                                    ayah_text=ayah_text,
                                    topic="general"
                                )
                                db.add(verse)
                                count += 1
                                
                                # Commit every 100 verses for better performance
                                if count % 100 == 0:
                                    db.commit()
                                    print(f"  [OK] Imported {count} English verses...")
                        
                        except (ValueError, IndexError) as e:
                            errors += 1
                            continue
                    
                    db.commit()
                    print(f"[OK] English Quran imported successfully: {count} verses")
                    return count
            
            except UnicodeDecodeError:
                continue
        
        # If all encodings fail
        raise Exception("Could not decode CSV file with any standard encoding")
        
    except Exception as e:
        db.rollback()
        print(f"[ERROR] Error importing English Quran: {e}")
        raise
    finally:
        db.close()

def import_quran_arabic(csv_path):
    """Import Arabic Quran from CSV file"""
    db = SessionLocal()
    count = 0
    errors = 0
    
    try:
        # Try different encodings
        for encoding in ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']:
            try:
                with open(csv_path, 'r', encoding=encoding) as csvfile:
                    reader = csv.reader(csvfile, delimiter='|')
                    
                    for row in reader:
                        try:
                            if len(row) < 3 or not row[0].strip() or not row[1].strip():
                                continue
                            
                            surah_number = int(row[0].strip())
                            ayah_number = int(row[1].strip())
                            ayah_text = row[2].strip()
                            
                            if not ayah_text:
                                continue
                            
                            surah_name = SURAH_NAMES_ARABIC.get(surah_number, f"سورة {surah_number}")
                            
                            # Check if already exists
                            existing = db.query(QuranArabic).filter(
                                QuranArabic.surah_number == surah_number,
                                QuranArabic.ayah_number == ayah_number
                            ).first()
                            
                            if not existing:
                                verse = QuranArabic(
                                    surah_number=surah_number,
                                    surah_name=surah_name,
                                    ayah_number=ayah_number,
                                    ayah_text=ayah_text,
                                    topic="general"
                                )
                                db.add(verse)
                                count += 1
                                
                                # Commit every 100 verses
                                if count % 100 == 0:
                                    db.commit()
                                    print(f"  [OK] Imported {count} Arabic verses...")
                        
                        except (ValueError, IndexError) as e:
                            errors += 1
                            continue
                    
                    db.commit()
                    print(f"[OK] Arabic Quran imported successfully: {count} verses")
                    return count
            
            except UnicodeDecodeError:
                continue
        
        # If all encodings fail
        raise Exception("Could not decode CSV file with any standard encoding")
        
    except Exception as e:
        db.rollback()
        print(f"[ERROR] Error importing Arabic Quran: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    import io
    import sys
    
    # Fix encoding for Windows console
    if sys.platform == 'win32':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    print("Starting Quran CSV import...\n")
    
    # Create tables first
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("[OK] Tables created successfully!\n")
    
    # Define CSV file paths
    english_csv = r"c:\Users\cheeh\AppData\Local\Temp\English.csv"
    arabic_csv = r"c:\Users\cheeh\Documents\Arabic-Original.csv\Arabic-Original.csv"
    
    # Import English Quran
    print("Importing English Quran from CSV...")
    try:
        english_count = import_quran_english(english_csv)
    except FileNotFoundError:
        print(f"[ERROR] English CSV file not found at: {english_csv}")
        english_count = 0
    
    print()
    
    # Import Arabic Quran
    print("Importing Arabic Quran from CSV...")
    try:
        arabic_count = import_quran_arabic(arabic_csv)
    except FileNotFoundError:
        print(f"[ERROR] Arabic CSV file not found at: {arabic_csv}")
        arabic_count = 0
    
    print(f"\n{'='*50}")
    print(f"Total verses imported:")
    print(f"  - English: {english_count}")
    print(f"  - Arabic: {arabic_count}")
    print(f"  - Total: {english_count + arabic_count}")
    print(f"{'='*50}")
