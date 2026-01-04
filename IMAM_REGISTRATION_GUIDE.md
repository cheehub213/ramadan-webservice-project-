# 🧑‍🏫 Imam Registration Guide

## Overview

The Ramadan WebService now allows imams to **self-register** to the platform. Once registered, imams will appear in the public imam directory and can accept consultation bookings from users.

---

## Registration Endpoint

### POST /api/v1/imam/imams

Register a new imam to the platform.

**Request Body (JSON):**

```json
{
  "name": "Dr. Mohammad Ahmed Hassan",
  "title": "Mufti",
  "specializations": "general,fiqh,madhab",
  "madhab": "Hanafi",
  "bio": "Dr. Mohammad Ahmed Hassan is a respected Islamic scholar with 20 years of experience in Islamic jurisprudence.",
  "years_experience": 20,
  "qualifications": "Masters in Islamic Studies from Al-Azhar University",
  "email": "imam@example.com",
  "phone": "+1-555-0100",
  "website": "https://example.com",
  "consultation_methods": "phone,email,video",
  "consultation_fee": 50.0,
  "currency": "USD",
  "languages": "English,Arabic,Urdu",
  "timezone": "EST",
  "is_available": true,
  "verified": false
}
```

**Response (HTTP 201 Created):**

```json
{
  "id": 9,
  "name": "Dr. Mohammad Ahmed Hassan",
  "title": "Mufti",
  "specializations": "general,fiqh,madhab",
  "madhab": "Hanafi",
  "bio": "Dr. Mohammad Ahmed Hassan is a respected Islamic scholar...",
  "years_experience": 20,
  "qualifications": "Masters in Islamic Studies from Al-Azhar University",
  "email": "imam@example.com",
  "phone": "+1-555-0100",
  "website": "https://example.com",
  "consultation_methods": "phone,email,video",
  "consultation_fee": 50.0,
  "currency": "USD",
  "is_available": true,
  "languages": "English,Arabic,Urdu",
  "timezone": "EST",
  "average_rating": 5.0,
  "total_consultations": 0,
  "total_reviews": 0,
  "verified": false
}
```

---

## Field Requirements

### Required Fields
- **name** (string): Imam's full name
- **specializations** (string): Comma-separated expertise areas
- **email** (string): Unique email address (must not already exist)
- **consultation_methods** (string): Comma-separated methods offered
- **languages** (string): Comma-separated languages spoken

### Optional Fields
- **title** (string): Title (e.g., "Dr.", "Mufti", "Sheikh", "Imam")
- **madhab** (string): Islamic school - one of: "Hanafi", "Maliki", "Shafi'i", "Hanbali"
- **bio** (string): Biography/description of imam
- **years_experience** (integer): Years of Islamic knowledge/teaching experience
- **qualifications** (string): Educational background and credentials
- **phone** (string): Phone number (with country code if international)
- **website** (string): Personal website or profile URL
- **consultation_fee** (number): Hourly or per-session fee (default: 0)
- **currency** (string): Currency code - default: "USD"
- **languages** (string): Spoken languages (default: "English")
- **timezone** (string): Imam's timezone (e.g., "EST", "PST", "GMT", "IST")
- **is_available** (boolean): Currently available for consultations (default: true)
- **verified** (boolean): Admin-verified badge (default: false, set by admin only)

### Specializations (Valid Values)
- `general` - General Islamic guidance
- `fiqh` - Islamic jurisprudence
- `quran` - Quranic interpretation (Tafsir)
- `hadith` - Hadith knowledge
- `family` - Family and marriage counseling
- `youth` - Youth counseling and mentoring
- `business` - Islamic business ethics
- `spirituality` - Spiritual guidance and practice
- `madhab` - Madhab expertise (specific school)

### Consultation Methods (Valid Values)
- `phone` - Phone call consultation
- `email` - Email correspondence
- `video` - Video call (Zoom, Teams, etc.)
- `in_person` - Face-to-face meeting
- `messaging` - Chat/messaging service

### Languages (Examples)
- English
- Arabic
- Urdu
- French
- Spanish
- Turkish
- Bengali
- Malay
- Indonesian

---

## Registration Examples

### Example 1: Basic Registration

**Request:**
```bash
curl -X POST http://localhost:8001/api/v1/imam/imams \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Shaikh Abdullah Hassan",
    "specializations": "family,youth",
    "email": "shaikh.abdullah@example.com",
    "consultation_methods": "phone,video",
    "languages": "English,Arabic"
  }'
```

