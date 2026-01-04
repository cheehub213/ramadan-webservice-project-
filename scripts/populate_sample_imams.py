#!/usr/bin/env python3
"""
Script to populate sample imam data in the database.
Run this after initializing the database tables.

Usage:
    python scripts/populate_sample_imams.py
"""

import sys
from datetime import datetime
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.database import SessionLocal
from app.models.imam import Imam, Consultation, ConsultationStatus
from sqlalchemy.exc import IntegrityError


def create_sample_imams():
    """Create sample imam profiles."""
    db = SessionLocal()
    
    sample_imams = [
        {
            "name": "Dr. Mohammad Ahmed Hassan",
            "title": "Mufti",
            "specializations": "general,fiqh,madhab",
            "madhab": "Hanafi",
            "bio": "Dr. Mohammad Ahmed Hassan is a respected Islamic scholar with over 20 years of experience in Islamic jurisprudence. He holds a Masters degree from Al-Azhar University and is certified in Islamic counseling. Known for clear explanations and practical guidance.",
            "years_experience": 20,
            "qualifications": "Masters in Islamic Studies from Al-Azhar University, Egypt; Certified Islamic Counselor; Qur'an Memorizer (Hafiz)",
            "email": "dr.ahmad@islamicguidance.com",
            "phone": "+1-555-0100",
            "website": "https://dr-ahmad.example.com",
            "consultation_methods": "phone,email,video",
            "consultation_fee": 50.0,
            "currency": "USD",
            "is_available": True,
            "languages": "English,Arabic,Urdu",
            "timezone": "EST",
            "average_rating": 4.9,
            "total_consultations": 247,
            "total_reviews": 180,
            "verified": True,
        },
        {
            "name": "Shaikh Abdullah Hassan Al-Rashid",
            "title": "Shaikh",
            "specializations": "family,youth,spirituality",
            "madhab": "Maliki",
            "bio": "Shaikh Abdullah specializes in family and youth counseling with deep Islamic understanding. He has helped hundreds of families navigate marriage, parenting, and relationship challenges while maintaining Islamic principles.",
            "years_experience": 15,
            "qualifications": "Bachelor's in Islamic Law from University of Medina; Advanced Tafsir Studies; Family Counseling Certification",
            "email": "shaikh.abdullah@familyguidance.com",
            "phone": "+44-20-7946-0958",
            "website": "https://shaikh-abdullah.example.com",
            "consultation_methods": "phone,email,video,messaging",
            "consultation_fee": 45.0,
            "currency": "GBP",
            "is_available": True,
            "languages": "English,Arabic,Urdu",
            "timezone": "GMT",
            "average_rating": 4.8,
            "total_consultations": 189,
            "total_reviews": 156,
            "verified": True,
        },
        {
            "name": "Dr. Karim Al-Rashid Muhammad",
            "title": "Dr.",
            "specializations": "business,fiqh,madhab",
            "madhab": "Shafi'i",
            "bio": "Dr. Karim is an expert in Islamic business ethics and halal compliance. With both a PhD in Islamic Finance and a CPA, he provides practical guidance on business decisions, investments, and financial matters from an Islamic perspective.",
            "years_experience": 18,
            "qualifications": "PhD in Islamic Finance from King Abdulaziz University; CPA (Certified Public Accountant); Islamic Banking Expert",
            "email": "dr.karim@businessislam.com",
            "phone": "+966-11-4654-3210",
            "website": "https://dr-karim-business.example.com",
            "consultation_methods": "phone,email,video",
            "consultation_fee": 75.0,
            "currency": "SAR",
            "is_available": True,
            "languages": "English,Arabic",
            "timezone": "AST",
            "average_rating": 4.7,
            "total_consultations": 134,
            "total_reviews": 98,
            "verified": True,
        },
        {
            "name": "Imam Muhammad Samir",
            "title": "Imam",
            "specializations": "quran,hadith,spirituality",
            "madhab": "Hanbali",
            "bio": "Imam Muhammad is a Quran scholar with expertise in Islamic tradition and spirituality. He has extensive knowledge of Quranic interpretation and hadith sciences, helping individuals deepen their understanding of Islamic teachings.",
            "years_experience": 22,
            "qualifications": "Bachelor's in Islamic Studies from Umm Al-Qura University; Qur'an Memorizer (Hafiz); Hadith Specialist",
            "email": "imam.samir@quranwisdom.com",
            "phone": "+966-12-2156-7890",
            "website": "https://imam-samir.example.com",
            "consultation_methods": "phone,email,video,in_person",
            "consultation_fee": 40.0,
            "currency": "SAR",
            "is_available": True,
            "languages": "English,Arabic",
            "timezone": "AST",
            "average_rating": 4.9,
            "total_consultations": 312,
            "total_reviews": 289,
            "verified": True,
        },
        {
            "name": "Dr. Fatima Al-Ansari",
            "title": "Dr.",
            "specializations": "family,youth,spirituality",
            "madhab": "Maliki",
            "bio": "Dr. Fatima brings a unique perspective as a female Islamic scholar specializing in women's issues, family dynamics, and youth guidance. She is particularly helpful for issues related to women's roles in Islam and family dynamics.",
            "years_experience": 12,
            "qualifications": "Masters in Islamic Studies; PhD in Islamic Law; Women's Islamic Leadership Certificate",
            "email": "dr.fatima@islamicwomen.com",
            "phone": "+966-50-1234-5678",
            "website": "https://dr-fatima.example.com",
            "consultation_methods": "phone,email,video,messaging",
            "consultation_fee": 55.0,
            "currency": "USD",
            "is_available": True,
            "languages": "English,Arabic,French",
            "timezone": "AST",
            "average_rating": 4.8,
            "total_consultations": 167,
            "total_reviews": 142,
            "verified": True,
        },
        {
            "name": "Shaikh Ibrahim Hassan",
            "title": "Shaikh",
            "specializations": "general,fiqh,youth",
            "madhab": "Hanafi",
            "bio": "Shaikh Ibrahim is a young, energetic Islamic scholar with a gift for connecting with youth. He specializes in explaining Islamic concepts in modern context while maintaining traditional Islamic values.",
            "years_experience": 8,
            "qualifications": "Bachelor's in Islamic Studies; Youth Engagement Specialist; Digital Islamic Education Expert",
            "email": "shaikh.ibrahim@youthislam.com",
            "phone": "+1-555-2000",
            "website": "https://shaikh-ibrahim.example.com",
            "consultation_methods": "phone,email,video,messaging",
            "consultation_fee": 35.0,
            "currency": "USD",
            "is_available": True,
            "languages": "English,Arabic",
            "timezone": "EST",
            "average_rating": 4.6,
            "total_consultations": 89,
            "total_reviews": 72,
            "verified": True,
        },
        {
            "name": "Dr. Ahmed Al-Khatib",
            "title": "Dr.",
            "specializations": "quran,fiqh,madhab",
            "madhab": "Shafi'i",
            "bio": "Dr. Ahmed is a renowned Quranic scholar with expertise in Tafsir (Quranic interpretation). His deep knowledge of classical Islamic texts combined with modern analytical skills makes him excellent for complex theological questions.",
            "years_experience": 25,
            "qualifications": "PhD in Islamic Studies from Cairo University; Expert in Tafsir; Classical Arabic Scholar",
            "email": "dr.ahmed.khatib@quranicstudies.com",
            "phone": "+20-2-2578-1234",
            "website": "https://dr-ahmed-khatib.example.com",
            "consultation_methods": "phone,email,video",
            "consultation_fee": 65.0,
            "currency": "EGP",
            "is_available": True,
            "languages": "English,Arabic,Turkish",
            "timezone": "EET",
            "average_rating": 4.9,
            "total_consultations": 256,
            "total_reviews": 201,
            "verified": True,
        },
        {
            "name": "Imam Hassan Al-Turki",
            "title": "Imam",
            "specializations": "general,spirituality",
            "madhab": "Hanbali",
            "bio": "Imam Hassan brings warm, compassionate Islamic guidance focused on spiritual growth and emotional well-being. Perfect for those seeking holistic Islamic perspective on life challenges.",
            "years_experience": 10,
            "qualifications": "Islamic Studies Degree; Spiritual Counseling Certification; Qur'an Memorizer",
            "email": "imam.hassan@spiritualguidance.com",
            "phone": "+971-4-3331-234",
            "website": "https://imam-hassan.example.com",
            "consultation_methods": "phone,email,video,messaging,in_person",
            "consultation_fee": 45.0,
            "currency": "AED",
            "is_available": True,
            "languages": "English,Arabic,Urdu",
            "timezone": "GST",
            "average_rating": 4.7,
            "total_consultations": 128,
            "total_reviews": 94,
            "verified": True,
        },
    ]
    
    created_count = 0
    skipped_count = 0
    
    print("📚 Populating sample imam data...")
    print("-" * 60)
    
    for imam_data in sample_imams:
        try:
            # Check if imam already exists
            existing = db.query(Imam).filter(Imam.email == imam_data["email"]).first()
            if existing:
                print(f"⏭️  Skipped: {imam_data['name']} (already exists)")
                skipped_count += 1
                continue
            
            imam = Imam(**imam_data)
            db.add(imam)
            db.commit()
            print(f"✅ Created: {imam_data['name']} ({imam_data['madhab']}) - ID: {imam.id}")
            created_count += 1
            
        except IntegrityError as e:
            db.rollback()
            print(f"❌ Error creating {imam_data['name']}: {str(e)}")
            skipped_count += 1
        except Exception as e:
            db.rollback()
            print(f"❌ Unexpected error: {str(e)}")
            skipped_count += 1
    
    print("-" * 60)
    print(f"\n📊 Summary:")
    print(f"   ✅ Created: {created_count}")
    print(f"   ⏭️  Skipped: {skipped_count}")
    print(f"   📦 Total: {created_count + skipped_count}")
    
    db.close()


