# 🧪 Imam Consultation API - Complete Test Inputs

## Quick Test Commands

Run these commands in your terminal after starting the API server on port 8001.

---

## 1️⃣ LIST ALL IMAMS

### Command
```bash
curl http://localhost:8001/api/v1/imam/imams
```

### Expected Response
```json
[
  {
    "id": 1,
    "name": "Dr. Mohammad Ahmed Hassan",
    "title": "Mufti",
    "specializations": "general,fiqh,madhab",
    "madhab": "Hanafi",
    "consultation_fee": 50.0,
    "is_available": true,
    "average_rating": 4.9,
    "verified": true
  },
  ...
]
```

---

## 2️⃣ LIST IMAMS WITH FILTERS

### Filter by Specialization
```bash
curl "http://localhost:8001/api/v1/imam/imams?specialization=family"
```

### Filter by Madhab
```bash
curl "http://localhost:8001/api/v1/imam/imams?madhab=Hanafi"
```

### Filter by Rating
```bash
curl "http://localhost:8001/api/v1/imam/imams?min_rating=4.5"
```

### Combined Filters
```bash
curl "http://localhost:8001/api/v1/imam/imams?specialization=family&madhab=Hanafi&min_rating=4.5&available_only=true"
```

---

## 3️⃣ GET SPECIFIC IMAM

### Get Imam ID 1
```bash
curl http://localhost:8001/api/v1/imam/imams/1
```

### Get Imam ID 2
```bash
curl http://localhost:8001/api/v1/imam/imams/2
```

### Expected Response
```json
{
  "id": 1,
  "name": "Dr. Mohammad Ahmed Hassan",
  "title": "Mufti",
  "specializations": "general,fiqh,madhab",
  "madhab": "Hanafi",
  "bio": "Dr. Mohammad Ahmed Hassan is a respected Islamic scholar...",
  "years_experience": 20,
  "qualifications": "Masters in Islamic Studies from Al-Azhar University",
  "email": "dr.ahmad@islamicguidance.com",
  "phone": "+1-555-0100",
  "website": "https://dr-ahmad.example.com",
  "consultation_methods": "phone,email,video",
  "consultation_fee": 50.0,
  "currency": "USD",
  "is_available": true,
  "languages": "English,Arabic,Urdu",
  "timezone": "EST",
  "average_rating": 4.9,
  "total_consultations": 247,
  "total_reviews": 180,
  "verified": true,
  "created_at": "2025-01-01T10:00:00",
  "updated_at": "2026-01-01T15:30:00"
}
```

---

## 4️⃣ GET IMAMS BY SPECIALIZATION

### Get Family Counselors
```bash
curl http://localhost:8001/api/v1/imam/imams/by-specialization/family
```

### Get Quran Experts
```bash
curl http://localhost:8001/api/v1/imam/imams/by-specialization/quran
```

### Get Business Ethics Experts
```bash
curl http://localhost:8001/api/v1/imam/imams/by-specialization/business
```

### Get Youth Counselors
```bash
curl http://localhost:8001/api/v1/imam/imams/by-specialization/youth
```

---

## 5️⃣ BOOK A CONSULTATION

### Command
```bash
curl -X POST http://localhost:8001/api/v1/imam/consultations/book \
  -H "Content-Type: application/json" \
  -d '{
    "imam_id": 1,
    "title": "Marriage Communication Issues",
    "description": "My spouse and I are having difficulty communicating about financial matters and household responsibilities.",
    "category": "family",
    "madhab_preference": "Hanafi",
    "user_email": "user@example.com",
    "preferred_method": "phone",
    "preferred_date": "2026-01-15T18:00:00",
    "duration_minutes": 45,
    "original_prompt": "How can we improve communication in marriage?",
    "deepseek_response": "Communication is key to a healthy marriage according to Islamic teachings...",
    "reason_for_consultation": "The AI answer was too general. Need specific Hanafi perspective."
  }'
```

### JSON Body (Alternative Format)
```json
{
  "imam_id": 2,
  "title": "Youth Islamic Identity",
  "description": "My teenage son is struggling to maintain Islamic practices while fitting in with peers at school. How can we help him balance both?",
  "category": "youth",
  "madhab_preference": "Maliki",
  "user_email": "parent@example.com",
  "preferred_method": "video",
  "preferred_date": "2026-01-20T19:00:00",
  "duration_minutes": 60,
  "original_prompt": "How can young people maintain Islam in secular environments?",
  "deepseek_response": "Islamic teachings provide guidance on maintaining faith in diverse environments...",
  "reason_for_consultation": "Looking for practical strategies specific to his situation."
}
```

