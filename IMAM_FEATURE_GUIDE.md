# 🕌 Imam Consultation System - Implementation Guide

## Quick Start

The Imam Consultation feature is now fully implemented and ready to use. Here's how to get started:

### 1. Initialize the Database

First, restart your FastAPI server to create the new database tables:

```bash
# From the project root directory
python -m uvicorn app.main:app --host localhost --port 8001 --reload
```

This will automatically create the `imam` and `consultation` tables in your SQLite database.

### 2. Populate Sample Data

Run the population script to add sample imams and consultations:

```bash
python scripts/populate_sample_imams.py
```

**Output:**
```
============================================================
🕌 RAMADAN SERVICE - SAMPLE DATA POPULATION
============================================================

📚 Populating sample imam data...
────────────────────────────────────────────────────────────
✅ Created: Dr. Mohammad Ahmed Hassan (Hanafi) - ID: 1
✅ Created: Shaikh Abdullah Hassan Al-Rashid (Maliki) - ID: 2
✅ Created: Dr. Karim Al-Rashid Muhammad (Shafi'i) - ID: 3
✅ Created: Imam Muhammad Samir (Hanbali) - ID: 4
✅ Created: Dr. Fatima Al-Ansari (Maliki) - ID: 5
✅ Created: Shaikh Ibrahim Hassan (Hanafi) - ID: 6
✅ Created: Dr. Ahmed Al-Khatib (Shafi'i) - ID: 7
✅ Created: Imam Hassan Al-Turki (Hanbali) - ID: 8
────────────────────────────────────────────────────────────

📊 Summary:
   ✅ Created: 8
   ⏭️  Skipped: 0
   📦 Total: 8

📅 Populating sample consultation data...
────────────────────────────────────────────────────────────
✅ Created: Marriage Communication Issues - ID: 1
✅ Created: Youth Islamic Identity - ID: 2
✅ Created: Business Partnership Ethics - ID: 3
────────────────────────────────────────────────────────────

📊 Consultations Summary:
   ✅ Created: 3
   ⏭️  Skipped: 0
   📦 Total: 3

============================================================
✅ Sample data population complete!
============================================================
```

### 3. Test via Swagger UI

Visit: `http://localhost:8001/docs`

You'll see a new section for Imam endpoints:
- `GET /api/v1/imam/imams` - List imams
- `GET /api/v1/imam/imams/{imam_id}` - Get imam details
- `POST /api/v1/imam/consultations/book` - Book consultation
- And more...

---

## What Was Implemented

### 📁 New Files Created

1. **`app/models/imam.py`** (150 lines)
   - `Imam` model: Profiles of Islamic scholars
   - `Consultation` model: Booking and consultation records
   - `ImamSpecialization` enum: Areas of expertise
   - `ConsultationStatus` enum: Consultation lifecycle states

2. **`app/schemas/imam.py`** (200 lines)
   - 12 validation schemas for requests/responses
   - 3 enums for API parameters
   - Input validation with Pydantic

3. **`app/routes/imam.py`** (400 lines)
   - 10 API endpoints for imam management
   - Consultation booking workflow
   - Status management and ratings system
   - Error handling and validation

4. **`scripts/populate_sample_imams.py`** (250 lines)
   - Automatic sample data creation
   - 8 diverse imam profiles
   - 3 sample consultations
   - Idempotent (safe to run multiple times)

### 📝 Updated Files

**`app/main.py`**
- Added: `from app.routes import search, health, imam`
- Added: `app.include_router(imam.router)`
- Updated version: 1.0.0 → 2.0.0
- Updated description: Added "Real Imams" mention

### 📚 Documentation Files Created

1. **`IMAM_CONSULTATION_GUIDE.md`** (400 lines)
   - User guide for booking imams
   - Complete API endpoint documentation
   - Workflow examples
   - Data models explained
   - Integration patterns

2. **`IMAM_MANAGEMENT_GUIDE.md`** (350 lines)
   - Admin guide for managing imams
   - How to add/update imam profiles
   - Handling consultations
   - Monitoring system health
   - Best practices

3. **`API_REFERENCE_COMPLETE.md`** (300 lines)
   - Complete API reference
   - All endpoints documented
   - Request/response formats
   - Error codes and solutions
   - Integration examples

4. **`scripts/populate_sample_imams.py`** (documentation included)
   - Comments explaining each section
   - Sample data structure
   - Usage instructions

---

## API Endpoints

### Available Endpoints

```
Imam Management:
├── GET    /api/v1/imam/imams
├── GET    /api/v1/imam/imams/{imam_id}
└── GET    /api/v1/imam/imams/by-specialization/{specialization}

Consultation Booking:
├── POST   /api/v1/imam/consultations/book
├── GET    /api/v1/imam/consultations/{consultation_id}
└── GET    /api/v1/imam/consultations/user/{user_email}

Consultation Management:
├── PUT    /api/v1/imam/consultations/{consultation_id}/confirm
├── PUT    /api/v1/imam/consultations/{consultation_id}/complete
├── PUT    /api/v1/imam/consultations/{consultation_id}/rate
└── PUT    /api/v1/imam/consultations/{consultation_id}/cancel
```