def create_sample_consultations():
    """Create sample consultation records for demonstration."""
    db = SessionLocal()
    
    sample_consultations = [
        {
            "imam_id": 1,
            "user_email": "sample_user_1@example.com",
            "title": "Marriage Communication Issues",
            "description": "My spouse and I are having difficulty communicating about financial matters and household responsibilities.",
            "category": "family",
            "madhab_preference": "Hanafi",
            "original_prompt": "How can we improve communication in marriage?",
            "deepseek_response": "Communication is key to a healthy marriage according to Islamic teachings...",
            "reason_for_consultation": "Need specific Hanafi perspective on financial management in marriage.",
            "preferred_method": "phone",
            "preferred_date": datetime(2026, 1, 15, 18, 0),
            "duration_minutes": 45,
            "status": "completed",
            "imam_notes": "Discussed Islamic principles of partnership in marriage.",
            "resolution": "Based on Hanafi madhab: Both spouses should have transparent discussions about finances. Women in Islam have full right to their own wealth...",
            "rating": 5,
            "review": "Excellent and practical guidance! The Imam understood our cultural context and provided solutions rooted in Islamic principles."
        },
        {
            "imam_id": 2,
            "user_email": "sample_user_2@example.com",
            "title": "Youth Islamic Identity",
            "description": "My teenage son is struggling to maintain Islamic practices while fitting in with his peers at school.",
            "category": "youth",
            "madhab_preference": "Maliki",
            "original_prompt": "How can young people maintain Islam in secular environments?",
            "deepseek_response": "Islamic teachings provide guidance on maintaining faith in diverse environments...",
            "reason_for_consultation": "Looking for practical strategies specific to his situation.",
            "preferred_method": "video",
            "preferred_date": datetime(2026, 1, 20, 19, 0),
            "duration_minutes": 60,
            "status": "completed",
            "imam_notes": "Provided practical strategies for Muslim youth.",
            "resolution": "Frame Islamic practices as identity and strength. Encourage Muslim youth groups. Balance social needs with religious commitments...",
            "rating": 5,
            "review": "Very helpful! Shaikh provided practical strategies our son could actually implement."
        },
        {
            "imam_id": 3,
            "user_email": "sample_user_3@example.com",
            "title": "Business Partnership Ethics",
            "description": "Considering a business partnership but concerned about certain practices.",
            "category": "business",
            "madhab_preference": "Shafi'i",
            "original_prompt": "Is this business arrangement halal?",
            "deepseek_response": "Islamic principles guide ethical business practices...",
            "reason_for_consultation": "Need expert Islamic finance perspective before committing.",
            "preferred_method": "email",
            "preferred_date": datetime(2026, 1, 22, 10, 0),
            "duration_minutes": 30,
            "status": "completed",
            "imam_notes": "Analyzed partnership agreement from Islamic perspective.",
            "resolution": "The partnership structure is permissible under Shafi'i madhab with these considerations...",
            "rating": 5,
            "review": "Dr. Karim's expertise in Islamic finance was invaluable. Clear recommendations we could act on."
        },
    ]
    
    created_count = 0
    skipped_count = 0
    
    print("\n📅 Populating sample consultation data...")
    print("-" * 60)
    
    for consultation_data in sample_consultations:
        try:
            # Check if consultation already exists
            existing = db.query(Consultation).filter(
                (Consultation.imam_id == consultation_data["imam_id"]) &
                (Consultation.user_email == consultation_data["user_email"]) &
                (Consultation.title == consultation_data["title"])
            ).first()
            
            if existing:
                print(f"⏭️  Skipped: {consultation_data['title']} (already exists)")
                skipped_count += 1
                continue
            
            consultation = Consultation(**consultation_data)
            db.add(consultation)
            db.commit()
            print(f"✅ Created: {consultation_data['title']} - ID: {consultation.id}")
            created_count += 1
            
        except IntegrityError as e:
            db.rollback()
            print(f"❌ Error creating consultation: {str(e)}")
            skipped_count += 1
        except Exception as e:
            db.rollback()
            print(f"❌ Unexpected error: {str(e)}")
            skipped_count += 1
    
    print("-" * 60)
    print(f"\n📊 Consultations Summary:")
    print(f"   ✅ Created: {created_count}")
    print(f"   ⏭️  Skipped: {skipped_count}")
    print(f"   📦 Total: {created_count + skipped_count}")
    
    db.close()


def main():
    """Main entry point."""
    print("\n" + "=" * 60)
    print("🕌 RAMADAN SERVICE - SAMPLE DATA POPULATION")
    print("=" * 60 + "\n")
    
    try:
        create_sample_imams()
        create_sample_consultations()
        
        print("\n" + "=" * 60)
        print("✅ Sample data population complete!")
        print("=" * 60)
        print("\n🎯 Next steps:")
        print("   1. Start the API server: python -m uvicorn app.main:app --reload")
        print("   2. Visit Swagger UI: http://localhost:8001/docs")
        print("   3. Test the endpoints:")
        print("      - GET /api/v1/imam/imams (list all imams)")
        print("      - GET /api/v1/imam/imams/1 (get specific imam)")
        print("      - GET /api/v1/imam/consultations/user/sample_user_1@example.com (view consultations)")
        print("\n")
        
    except Exception as e:
        print(f"\n❌ Error during population: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
