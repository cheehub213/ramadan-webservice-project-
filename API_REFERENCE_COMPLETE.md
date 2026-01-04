# 📚 API Documentation - Complete Reference

## Overview

The Ramadan WebService API v2.0 combines AI-powered spiritual guidance with direct access to Islamic scholars (Imams). It provides:

- 🤖 **Intelligent Quranic/Hadith Search** powered by Deepseek AI
- 🌍 **Bilingual Responses** in English & Arabic
- 📖 **Detailed Explanations** with relevance scoring
- 🕌 **Real Imam Consultations** for complex situations
- ⭐ **Verification & Ratings** system for imams

---

## Base URL

```
http://localhost:8001/api/v1
```

---

## Authentication

Currently, the API uses email-based identification for users. Future versions will implement:
- JWT tokens
- OAuth2 integration
- Role-based access control (User, Imam, Admin)

---

## Health Check

### Endpoint
```
GET /health
```

### Response
```json
{
  "status": "healthy",
  "timestamp": "2026-01-01T12:00:00",
  "version": "2.0.0"
}
```

---

## Search Endpoints

### 1. Search for Islamic Guidance

**Endpoint:** `POST /search/answer`

**Description:** Get Islamic guidance on any life question using Deepseek AI analysis combined with Quranic verses and hadiths.

**Request Body:**
```json
{
  "prompt": "I'm having difficulties with my marriage communication",
  "response_language": "bilingual"
}
```

**Parameters:**
- `prompt` (required): The question or concern
- `response_language` (optional): One of:
  - `"english"` - Response in English only
  - `"arabic"` - Response in Arabic only
  - `"bilingual"` - Response in both languages (default)

**Response:**
```json
{
  "topic": "Marriage and Communication",
  "emotion": "Concerned",
  "keywords": ["marriage", "communication", "family"],
  "quran_verses": [
    {
      "verse": "Quran 4:21",
      "text": "And you have taken from them a solemn covenant. (Quran 4:21)",
      "explanation_en": "This verse emphasizes the importance of honoring marital contracts...",
      "explanation_ar": "تؤكد هذه الآية على أهمية احترام العقد الزوجي...",
      "relevance_score": 0.95,
      "matched_keywords": ["marriage", "covenant"]
    }
  ],
  "hadiths": [
    {
      "hadith": "Sahih Al-Bukhari 3331",
      "text": "The best of you are those who are best to their wives...",
      "explanation_en": "This hadith establishes the Islamic principle of treating wives with kindness...",
      "explanation_ar": "يؤسس هذا الحديث لمبدأ إسلامي بمعاملة الزوجات باللطف...",
      "relevance_score": 0.98,
      "matched_keywords": ["wives", "kindness"]
    }
  ]
}
```

**Status Codes:**
- `200`: Successful guidance retrieval
- `400`: Invalid input
- `500`: Server error

---

### 2. Search Quran Verses

**Endpoint:** `GET /search/quran`

**Description:** Search for specific Quranic verses by topic or keyword.

**Query Parameters:**
```
topic: Topic to search (e.g., "marriage", "patience", "forgiveness")
limit: Maximum number of results (default: 10, max: 50)
```

**Example Request:**
```
GET /search/quran?topic=patience&limit=5
```

**Response:**
```json
[
  {
    "verse": "Quran 16:127",
    "text": "So be patient. Indeed, Allah is with the patient...",
    "surah_number": 16,
    "verse_number": 127,
    "explanation_en": "This verse encourages patience in the face of trials...",
    "explanation_ar": "تشجع هذه الآية على الصبر في مواجهة المحن...",
    "relevance_score": 0.92,
    "matched_keywords": ["patience", "Allah", "trials"]
  }
]
```

---

### 3. Search Hadiths

**Endpoint:** `GET /search/hadith`

**Description:** Search for authentic hadiths by topic or keyword.

**Query Parameters:**
```
topic: Topic to search (e.g., "kindness", "patience", "prayer")
limit: Maximum number of results (default: 10, max: 50)
```

