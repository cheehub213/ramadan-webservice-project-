"""
Script to populate sample Quran and Hadith data into the database.
Run this after creating the database tables.

Usage:
    python scripts/populate_sample_data.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal, Base, engine
from app.models import QuranEnglish, QuranArabic, Hadith

def populate_sample_data():
    """Add sample Quran verses and Hadiths to database"""
    
    db = SessionLocal()
    
    try:
        # Sample Quran verses (English)
        sample_quran_english = [
            {
                "surah_number": 94,
                "surah_name": "Ash-Sharh",
                "ayah_number": 1,
                "ayah_text": "Did We not open your heart for you",
                "topic": "comfort, ease"
            },
            {
                "surah_number": 2,
                "surah_name": "Al-Baqarah",
                "ayah_number": 155,
                "ayah_text": "And We will surely test you with something of fear and hunger and a loss of wealth and lives and fruits, but give glad tidings to the patient",
                "topic": "patience, testing"
            },
            {
                "surah_number": 2,
                "surah_name": "Al-Baqarah",
                "ayah_number": 286,
                "ayah_text": "Allah does not burden a soul beyond that it can bear",
                "topic": "relief, ease"
            },
            {
                "surah_number": 39,
                "surah_name": "Az-Zumar",
                "ayah_number": 53,
                "ayah_text": "Say, 'O My servants who have transgressed against themselves [by sinning], do not despair of the mercy of Allah'",
                "topic": "repentance, forgiveness, hope"
            },
            {
                "surah_number": 97,
                "surah_name": "Al-Qadr",
                "ayah_number": 1,
                "ayah_text": "Indeed, We sent the Qur'an down during the Night of Decree",
                "topic": "Ramadan, blessing"
            }
        ]
        
        # Sample Quran verses (Arabic)
        sample_quran_arabic = [
            {
                "surah_number": 94,
                "surah_name": "الشرح",
                "ayah_number": 1,
                "ayah_text": "ألم نشرح لك صدرك",
                "topic": "comfort, ease"
            },
            {
                "surah_number": 2,
                "surah_name": "البقرة",
                "ayah_number": 155,
                "ayah_text": "ولنبلونكم بشيء من الخوف والجوع ونقص من الأموال والأنفس والثمرات وبشر الصابرين",
                "topic": "patience, testing"
            }
        ]
        
        # Sample Hadiths
        sample_hadiths = [
            {
                "hadith_number": "1234",
                "narrator": "Abu Huraira",
                "hadith_text_arabic": "قال النبي صلى الله عليه وسلم: الصبر نور",
                "hadith_text_english": "The Prophet (peace be upon him) said: 'Patience is a light'",
                "topic": "patience",
                "source": "Sahih Muslim"
            },
            {
                "hadith_number": "5678",
                "narrator": "Anas ibn Malik",
                "hadith_text_arabic": "قال رسول الله صلى الله عليه وسلم: من تاب قبل موته بسنة قَبِل الله توبته",
                "hadith_text_english": "The Messenger of Allah (peace be upon him) said: 'Whoever repents before death by a year, Allah accepts their repentance'",
                "topic": "repentance",
                "source": "Jami' at-Tirmidhi"
            }
        ]
        
        # Check if data already exists
        if db.query(QuranEnglish).count() > 0:
            print("Data already exists in database. Skipping population...")
            return
        
        # Add English Quran verses
        print("Adding sample English Quran verses...")
        for verse_data in sample_quran_english:
            verse = QuranEnglish(**verse_data)
            db.add(verse)
        
        # Add Arabic Quran verses
        print("Adding sample Arabic Quran verses...")
        for verse_data in sample_quran_arabic:
            verse = QuranArabic(**verse_data)
            db.add(verse)
        
        # Add Hadiths
        print("Adding sample Hadiths...")
        for hadith_data in sample_hadiths:
            hadith = Hadith(**hadith_data)
            db.add(hadith)
        
        db.commit()
        print("✓ Sample data populated successfully!")
        print(f"  - Quran English: {len(sample_quran_english)} verses")
        print(f"  - Quran Arabic: {len(sample_quran_arabic)} verses")
        print(f"  - Hadiths: {len(sample_hadiths)}")
        
    except Exception as e:
        db.rollback()
        print(f"✗ Error populating data: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    # Create tables first
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✓ Tables created successfully!")
    
    # Populate sample data
    populate_sample_data()