### Example Usage

**List all family counselors with high ratings:**
```bash
GET /api/v1/imam/imams?specialization=family&min_rating=4.5&available_only=true
```

**Book a consultation:**
```bash
POST /api/v1/imam/consultations/book
{
  "imam_id": 1,
  "title": "Marriage Issues",
  "description": "...",
  "category": "family",
  "user_email": "user@example.com",
  "preferred_method": "phone",
  "preferred_date": "2026-01-15T18:00:00"
}
```

**Rate a consultation:**
```bash
PUT /api/v1/imam/consultations/1/rate
{
  "rating": 5,
  "review": "Excellent guidance!"
}
```

---

## Sample Imams Included

The population script creates 8 diverse imams:

| Imam | Specialization | Madhab | Fee |
|------|---|---|---|
| Dr. Mohammad Ahmed Hassan | General, Fiqh, Madhab | Hanafi | $50 |
| Shaikh Abdullah Hassan | Family, Youth, Spirituality | Maliki | £45 |
| Dr. Karim Al-Rashid | Business, Fiqh, Madhab | Shafi'i | 75 SAR |
| Imam Muhammad Samir | Quran, Hadith, Spirituality | Hanbali | 40 SAR |
| Dr. Fatima Al-Ansari | Family, Youth, Spirituality | Maliki | $55 |
| Shaikh Ibrahim Hassan | General, Fiqh, Youth | Hanafi | $35 |
| Dr. Ahmed Al-Khatib | Quran, Fiqh, Madhab | Shafi'i | 65 EGP |
| Imam Hassan Al-Turki | General, Spirituality | Hanbali | 45 AED |

---

## Database Schema

### Imam Table
```sql
CREATE TABLE imam (
    id INTEGER PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    title VARCHAR(100),
    specializations VARCHAR(255),
    madhab VARCHAR(50),
    bio TEXT,
    years_experience INTEGER,
    qualifications TEXT,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(20),
    website VARCHAR(255),
    consultation_methods VARCHAR(255),
    consultation_fee FLOAT,
    currency VARCHAR(10),
    is_available BOOLEAN DEFAULT true,
    languages VARCHAR(255),
    timezone VARCHAR(50),
    average_rating FLOAT DEFAULT 0.0,
    total_consultations INTEGER DEFAULT 0,
    total_reviews INTEGER DEFAULT 0,
    verified BOOLEAN DEFAULT false,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
```

### Consultation Table
```sql
CREATE TABLE consultation (
    id INTEGER PRIMARY KEY,
    imam_id INTEGER NOT NULL,
    user_id VARCHAR(255),
    title VARCHAR(255) NOT NULL,
    description TEXT,
    category VARCHAR(50),
    madhab_preference VARCHAR(50),
    original_prompt TEXT,
    deepseek_response TEXT,
    reason_for_consultation TEXT,
    preferred_method VARCHAR(50),
    preferred_date TIMESTAMP,
    actual_date TIMESTAMP,
    duration_minutes INTEGER,
    status VARCHAR(50) DEFAULT 'pending',
    imam_notes TEXT,
    resolution TEXT,
    rating INTEGER,
    review TEXT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    FOREIGN KEY(imam_id) REFERENCES imam(id)
);
```

---

## Features

### ✨ Key Features

1. **Imam Profiles**
   - Detailed background and qualifications
   - Specializations (general, fiqh, quran, family, business, etc.)
   - Islamic school (madhab) expertise
   - Consultation fees and methods
   - Languages spoken and timezone