**Response (201 Created):**
```json
{
  "id": 9,
  "name": "Shaikh Abdullah Hassan",
  "title": null,
  "specializations": "family,youth",
  "madhab": null,
  "bio": null,
  "years_experience": null,
  "qualifications": null,
  "email": "shaikh.abdullah@example.com",
  "phone": null,
  "website": null,
  "consultation_methods": "phone,video",
  "consultation_fee": 0.0,
  "currency": "USD",
  "is_available": true,
  "languages": "English,Arabic",
  "timezone": null,
  "average_rating": 5.0,
  "total_consultations": 0,
  "total_reviews": 0,
  "verified": false
}
```

---

### Example 2: Full Registration with All Details

**Request:**
```bash
curl -X POST http://localhost:8001/api/v1/imam/imams \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Dr. Karim Al-Rashid",
    "title": "Dr.",
    "specializations": "business,fiqh,madhab",
    "madhab": "Shafi'i",
    "bio": "Islamic finance expert with expertise in Sharia-compliant investments and business ethics.",
    "years_experience": 18,
    "qualifications": "PhD Islamic Finance from INCEIF",
    "email": "dr.karim@islamicbusiness.com",
    "phone": "+1-555-0103",
    "website": "https://karim-rashid.com",
    "consultation_methods": "phone,email,video",
    "consultation_fee": 75.0,
    "currency": "USD",
    "languages": "English,Arabic,Malay",
    "timezone": "PST",
    "is_available": true,
    "verified": false
  }'
```

**Response (201 Created):**
```json
{
  "id": 10,
  "name": "Dr. Karim Al-Rashid",
  "title": "Dr.",
  "specializations": "business,fiqh,madhab",
  "madhab": "Shafi'i",
  "bio": "Islamic finance expert with expertise in Sharia-compliant investments and business ethics.",
  "years_experience": 18,
  "qualifications": "PhD Islamic Finance from INCEIF",
  "email": "dr.karim@islamicbusiness.com",
  "phone": "+1-555-0103",
  "website": "https://karim-rashid.com",
  "consultation_methods": "phone,email,video",
  "consultation_fee": 75.0,
  "currency": "USD",
  "is_available": true,
  "languages": "English,Arabic,Malay",
  "timezone": "PST",
  "average_rating": 5.0,
  "total_consultations": 0,
  "total_reviews": 0,
  "verified": false
}
```

---

### Example 3: Youth Counselor Registration

**Request:**
```bash
curl -X POST http://localhost:8001/api/v1/imam/imams \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Imam Hassan Al-Turki",
    "title": "Imam",
    "specializations": "youth,general,spirituality",
    "madhab": "Hanbali",
    "bio": "Imam specializing in youth engagement and mentoring for teenagers and young adults navigating Islamic identity.",
    "years_experience": 12,
    "qualifications": "Islamic Teacher Certification, Youth Ministry Training",
    "email": "imam.hassan@youth.com",
    "phone": "+1-555-0108",
    "website": "https://youthmosque.com",
    "consultation_methods": "phone,video,messaging",
    "consultation_fee": 40.0,
    "currency": "USD",
    "languages": "English,Arabic",
    "timezone": "CST",
    "is_available": true,
    "verified": false
  }'
```

---

### Example 4: Family Counselor Registration

**Request:**
```bash
curl -X POST http://localhost:8001/api/v1/imam/imams \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Dr. Fatima Al-Ansari",
    "title": "Dr.",
    "specializations": "family,women,general",
    "madhab": "Maliki",
    "bio": "Female Islamic counselor specializing in family dynamics, women'\''s issues, and marriage guidance.",
    "years_experience": 15,
    "qualifications": "Masters in Islamic Studies, Family Counseling Certificate",
    "email": "dr.fatima@familycare.com",
    "phone": "+1-555-0105",
    "website": "https://familyislam.com",
    "consultation_methods": "phone,video,email",
    "consultation_fee": 60.0,
    "currency": "USD",
    "languages": "English,Arabic,Urdu,French",
    "timezone": "EST",
    "is_available": true,
    "verified": false
  }'
```

---

### Example 5: Quran Expert Registration