### JSON Body - Business Consultation
```json
{
  "imam_id": 3,
  "title": "Business Partnership Ethics",
  "description": "Considering a business partnership but concerned about certain practices. Need to verify halal compliance.",
  "category": "business",
  "madhab_preference": "Shafi'i",
  "user_email": "businessman@example.com",
  "preferred_method": "email",
  "preferred_date": "2026-01-22T10:00:00",
  "duration_minutes": 30,
  "original_prompt": "Is this business arrangement halal?",
  "deepseek_response": "Islamic principles guide ethical business practices...",
  "reason_for_consultation": "Need expert Islamic finance perspective before committing."
}
```

### Expected Response
```json
{
  "id": 4,
  "imam_id": 1,
  "user_email": "user@example.com",
  "title": "Marriage Communication Issues",
  "description": "My spouse and I are having difficulty communicating...",
  "category": "family",
  "madhab_preference": "Hanafi",
  "status": "pending",
  "preferred_method": "phone",
  "preferred_date": "2026-01-15T18:00:00",
  "created_at": "2026-01-01T10:00:00",
  "updated_at": "2026-01-01T10:00:00"
}
```

---

## 6️⃣ GET CONSULTATION DETAILS

### Get Consultation ID 1
```bash
curl http://localhost:8001/api/v1/imam/consultations/1
```

### Get Consultation ID 4 (newly booked)
```bash
curl http://localhost:8001/api/v1/imam/consultations/4
```

### Expected Response
```json
{
  "id": 1,
  "imam_id": 1,
  "user_email": "sample_user_1@example.com",
  "title": "Marriage Communication Issues",
  "description": "My spouse and I are having difficulty communicating...",
  "category": "family",
  "madhab_preference": "Hanafi",
  "original_prompt": "How can we improve communication in marriage?",
  "deepseek_response": "Communication is key to a healthy marriage according to Islamic teachings...",
  "reason_for_consultation": "Need specific Hanafi perspective on financial management in marriage.",
  "preferred_method": "phone",
  "preferred_date": "2026-01-15T18:00:00",
  "actual_date": "2026-01-15T18:00:00",
  "status": "completed",
  "imam_notes": "Discussed Islamic principles of partnership in marriage.",
  "resolution": "Based on Hanafi madhab: Both spouses should have transparent discussions about finances...",
  "rating": 5,
  "review": "Excellent and practical guidance!"
}
```

---

## 7️⃣ GET USER'S CONSULTATIONS

### Get Consultations for User
```bash
curl http://localhost:8001/api/v1/imam/consultations/user/user@example.com
```

### Get Sample User's Consultations
```bash
curl http://localhost:8001/api/v1/imam/consultations/user/sample_user_1@example.com
```

### Expected Response
```json
[
  {
    "id": 1,
    "imam_id": 1,
    "title": "Marriage Communication Issues",
    "category": "family",
    "status": "completed",
    "rating": 5
  },
  {
    "id": 4,
    "imam_id": 1,
    "title": "Marriage Communication Issues",
    "category": "family",
    "status": "pending",
    "rating": null
  }
]
```

---

## 8️⃣ CONFIRM CONSULTATION (Imam)

### Command
```bash
curl -X PUT http://localhost:8001/api/v1/imam/consultations/4/confirm \
  -H "Content-Type: application/json" \
  -d '{
    "status": "confirmed",
    "actual_date": "2026-01-15T18:00:00",
    "imam_notes": "Confirmed. Please call on +1-555-0100 at 6 PM EST. Have your detailed situation ready for discussion."
  }'
```

### JSON Body (Alternative)
```json
{
  "status": "confirmed",
  "actual_date": "2026-01-20T19:00:00",
  "imam_notes": "Ready to discuss. This is a video consultation. Zoom link will be sent via email 1 hour before."
}
```

### Expected Response
```json
{
  "id": 4,
  "imam_id": 1,
  "user_email": "user@example.com",
  "title": "Marriage Communication Issues",
  "status": "confirmed",
  "actual_date": "2026-01-15T18:00:00",
  "imam_notes": "Confirmed. Please call on +1-555-0100 at 6 PM EST...",
  "updated_at": "2026-01-01T11:00:00"
}
```

---

## 9️⃣ COMPLETE CONSULTATION (Imam)