2. **Filtering & Search**
   - Filter by specialization
   - Filter by madhab (Hanafi, Maliki, Shafi'i, Hanbali)
   - Filter by availability
   - Filter by minimum rating
   - Search by language

3. **Booking System**
   - Easy consultation booking
   - Multiple consultation methods (phone, email, video, in-person)
   - Preferred date/time scheduling
   - Include context (original prompt, why AI was insufficient)

4. **Consultation Lifecycle**
   - Pending → Confirmed → Completed → Rated
   - Imam can confirm, complete, and manage consultations
   - Users can rate and review
   - Ratings automatically update imam profile

5. **Quality Assurance**
   - 1-5 star rating system
   - Written reviews from users
   - Total consultation count
   - Verification badge for trusted imams

---

## Workflow Example

### User Journey

```
1. User searches for Islamic guidance
   └─ POST /api/v1/search/answer

2. Deepseek provides answer
   └─ User reads response

3. User decides to consult imam
   └─ Reason: "Too general" or "Doesn't match my madhab"

4. User browses imams
   └─ GET /api/v1/imam/imams?specialization=family&madhab=Hanafi

5. User selects an imam
   └─ GET /api/v1/imam/imams/1

6. User books consultation
   └─ POST /api/v1/imam/consultations/book

7. Imam confirms booking
   └─ PUT /api/v1/imam/consultations/1/confirm

8. Direct communication happens
   └─ Phone/Email/Video consultation

9. Imam provides resolution
   └─ PUT /api/v1/imam/consultations/1/complete

10. User rates imam
    └─ PUT /api/v1/imam/consultations/1/rate

11. Rating updates imam's profile
    └─ Affects future filtering and visibility
```

---

## Testing

### Via Swagger UI

1. Open `http://localhost:8001/docs`
2. Expand the "Imam" section
3. Try the endpoints:
   - GET `/api/v1/imam/imams` - See all imams
   - GET `/api/v1/imam/imams/1` - Get imam details
   - POST `/api/v1/imam/consultations/book` - Book consultation

### Via cURL

**List imams:**
```bash
curl http://localhost:8001/api/v1/imam/imams
```

**Get specific imam:**
```bash
curl http://localhost:8001/api/v1/imam/imams/1
```

**Book consultation:**
```bash
curl -X POST http://localhost:8001/api/v1/imam/consultations/book \
  -H "Content-Type: application/json" \
  -d '{
    "imam_id": 1,
    "title": "Marriage Issues",
    "description": "We are having communication problems...",
    "category": "family",
    "user_email": "user@example.com",
    "preferred_method": "phone",
    "preferred_date": "2026-01-15T18:00:00"
  }'
```

---

## Integration with Existing Features

### With Search Endpoint

When a user gets an answer from `/api/v1/search/answer`, they can:

1. Accept the answer ✅
2. Request clarification from an imam 🕌

**Suggested Enhancement:**
Add response field to indicate imam consultation option:

```json
{
  "quran_verses": [...],
  "hadiths": [...],
  "can_consult_imam": true,
  "relevant_imam_specializations": ["family", "fiqh"]
}
```

Then guide user to:
```bash
GET /api/v1/imam/imams?specialization=family
```

---

## Future Enhancements

### Short Term (v2.1)
- [ ] Admin endpoints for managing imams
- [ ] Email notifications for consultation status changes
- [ ] Imam dashboard showing pending consultations
- [ ] Integration suggestion from search to imam booking

### Medium Term (v2.2)
- [ ] Video conferencing integration
- [ ] Payment processing for consultation fees
- [ ] Rescheduling consultations
- [ ] Follow-up consultations

### Long Term (v2.3)
- [ ] Group consultations (Halaqah/classes)
- [ ] Referrals between imams
- [ ] Islamic knowledge marketplace
- [ ] Certification/credential verification system
- [ ] Multi-language support for all responses

---

## Configuration

### Environment Variables (if needed)

Currently, no additional environment variables are needed. All configuration is in the database.

### Database

Uses existing SQLite database (`ramadan.db`). New tables (`imam`, `consultation`) are created automatically.

---

## Troubleshooting

### Tables Not Created

If imam/consultation tables aren't created:
1. Ensure `Base.metadata.create_all(engine)` is called in `app/database.py`
2. Restart the API server

### Sample Data Not Populated

If sample imams aren't showing:
```bash
python scripts/populate_sample_imams.py
```

### Imam Email Conflict

If you get "Email already exists" error:
- Use unique email addresses when adding imams
- Or clear the imam table and repopulate

---

## Support Resources

📖 **Guides:**
- [Imam Consultation User Guide](IMAM_CONSULTATION_GUIDE.md)
- [Imam Management Guide](IMAM_MANAGEMENT_GUIDE.md)
- [Complete API Reference](API_REFERENCE_COMPLETE.md)

🧪 **Testing:**
- Try endpoints in Swagger UI: `/docs`
- Use sample imams (IDs 1-8)
- Use sample consultations for reference

❓ **Questions:**
- Check the documentation files
- Review code comments
- Test via Swagger UI

---

## Summary

✅ **What's Working:**
- 10 fully functional API endpoints
- 8 sample imams with diverse specializations
- 3 sample consultations for reference
- Complete filtering and search capabilities
- Consultation lifecycle management
- Rating and review system
- Bilingual support (inherits from search feature)

🚀 **Ready to Use:**
1. Restart API server
2. Run population script
3. Test via Swagger UI
4. Integrate with your UI

💡 **Next Steps:**
1. Add integration layer to suggest imams in search results
2. Create user dashboard for managing consultations
3. Add notification system for status updates
4. Implement payment processing
5. Build imam management dashboard

---

**Building a bridge between AI-powered guidance and Islamic scholarship! 🕌**

*Last Updated: January 2026*
*Version: 2.0.0*