**Example Request:**
```
GET /search/hadith?topic=kindness&limit=5
```

**Response:**
```json
[
  {
    "hadith": "Sahih Al-Bukhari 3331",
    "text": "The best of you are those who are best to their wives...",
    "collection": "Sahih Al-Bukhari",
    "hadith_number": 3331,
    "narrator": "Abu Hurairah",
    "explanation_en": "This hadith emphasizes the importance of treating spouses with kindness...",
    "explanation_ar": "يؤكد هذا الحديث على أهمية معاملة الزوجين باللطف...",
    "relevance_score": 0.89,
    "matched_keywords": ["kindness", "wives", "treatment"]
  }
]
```

---

## Imam Consultation Endpoints

### 1. List Available Imams

**Endpoint:** `GET /imam/imams`

**Description:** Browse available imams for consultation with optional filtering.

**Query Parameters:**
```
specialization: Filter by expertise (general, fiqh, quran, hadith, family, youth, business, spirituality)
madhab: Filter by Islamic school (Hanafi, Maliki, Shafi'i, Hanbali)
available_only: Show only available imams (default: true)
min_rating: Minimum rating (0.0-5.0, default: 0.0)
language: Filter by language spoken
```

**Example Request:**
```
GET /imam/imams?specialization=family&madhab=Hanafi&min_rating=4.5&available_only=true
```

**Response:**
```json
[
  {
    "id": 1,
    "name": "Dr. Mohammad Ahmed",
    "title": "Mufti",
    "specializations": "family,fiqh,madhab",
    "madhab": "Hanafi",
    "bio": "20 years of Islamic scholarship specializing in family matters...",
    "consultation_methods": "phone,email,video",
    "consultation_fee": 50.0,
    "currency": "USD",
    "is_available": true,
    "languages": "English,Arabic,Urdu",
    "average_rating": 4.9,
    "total_consultations": 247,
    "verified": true
  }
]
```

---

### 2. Get Imam Details

**Endpoint:** `GET /imam/imams/{imam_id}`

**Description:** Get complete profile and credentials of a specific imam.

**Path Parameters:**
```
imam_id: ID of the imam (required)
```

**Example Request:**
```
GET /imam/imams/1
```