### Command
```bash
curl -X PUT http://localhost:8001/api/v1/imam/consultations/4/complete \
  -H "Content-Type: application/json" \
  -d '{
    "imam_notes": "Discussed the couple'\''s marriage situation in detail, reviewed Islamic principles of partnership and financial management.",
    "resolution": "Based on Hanafi madhab and your situation, here'\''s my guidance:\n\n1. Communication: Implement weekly family meetings to discuss concerns. Set aside 30 minutes without distractions.\n\n2. Finances: In Islam, both spouses should have transparent conversations about household budget. Wife has full right to her own wealth. Consider creating joint and separate accounts.\n\n3. Parenting: Find compromise that honors both cultural backgrounds while following Islamic principles. Make decisions together through consultation (Shura).\n\nRecommended: Read Surah Al-Nisa verse 21 together. Consider Islamic counseling if issues persist."
  }'
```

### JSON Body (Alternative)
```json
{
  "imam_notes": "Had detailed discussion about youth challenges in secular environments. Provided practical Islamic strategies.",
  "resolution": "Key points from our consultation:\n\n1. Frame Islamic practices as identity and strength, not burden\n2. Encourage Muslim youth groups for peer support\n3. Balance social needs with religious commitments\n4. Learn from Quranic examples of youth facing similar challenges\n5. Build confidence in Islamic values\n\nRecommend: Connect with local Muslim Student Association or youth group."
}
```

### Expected Response
```json
{
  "id": 4,
  "imam_id": 1,
  "user_email": "user@example.com",
  "title": "Marriage Communication Issues",
  "status": "completed",
  "imam_notes": "Discussed the couple's marriage situation...",
  "resolution": "Based on Hanafi madhab and your situation...",
  "updated_at": "2026-01-15T20:00:00"
}
```

---

## 🔟 RATE CONSULTATION

### Command
```bash
curl -X PUT http://localhost:8001/api/v1/imam/consultations/4/rate \
  -H "Content-Type: application/json" \
  -d '{
    "rating": 5,
    "review": "Excellent and practical guidance! The imam understood our situation perfectly and provided clear Islamic solutions based on Hanafi madhab. Highly recommended!"
  }'
```

### JSON Body - 4 Star Rating
```json
{
  "rating": 4,
  "review": "Very helpful guidance. The imam provided solid Islamic perspective. Would have appreciated more concrete examples for our specific situation, but overall excellent service."
}
```

### JSON Body - 3 Star Rating
```json
{
  "rating": 3,
  "review": "Good consultation, provided Islamic perspective. Felt a bit rushed and would have liked more time to discuss follow-up questions."
}
```

### Expected Response
```json
{
  "id": 4,
  "imam_id": 1,
  "user_email": "user@example.com",
  "title": "Marriage Communication Issues",
  "status": "completed",
  "rating": 5,
  "review": "Excellent and practical guidance!...",
  "updated_at": "2026-01-15T20:30:00"
}
```

---

## 1️⃣1️⃣ CANCEL CONSULTATION

### Command (Cancel Pending)
```bash
curl -X PUT http://localhost:8001/api/v1/imam/consultations/4/cancel
```

### Expected Response
```json
{
  "id": 4,
  "imam_id": 1,
  "user_email": "user@example.com",
  "title": "Marriage Communication Issues",
  "status": "cancelled",
  "updated_at": "2026-01-01T12:00:00"
}
```

---

## 📋 TESTING SEQUENCE

Follow this order for a complete test:

### Phase 1: Discovery (5 minutes)
```bash
# 1. List all imams
curl http://localhost:8001/api/v1/imam/imams

# 2. Get one imam's details
curl http://localhost:8001/api/v1/imam/imams/1

# 3. Filter by specialization
curl "http://localhost:8001/api/v1/imam/imams?specialization=family"

# 4. Filter by madhab
curl "http://localhost:8001/api/v1/imam/imams?madhab=Hanafi&min_rating=4.5"
```

### Phase 2: Booking (2 minutes)
```bash
# 5. Book new consultation
curl -X POST http://localhost:8001/api/v1/imam/consultations/book \
  -H "Content-Type: application/json" \
  -d '{
    "imam_id": 1,
    "title": "Test Marriage Issue",
    "description": "Testing the consultation system",
    "category": "family",
    "madhab_preference": "Hanafi",
    "user_email": "testuser@example.com",
    "preferred_method": "phone",
    "preferred_date": "2026-01-15T18:00:00"
  }'

# 6. Get the booked consultation (use ID from response)
curl http://localhost:8001/api/v1/imam/consultations/4
```