**Request:**
```bash
curl -X POST http://localhost:8001/api/v1/imam/imams \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Dr. Ahmed Al-Khatib",
    "title": "Dr.",
    "specializations": "quran,hadith,tafsir",
    "madhab": "Shafi'i",
    "bio": "Quran and Hadith specialist with expertise in Tafsir (Quranic interpretation) and Islamic jurisprudence.",
    "years_experience": 25,
    "qualifications": "PhD Islamic Studies, Hafiz, Master of Tafsir",
    "email": "dr.ahmed@quranicstudies.com",
    "phone": "+1-555-0107",
    "website": "https://quranic-academy.com",
    "consultation_methods": "phone,video,in_person",
    "consultation_fee": 65.0,
    "currency": "USD",
    "languages": "English,Arabic,Turkish",
    "timezone": "GMT",
    "is_available": true,
    "verified": false
  }'
```

---

## Error Responses

### Duplicate Email (HTTP 400)

**Request:**
```bash
curl -X POST http://localhost:8001/api/v1/imam/imams \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Another Imam",
    "specializations": "general",
    "email": "imam@example.com",
    "consultation_methods": "phone",
    "languages": "English"
  }'
```

**Response:**
```json
{
  "detail": "Imam with email 'imam@example.com' already registered"
}
```

### Server Error (HTTP 500)

**Response:**
```json
{
  "detail": "Error registering imam: [error details]"
}
```

---

## Workflow After Registration

1. **Imam Registers** → POST /api/v1/imam/imams
2. **Appears in Directory** → GET /api/v1/imam/imams
3. **Accepts Bookings** → Users POST /api/v1/imam/consultations/book
4. **Manages Consultations** → PUT /api/v1/imam/consultations/{id}/confirm, /complete
5. **Gets Rated** → PUT /api/v1/imam/consultations/{id}/rate
6. **Rating Updates** → average_rating is updated automatically

---

## Integration Flow

**Step 1: Imam Registration**
```
POST /api/v1/imam/imams
↓
Imam profile created with ID
```

**Step 2: Verification**
```
GET /api/v1/imam/imams
↓
Imam appears in public directory
```

**Step 3: User Books Consultation**
```
POST /api/v1/imam/consultations/book
↓
Consultation created with status="pending"
```

**Step 4: Imam Confirms**
```
PUT /api/v1/imam/consultations/{id}/confirm
↓
Status changes to "confirmed"
```

**Step 5: Imam Completes & Provides Resolution**
```
PUT /api/v1/imam/consultations/{id}/complete
↓
Status changes to "completed"
```

**Step 6: User Rates**
```
PUT /api/v1/imam/consultations/{id}/rate
↓
Imam's average_rating is updated
```

---

## Quick Start

### Register Your First Imam

```bash
curl -X POST http://localhost:8001/api/v1/imam/imams \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Your Full Name",
    "specializations": "general,fiqh",
    "email": "your.email@example.com",
    "consultation_methods": "phone,video",
    "languages": "English,Arabic"
  }'
```

### Verify Registration

```bash
curl http://localhost:8001/api/v1/imam/imams
```

Your newly registered imam should appear in the list!

---

## Tips

- ✅ Use unique email addresses for each imam
- ✅ Comma-separate values for multi-choice fields (no spaces)
- ✅ Set competitive consultation fees
- ✅ Provide complete bio for better user trust
- ✅ Include phone/website for credibility
- ✅ Specify timezone for better scheduling
- ⚠️ The `verified` field can only be set by administrators
- ⚠️ New imams start with a 5.0 rating

---

## Example: Complete Registration Sequence

```bash
# 1. Register Imam 1
curl -X POST http://localhost:8001/api/v1/imam/imams \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Shaikh Abdullah",
    "specializations": "family,youth",
    "email": "abdullah@example.com",
    "consultation_methods": "phone,video",
    "languages": "English,Arabic"
  }'

# 2. Register Imam 2
curl -X POST http://localhost:8001/api/v1/imam/imams \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Dr. Karim Al-Rashid",
    "specializations": "business,fiqh",
    "email": "karim@example.com",
    "consultation_methods": "email,video",
    "languages": "English,Arabic,Malay"
  }'

# 3. List all imams (both should appear)
curl http://localhost:8001/api/v1/imam/imams

# 4. Get statistics on Imam 1
curl http://localhost:8001/api/v1/imam/imams/9

# 5. Filter by specialization
curl "http://localhost:8001/api/v1/imam/imams?specialization=family"
```

---

**Ready to register imams? Start with the Quick Start example above! 🚀**