**Response:**
```json
{
  "id": 1,
  "name": "Dr. Mohammad Ahmed",
  "title": "Mufti",
  "specializations": "family,fiqh,madhab",
  "madhab": "Hanafi",
  "bio": "Dr. Mohammad Ahmed is a respected Islamic scholar with over 20 years of experience...",
  "years_experience": 20,
  "qualifications": "Masters in Islamic Studies from Al-Azhar University; Certified Islamic Counselor",
  "email": "imam@example.com",
  "phone": "+1-555-0100",
  "website": "https://imam.example.com",
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

### 3. Get Imams by Specialization

**Endpoint:** `GET /imam/imams/by-specialization/{specialization}`

**Description:** Find all imams specializing in a specific area.

**Path Parameters:**
```
specialization: Area of expertise (family, fiqh, quran, hadith, etc.)
```

**Example Request:**
```
GET /imam/imams/by-specialization/family
```

**Response:** Array of imam profiles specializing in that area

---

### 4. Book a Consultation

**Endpoint:** `POST /imam/consultations/book`

**Description:** Schedule a consultation with an imam.

**Request Body:**
```json
{
  "imam_id": 1,
  "title": "Marriage and Communication Issues",
  "description": "I'm experiencing tension in my marriage regarding communication...",
  "category": "family",
  "madhab_preference": "Hanafi",
  "user_email": "user@example.com",
  "preferred_method": "phone",
  "preferred_date": "2026-01-15T18:00:00",
  "duration_minutes": 45,
  "original_prompt": "I have marriage problems",
  "deepseek_response": "Islamic teachings emphasize kindness and communication...",
  "reason_for_consultation": "The AI answer was too general. Need madhab-specific guidance."
}
```

**Fields:**
- `imam_id` (required): ID of the imam to book with
- `title` (required): Brief title of your concern
- `description` (required): Detailed description of your situation
- `category` (required): Category (family, fiqh, quran, hadith, business, youth, spiritual, general)
- `madhab_preference` (optional): Your Islamic school preference
- `user_email` (required): Your email address
- `preferred_method` (required): Preferred consultation method (phone, email, video, in_person, messaging)
- `preferred_date` (required): Preferred date/time for consultation
- `duration_minutes` (optional): Expected consultation duration
- `original_prompt` (optional): Your original question
- `deepseek_response` (optional): AI response you found insufficient
- `reason_for_consultation` (optional): Why you're seeking imam guidance

**Response:**
```json
{
  "id": 1,
  "imam_id": 1,
  "user_email": "user@example.com",
  "title": "Marriage and Communication Issues",
  "category": "family",
  "madhab_preference": "Hanafi",
  "status": "pending",
  "preferred_method": "phone",
  "preferred_date": "2026-01-15T18:00:00",
  "created_at": "2026-01-01T10:00:00",
  "updated_at": "2026-01-01T10:00:00"
}
```

**Status Codes:**
- `200`: Consultation booked successfully
- `400`: Invalid input or imam not available
- `404`: Imam not found
- `500`: Server error

---

### 5. Get Consultation Details

**Endpoint:** `GET /imam/consultations/{consultation_id}`

**Description:** Retrieve complete details of a consultation including imam's notes and resolution.

**Path Parameters:**
```
consultation_id: ID of the consultation
```

**Example Request:**
```
GET /imam/consultations/1
```

**Response:**
```json
{
  "id": 1,
  "imam_id": 1,
  "user_email": "user@example.com",
  "title": "Marriage and Communication Issues",
  "description": "I'm experiencing tension in my marriage...",
  "category": "family",
  "madhab_preference": "Hanafi",
  "original_prompt": "I have marriage problems",
  "deepseek_response": "Islamic teachings emphasize...",
  "reason_for_consultation": "The AI answer was too general",
  "preferred_method": "phone",
  "preferred_date": "2026-01-15T18:00:00",
  "actual_date": "2026-01-15T18:00:00",
  "status": "completed",
  "imam_notes": "Discussed marriage dynamics in detail...",
  "resolution": "Based on Hanafi madhab: 1. Improve communication... 2. Regarding finances...",
  "rating": 5,
  "review": "Excellent guidance! Very helpful.",
  "created_at": "2026-01-01T10:00:00",
  "updated_at": "2026-01-15T20:00:00"
}
```

---

### 6. Get User's Consultations

**Endpoint:** `GET /imam/consultations/user/{user_email}`

**Description:** Retrieve all consultations for a specific user.

**Path Parameters:**
```
user_email: User's email address
```

**Example Request:**
```
GET /imam/consultations/user/user@example.com
```

**Response:** Array of consultation records for the user

---

### 7. Confirm Consultation (Imam)

**Endpoint:** `PUT /imam/consultations/{consultation_id}/confirm`

**Description:** Imam confirms booking and provides contact details.

**Request Body:**
```json
{
  "status": "confirmed",
  "actual_date": "2026-01-15T18:00:00",
  "imam_notes": "Confirmed. Please call +1-555-0100 at 6 PM EST."
}
```

**Response:** Updated consultation record

---

### 8. Complete Consultation (Imam)

**Endpoint:** `PUT /imam/consultations/{consultation_id}/complete`

**Description:** Mark consultation as complete with resolution and notes.

**Request Body:**
```json
{
  "imam_notes": "Discussed user's marriage situation in detail",
  "resolution": "Based on Hanafi madhab:\n\n1. Communication: Implement weekly family meetings...\n\n2. Financial Management: Discuss household budget together..."
}
```

**Response:** Updated consultation record with status "completed"

---

### 9. Rate Consultation

**Endpoint:** `PUT /imam/consultations/{consultation_id}/rate`

**Description:** Rate and review a completed consultation.

**Request Body:**
```json
{
  "rating": 5,
  "review": "Excellent guidance! The imam truly understood my situation and provided practical Islamic solutions."
}
```

**Fields:**
- `rating` (required): Rating from 1-5 stars
- `review` (required): Written review of the consultation

**Response:** Updated consultation with rating and review

**Note:** Rating automatically updates the imam's average rating in their profile.

---

### 10. Cancel Consultation

**Endpoint:** `PUT /imam/consultations/{consultation_id}/cancel`

**Description:** Cancel a pending or confirmed consultation.

**Response:** Updated consultation with status "cancelled"

**Note:** Can only cancel consultations with status "pending" or "confirmed", not completed ones.

---

## Common Response Formats

### Success Response (200)
```json
{
  "id": 1,
  "status": "success",
  "data": { ... }
}
```

### Error Response (4xx, 5xx)
```json
{
  "detail": "Error message describing what went wrong"
}
```

### Pagination Response
```json
{
  "items": [...],
  "total": 45,
  "page": 1,
  "page_size": 10
}
```

---

## Error Codes

| Code | Meaning | Solution |
|------|---------|----------|
| 400 | Bad Request | Check your request body for invalid fields |
| 401 | Unauthorized | Provide valid authentication credentials |
| 404 | Not Found | Resource doesn't exist (check ID) |
| 422 | Validation Error | Invalid field types or missing required fields |
| 500 | Server Error | Contact support if problem persists |

---

## Rate Limiting

Currently, no rate limiting is enforced. Future versions will implement:
- 100 requests per minute per IP
- 1000 requests per hour per authenticated user
- Separate limits for different endpoint categories

---

## Webhooks (Future)

Planned webhook events:
- `consultation.booked`
- `consultation.confirmed`
- `consultation.completed`
- `imam.rating_updated`
- `new_guidance_available`

---

## Integration Examples

### Example 1: Simple Guidance Request
```bash
curl -X POST http://localhost:8001/api/v1/search/answer \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "How should I handle conflicts with my family?",
    "response_language": "bilingual"
  }'