### Phase 3: Imam Management (3 minutes)
```bash
# 7. Imam confirms booking
curl -X PUT http://localhost:8001/api/v1/imam/consultations/4/confirm \
  -H "Content-Type: application/json" \
  -d '{
    "status": "confirmed",
    "actual_date": "2026-01-15T18:00:00",
    "imam_notes": "Confirmed. Ready for consultation."
  }'

# 8. Imam completes consultation
curl -X PUT http://localhost:8001/api/v1/imam/consultations/4/complete \
  -H "Content-Type: application/json" \
  -d '{
    "imam_notes": "Provided guidance on marriage issues",
    "resolution": "Based on Islamic teachings and your situation: 1. Improve communication... 2. Regarding finances..."
  }'
```

### Phase 4: Rating (1 minute)
```bash
# 9. User rates consultation
curl -X PUT http://localhost:8001/api/v1/imam/consultations/4/rate \
  -H "Content-Type: application/json" \
  -d '{
    "rating": 5,
    "review": "Excellent guidance!"
  }'
```

### Phase 5: History (1 minute)
```bash
# 10. Check user's consultation history
curl "http://localhost:8001/api/v1/imam/consultations/user/testuser@example.com"
```

**Total Testing Time: ~12 minutes**

---

## 🔍 SAMPLE DATA FOR TESTING

Use these IDs from the pre-loaded sample data:

### Imam IDs Available
- **1** - Dr. Mohammad Ahmed Hassan (Hanafi, Mufti, General/Fiqh)
- **2** - Shaikh Abdullah Hassan (Maliki, Family/Youth)
- **3** - Dr. Karim Al-Rashid (Shafi'i, Business/Fiqh)
- **4** - Imam Muhammad Samir (Hanbali, Quran/Hadith)
- **5** - Dr. Fatima Al-Ansari (Maliki, Family/Women)
- **6** - Shaikh Ibrahim Hassan (Hanafi, General/Youth)
- **7** - Dr. Ahmed Al-Khatib (Shafi'i, Quran/Tafsir)
- **8** - Imam Hassan Al-Turki (Hanbali, General/Spiritual)

### Sample Consultations Pre-loaded
- **1** - Marriage Communication (completed, 5★)
- **2** - Youth Islamic Identity (completed, 5★)
- **3** - Business Partnership (completed, 5★)

### Available Specializations
- general
- fiqh
- quran
- hadith
- family
- youth
- business
- spirituality
- madhab

### Islamic Schools (Madhabs)
- Hanafi
- Maliki
- Shafi'i
- Hanbali

### Consultation Methods
- phone
- email
- video
- in_person
- messaging

### Consultation Categories
- family
- fiqh
- quran
- hadith
- business
- youth
- spiritual
- general

---

## ✅ SUCCESS INDICATORS

After each request, you should see:

| Endpoint | Success Code | Response |
|----------|---|---|
| List Imams | 200 | Array of imams |
| Get Imam | 200 | Single imam object |
| Filter | 200 | Filtered array |
| Book | 200 | Consultation object, status="pending" |
| Get Consultation | 200 | Consultation object |
| User History | 200 | Array of consultations |
| Confirm | 200 | Consultation with status="confirmed" |
| Complete | 200 | Consultation with status="completed" |
| Rate | 200 | Consultation with rating and review |
| Cancel | 200 | Consultation with status="cancelled" |

---

## 🆘 ERROR TESTING

### Test Error Cases

**Imam Not Found**
```bash
curl http://localhost:8001/api/v1/imam/imams/999
# Expected: 404 Not Found
```

**Invalid Imam ID in Booking**
```bash
curl -X POST http://localhost:8001/api/v1/imam/consultations/book \
  -H "Content-Type: application/json" \
  -d '{"imam_id": 999, "title": "Test", ...}'
# Expected: 404 Imam not found
```

**Imam Unavailable**
```bash
# Try booking with unavailable imam
# Expected: 400 Bad Request
```

**Consultation Not Found**
```bash
curl http://localhost:8001/api/v1/imam/consultations/999
# Expected: 404 Not Found
```

---

## 💡 TIPS FOR TESTING

1. **Use Swagger UI** - Open http://localhost:8001/docs for interactive testing
2. **Copy Consultation IDs** - When you book, note the ID returned
3. **Test in Order** - Follow the sequence above
4. **Use Sample Data** - Reference the pre-loaded imams and consultations
5. **Check Responses** - Verify all fields are present
6. **Validate Status** - Confirm status changes correctly
7. **Monitor Ratings** - Check imam ratings update

---

**Ready to test? Start with Phase 1! 🚀**
