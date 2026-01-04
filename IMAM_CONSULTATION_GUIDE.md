# 🕌 Imam Consultation Feature Guide

## Overview

The Imam Consultation feature allows users to book direct consultations with verified Islamic scholars (Imams) when they need more personalized guidance or when the Deepseek AI response is insufficient or confusing. This bridges the gap between AI-generated answers and authentic Islamic scholarship.

---

## Use Cases

### When to Use Imam Consultation

1. **Deepseek Response is Confusing**
   - User receives a response from the AI but finds it unclear or too general
   - Needs clarification or more detailed explanation

2. **Madhab-Specific Guidance**
   - User follows a specific Islamic school (Hanafi, Maliki, Shafi'i, Hanbali)
   - Deepseek response differs from their madhab's position
   - Needs madhab-specific fatwa or guidance

3. **Complex Personal Situations**
   - Family issues requiring nuanced understanding
   - Business/financial decisions with ethical implications
   - Spiritual/psychological concerns
   - Situations requiring cultural sensitivity

4. **Expert Validation**
   - User wants guidance from a verified Islamic scholar
   - Wants second opinion from a qualified Imam
   - Needs official Islamic ruling (Fatwa)

5. **Real-Time Discussion**
   - Issue requires back-and-forth dialogue
   - User needs to provide more context
   - Wants to ask follow-up questions

---

## Feature Architecture

### Components

```
┌─────────────────┐
│  User Searches  │
│    Question     │
└────────┬────────┘
         │
         v
┌─────────────────────────────────┐
│   Deepseek AI Provides Answer    │
└────────┬────────────────────────┘
         │
    ┌────────────────────┐
    │   User Decision    │
    ├────────────────────┤
    │ Satisfied?         │
    │ ├─ YES → Use answer│
    │ └─ NO → Continue  │
    └────────┬───────────┘
             │
             v
┌────────────────────────────────────┐
│   Browse Available Imams            │
│   • Filter by specialization        │
│   • Filter by madhab                │
│   • Check ratings & availability    │
└────────┬───────────────────────────┘
         │
         v
┌────────────────────────────────────┐
│   Book Consultation with Imam       │
│   • Choose consultation method      │
│   • Provide detailed description    │
│   • Include Deepseek response       │
│   • Set preferred date/time         │
└────────┬───────────────────────────┘
         │
         v
┌────────────────────────────────────┐
│   Imam Confirmation                 │
│   • Imam reviews request            │
│   • Confirms availability           │
│   • Provides contact details        │
└────────┬───────────────────────────┘
         │
         v
┌────────────────────────────────────┐
│   Direct Consultation               │
│   • Phone / Email / Video / Chat    │
│   • Personalized guidance           │
│   • Madhab-specific advice          │
└────────┬───────────────────────────┘
         │
         v
┌────────────────────────────────────┐
│   Rate & Review                     │
│   • Rating (1-5 stars)              │
│   • Written review                  │
│   • Feedback updates imam rating    │
└────────────────────────────────────┘
```

---

## API Endpoints

### 1. List Available Imams

**Endpoint:** `GET /api/v1/imam/imams`

**Parameters:**
```
specialization: Filter by expertise (optional)
  - general: General Islamic guidance
  - fiqh: Islamic jurisprudence
  - quran: Quranic interpretation (Tafsir)
  - hadith: Hadith knowledge
  - family: Family and marriage issues
  - youth: Youth counseling
  - business: Islamic business ethics
  - spirituality: Spiritual guidance
  - madhab: Specific madhab expert

madhab: Filter by Islamic school (optional)
  - Hanafi
  - Maliki
  - Shafi'i
  - Hanbali

available_only: Show only available imams (default: true)
min_rating: Minimum rating filter 0.0-5.0 (default: 0.0)
```

**Example Request:**
```bash
GET /api/v1/imam/imams?specialization=family&madhab=Hanafi&min_rating=4.5&available_only=true
```

**Example Response:**
```json
[
  {
    "id": 1,
    "name": "Dr. Mohammad Ahmed",
    "title": "Mufti",
    "specializations": "family,fiqh,madhab",
    "madhab": "Hanafi",
    "bio": "20 years of Islamic knowledge...",
    "consultation_methods": "phone,email,video",
    "consultation_fee": 50.0,
    "is_available": true,
    "languages": "English,Arabic,Urdu",
    "average_rating": 4.9,
    "total_consultations": 247,
    "verified": true
  }
]
```

### 2. Get Imam Details

**Endpoint:** `GET /api/v1/imam/imams/{imam_id}`

**Parameters:**
```
imam_id: ID of the imam (required)
```

**Example Response:**
```json
{
  "id": 1,
  "name": "Dr. Mohammad Ahmed",
  "title": "Mufti",
  "specializations": "family,fiqh,madhab",
  "madhab": "Hanafi",
  "bio": "Dr. Mohammad Ahmed is...",
  "years_experience": 20,
  "qualifications": "Bachelor's in Islamic Studies, Al-Azhar University; Master's in Fiqh...",
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

### 3. Get Imams by Specialization

**Endpoint:** `GET /api/v1/imam/imams/by-specialization/{specialization}`

**Example Request:**
```bash
GET /api/v1/imam/imams/by-specialization/family
```

**Returns:** List of imams specializing in family issues

### 4. Book a Consultation

**Endpoint:** `POST /api/v1/imam/consultations/book`

**Request Body:**
```json
{
  "imam_id": 1,
  "title": "Marriage and Family Issues",
  "description": "I'm struggling with communication in my marriage. We have different approaches to parenting and managing household finances. This is causing tension...",
  "category": "family",
  "madhab_preference": "Hanafi",
  "user_email": "user@example.com",
  "preferred_method": "phone",
  "preferred_date": "2026-01-15T18:00:00",
  "duration_minutes": 45,
  "original_prompt": "I have marriage problems",
  "deepseek_response": "Based on Islamic teachings, communication and understanding are key...",
  "reason_for_consultation": "The AI response was too general. I need specific guidance based on Hanafi madhab for my cultural context."
}
```

**Response:**
```json
{
  "id": 1,
  "imam_id": 1,
  "title": "Marriage and Family Issues",
  "description": "I'm struggling with communication...",
  "category": "family",
  "madhab_preference": "Hanafi",
  "preferred_method": "phone",
  "preferred_date": "2026-01-15T18:00:00",
  "status": "pending",
  "rating": null,
  "review": null,
  "created_at": "2026-01-01T10:00:00",
  "updated_at": "2026-01-01T10:00:00"
}
```

**Status Codes:**
- 200: Consultation booked successfully
- 404: Imam not found
- 400: Imam not available or invalid input
- 500: Server error

### 5. Get Consultation Details

**Endpoint:** `GET /api/v1/imam/consultations/{consultation_id}`

**Parameters:**
```
consultation_id: ID of the consultation (required)
```

**Response includes:**
- Full consultation details
- Imam notes and resolution
- Original prompt and Deepseek response
- Status and scheduling information

### 6. Get User's Consultations

**Endpoint:** `GET /api/v1/imam/consultations/user/{user_email}`

**Parameters:**
```
user_email: User's email address (required)
```

**Returns:** List of all consultations for the user (past and pending)

### 7. Confirm Consultation (Imam)

**Endpoint:** `PUT /api/v1/imam/consultations/{consultation_id}/confirm`

**Request Body:**
```json
{
  "status": "confirmed",
  "actual_date": "2026-01-15T18:00:00",
  "imam_notes": "Confirmed. Please call on: +1-555-0100 at scheduled time. Have your questions ready."
}
```

### 8. Complete Consultation (Imam)

**Endpoint:** `PUT /api/v1/imam/consultations/{consultation_id}/complete`

**Request Body:**
```json
{
  "imam_notes": "Discussed your family situation in detail",
  "resolution": "Based on Islamic principles and Hanafi madhab, here's my guidance:\n1. Improve communication through scheduled family meetings...\n2. Regarding finances: In Islam, both spouses should have transparent discussions...\n3. Parenting approach: Try to find middle ground honoring both cultural backgrounds..."
}
```

### 9. Rate Consultation

**Endpoint:** `PUT /api/v1/imam/consultations/{consultation_id}/rate`

**Request Body:**
```json
{
  "rating": 5,
  "review": "Excellent guidance! The imam understood my situation perfectly and provided practical Islamic solutions based on my madhab. Highly recommended!"
}
```

### 10. Cancel Consultation

**Endpoint:** `PUT /api/v1/imam/consultations/{consultation_id}/cancel`

**Note:** Can only cancel pending or confirmed consultations, not completed ones

---

## Workflow Example

### Step 1: User Searches for Guidance
```bash
POST /api/v1/search/answer
{
  "prompt": "I'm having marriage problems",
  "response_language": "bilingual"
}
```

### Step 2: Deepseek Provides Answer
```json
{
  "results": {
    "quran_verses": [...],
    "hadiths": [...]
  },
  "explanations": "General Islamic guidance on marriage..."
}
```

### Step 3: User Not Satisfied
User realizes the answer is too general and needs specific madhab guidance

### Step 4: Browse Imams
```bash
GET /api/v1/imam/imams?specialization=family&madhab=Hanafi&min_rating=4.5
```

### Step 5: Book Consultation
```bash
POST /api/v1/imam/consultations/book
{
  "imam_id": 1,
  "title": "Marriage Problems",
  "description": "Specific details about my marriage issue...",
  "user_email": "user@example.com",
  "reason_for_consultation": "The AI answer was too general, doesn't address my Hanafi madhab perspective"
}
```

### Step 6: Imam Confirms
```bash
PUT /api/v1/imam/consultations/1/confirm
{
  "status": "confirmed",
  "actual_date": "2026-01-15T18:00:00",
  "imam_notes": "Ready to discuss. Call at +1-555-0100"
}
```

### Step 7: Direct Consultation Happens
User and Imam discuss via phone/email/video

### Step 8: Imam Completes
```bash
PUT /api/v1/imam/consultations/1/complete
{
  "resolution": "Based on Hanafi madhab and your situation, here's my guidance..."
}
```

### Step 9: User Rates
```bash
PUT /api/v1/imam/consultations/1/rate
{
  "rating": 5,
  "review": "Excellent and personalized guidance!"
}
```

---

## Data Models

### Imam Model
- **id**: Unique identifier
- **name**: Imam's full name
- **title**: Title (Dr., Mufti, etc.)
- **specializations**: Comma-separated areas of expertise
- **madhab**: Islamic school (Hanafi, Maliki, Shafi'i, Hanbali)
- **bio**: Background and qualifications
- **years_experience**: Years of Islamic knowledge
- **email**: Contact email (unique)
- **phone**: Phone number
- **consultation_methods**: Available methods (phone, email, video, in_person, messaging)
- **consultation_fee**: Fee per consultation
- **is_available**: Currently accepting bookings
- **languages**: Spoken languages
- **timezone**: Imam's timezone
- **average_rating**: Average rating (0-5 stars)
- **total_consultations**: Number of completed consultations
- **verified**: Is imam verified by platform

### Consultation Model
- **id**: Unique identifier
- **imam_id**: Reference to Imam
- **user_id**: User's email
- **title**: Brief title of concern
- **description**: Detailed description
- **category**: Category of issue
- **madhab_preference**: User's madhab preference
- **original_prompt**: User's original question
- **deepseek_response**: AI response that was insufficient
- **reason_for_consultation**: Why seeking imam
- **preferred_method**: Preferred consultation method
- **preferred_date**: Preferred date/time
- **actual_date**: Actual consultation date/time
- **status**: pending, confirmed, completed, cancelled, rescheduled
- **imam_notes**: Imam's notes and guidance
- **resolution**: Final guidance provided
- **rating**: User's rating (1-5)
- **review**: User's written review
- **created_at**: Booking creation time
- **completed_at**: Consultation completion time

---

## Consultation Statuses

1. **pending** - Waiting for imam confirmation
2. **confirmed** - Imam confirmed, scheduled for consultation
3. **completed** - Consultation finished
4. **cancelled** - User or imam cancelled
5. **rescheduled** - Rescheduled for different time

---

## Consultation Methods

- **phone**: Phone call consultation
- **email**: Email-based correspondence
- **video**: Video call (Zoom, Google Meet, etc.)
- **in_person**: Face-to-face meeting
- **messaging**: Chat/messaging service

---

## Best Practices

### For Users

1. **Provide Context**: Include the Deepseek response and why you found it insufficient
2. **Specify Madhab**: If you follow a specific madhab, mention it
3. **Be Clear**: Describe your situation in detail
4. **Choose Specialization**: Select an imam specializing in your issue area
5. **Set Expectations**: Be clear about what you're seeking (fatwa, advice, clarification)
6. **Rate After**: Leave honest ratings to help others

### For Imams

1. **Confirm Promptly**: Respond quickly to booking requests
2. **Provide Contact Info**: Give clear instructions on how to connect
3. **Document Resolution**: Record the guidance provided
4. **Be Professional**: Maintain Islamic and professional standards
5. **Follow Up**: Check if user is satisfied

---

## Integration with Search Flow

The Imam Consultation feature integrates seamlessly with the Quran/Hadith search:

```
User Question
    ↓
Deepseek AI Analysis
    ↓
Quran Verses + Hadiths + Explanations
    ↓
User Satisfied?
    ├─ YES → Done
    └─ NO → Consult Imam
            ├─ Browse Imams
            ├─ Book Consultation
            ├─ Direct Communication
            └─ Personalized Resolution
```

---

## Benefits

✅ **Personalized Guidance** - Tailored to user's specific situation
✅ **Madhab-Specific** - Guidance based on user's Islamic school
✅ **Expert Validation** - Responses from verified Islamic scholars
✅ **Two-Way Dialogue** - Back-and-forth discussion possible
✅ **Cultural Sensitivity** - Understanding of user's context
✅ **Trust Building** - Direct relationship with scholar
✅ **Quality Assurance** - Ratings ensure quality service
✅ **Comprehensive Solution** - Combines AI + expert guidance

---

## Future Enhancements

- Group consultations (Halaqah/classes)
- Scheduled workshops on Islamic topics
- Referrals between imams
- Imam directory with verified credentials
- Payment processing integration
- Video conferencing integration
- Consultation history and follow-ups
- Multi-language support with translation
- Specialized consultation packages

---

## Support

For issues with Imam Consultations, please:
1. Check consultation status
2. Contact the Imam directly using provided contact info
3. Report any issues through the platform

---

**Bringing together Quranic wisdom and expert Islamic scholarship! 🕌**