```

### Example 2: Browse Imams and Book Consultation
```bash
# Step 1: List available family counselors
curl http://localhost:8001/api/v1/imam/imams?specialization=family&min_rating=4.5

# Step 2: Book consultation with selected imam
curl -X POST http://localhost:8001/api/v1/imam/consultations/book \
  -H "Content-Type: application/json" \
  -d '{
    "imam_id": 1,
    "title": "Family Conflict Resolution",
    "description": "Detailed situation...",
    "category": "family",
    "user_email": "user@example.com",
    "preferred_method": "phone",
    "preferred_date": "2026-01-15T18:00:00"
  }'
```

### Example 3: Complete Consultation and Rate
```bash
# Step 1: Mark consultation complete
curl -X PUT http://localhost:8001/api/v1/imam/consultations/1/complete \
  -H "Content-Type: application/json" \
  -d '{
    "resolution": "Based on Islamic teachings: ..."
  }'

# Step 2: Rate the consultation
curl -X PUT http://localhost:8001/api/v1/imam/consultations/1/rate \
  -H "Content-Type: application/json" \
  -d '{
    "rating": 5,
    "review": "Excellent guidance!"
  }'
```

---

## API Versioning

Current Version: **2.0.0**

Changes in v2.0.0:
- ✨ Added Imam Consultation system
- ✨ Added bilingual response support
- ✨ Added explanation generation
- 📊 Added relevance scoring
- 🔑 Added matched keywords tracking

Backwards compatible with v1.0.0 endpoints.

---

## Support & Documentation

- 📖 [Imam Consultation Guide](IMAM_CONSULTATION_GUIDE.md)
- 📚 [Imam Management Guide](IMAM_MANAGEMENT_GUIDE.md)
- 🔍 [Bilingual Features Guide](BILINGUAL_FEATURES.md)
- 📋 [Quick Reference](QUICK_REFERENCE.md)
- 🧪 [Test Cases](TESTING_GUIDE.md)

For issues, contact: support@ramaданservice.com

---

**Building bridges between AI-powered guidance and Islamic scholarship! 🕌**
