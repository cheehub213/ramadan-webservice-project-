# 🕌 Imam Management Guide

## For Administrators & Imam Account Managers

This guide covers how to manage imam profiles, handle consultations, and maintain the quality of the imam service.

---

## Admin Endpoints

### Adding New Imams

**Note:** The current system doesn't have a dedicated POST endpoint for admin to add imams. You'll need to add imams directly to the database using:

**Option 1: Direct Database Insert**
```python
from app.models.imam import Imam, ImamSpecialization
from app.database import SessionLocal

db = SessionLocal()
new_imam = Imam(
    name="Sheikh Ahmad Hassan",
    title="Shaikh",
    specializations="fiqh,quran,madhab",
    madhab="Shafi'i",
    bio="An Islamic scholar with 25 years of experience in Islamic jurisprudence...",
    years_experience=25,
    qualifications="Bachelor's in Islamic Studies from Umm Al-Qura University",
    email="sheikh.ahmad@example.com",
    phone="+1-555-0200",
    website="https://sheikh-ahmad.com",
    consultation_methods="phone,email,video",
    consultation_fee=60.0,
    currency="USD",
    is_available=True,
    languages="English,Arabic",
    timezone="PST",
    average_rating=0.0,
    total_consultations=0,
    total_reviews=0,
    verified=True
)
db.add(new_imam)
db.commit()
```

**Option 2: Create Admin Endpoint (Recommended)**

Add this to `app/routes/imam.py`:

```python
from fastapi import APIRouter, HTTPException, Depends
from app.schemas.imam import ImamCreate, ImamResponse
from app.models.imam import Imam
from app.database import get_db

@router.post("/admin/imams", response_model=ImamResponse, tags=["Admin"])
async def create_imam(imam_data: ImamCreate, db: Session = Depends(get_db)):
    """
    Admin endpoint to add new imam to the system.
    Requires admin authentication.
    """
    # Check if email already exists
    existing = db.query(Imam).filter(Imam.email == imam_data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Imam with this email already exists")
    
    new_imam = Imam(**imam_data.model_dump())
    db.add(new_imam)
    db.commit()
    db.refresh(new_imam)
    return new_imam

@router.put("/admin/imams/{imam_id}", response_model=ImamResponse, tags=["Admin"])
async def update_imam(imam_id: int, imam_data: ImamUpdate, db: Session = Depends(get_db)):
    """
    Admin endpoint to update imam profile.
    """
    imam = db.query(Imam).filter(Imam.id == imam_id).first()
    if not imam:
        raise HTTPException(status_code=404, detail="Imam not found")
    
    for key, value in imam_data.model_dump(exclude_unset=True).items():
        setattr(imam, key, value)
    
    db.commit()
    db.refresh(imam)
    return imam

@router.delete("/admin/imams/{imam_id}", tags=["Admin"])
async def delete_imam(imam_id: int, db: Session = Depends(get_db)):
    """
    Admin endpoint to delete imam profile.
    """
    imam = db.query(Imam).filter(Imam.id == imam_id).first()
    if not imam:
        raise HTTPException(status_code=404, detail="Imam not found")
    
    db.delete(imam)
    db.commit()
    return {"message": "Imam profile deleted successfully"}
```

---

## Imam Profile Fields Explained

### Basic Information
- **name**: Full name of the imam
- **title**: Academic/religious title (Dr., Shaikh, Mufti, Qadi, etc.)
- **email**: Primary contact email (must be unique)
- **phone**: Phone number with country code
- **website**: Personal website or profile page

### Expertise
- **specializations**: Areas of expertise (comma-separated)
  - `general` - General Islamic guidance
  - `fiqh` - Islamic jurisprudence
  - `quran` - Quranic interpretation
  - `hadith` - Hadith knowledge
  - `family` - Family/marriage counseling
  - `youth` - Youth guidance
  - `business` - Islamic business ethics
  - `spirituality` - Spiritual guidance
  - `madhab` - Specific madhab expertise

- **madhab**: Islamic school of thought
  - `Hanafi` - Hanafi school (largest following)
  - `Maliki` - Maliki school
  - `Shafi'i` - Shafi'i school
  - `Hanbali` - Hanbali school

### Credentials
- **years_experience**: Years of Islamic scholarship/practice
- **qualifications**: Educational background and certifications
- **verified**: Boolean - Is imam verified by platform?

### Availability
- **is_available**: Currently accepting new consultations?
- **consultation_methods**: How users can consult
  - `phone` - Phone call
  - `email` - Email correspondence
  - `video` - Video call
  - `in_person` - Face-to-face
  - `messaging` - Chat/messaging

- **consultation_fee**: Cost per consultation
- **currency**: Currency for fee (USD, EUR, GBP, SAR, etc.)
- **timezone**: Imam's timezone for scheduling
- **languages**: Languages spoken (comma-separated)

### Reputation
- **average_rating**: Auto-calculated from user reviews (0-5)
- **total_consultations**: Auto-calculated count
- **total_reviews**: Auto-calculated count

---

## Handling Consultations

### Consultation Workflow

```
1. USER BOOKS
   └─ Status: pending
   └─ Imam notified of new booking

2. IMAM REVIEWS
   └─ Checks user's concern
   └─ Verifies availability

3. IMAM CONFIRMS
   └─ Status: confirmed
   └─ Provides contact method and schedule
   └─ Sends contact information to user

4. DIRECT CONSULTATION
   └─ Phone/Email/Video communication
   └─ Imam provides guidance based on Islamic scholarship

5. IMAM COMPLETES
   └─ Status: completed
   └─ Documents resolution and guidance provided
   └─ Records imam notes

6. USER RATES
   └─ Rates imam 1-5 stars
   └─ Leaves written review
   └─ Feedback updates imam's average rating
```

### Responding to Consultations

#### Confirming a Booking
```bash
PUT /api/v1/imam/consultations/{consultation_id}/confirm

Request Body:
{
  "status": "confirmed",
  "actual_date": "2026-01-15T18:00:00",
  "imam_notes": "Confirmed. Please call on +1-555-0100 at 6 PM EST. Have your detailed situation ready for discussion."
}
```

**Best Practices:**
- Confirm within 24 hours
- Provide clear contact instructions
- Set reasonable expectations about consultation duration
- Mention any preparation needed

#### Completing a Consultation
```bash
PUT /api/v1/imam/consultations/{consultation_id}/complete

Request Body:
{
  "imam_notes": "Discussed user's marriage issues in detail, reviewed Islamic perspective on communication and financial management",
  "resolution": "Based on Shafi'i madhab and Islamic principles:\n\n1. Communication: Implement weekly family meetings to discuss concerns...\n\n2. Finances: Both spouses should have transparent conversations about household budget...\n\n3. Parenting: Find compromise that honors both cultural backgrounds while following Islamic principles...\n\nRecommended: Read Surah Al-Nisa verse 21 together, consider marriage counseling if issues persist."
}
```

**Best Practices:**
- Document specific guidance provided
- Reference Islamic sources when applicable
- Include actionable recommendations
- Be empathetic and culturally sensitive
- Offer follow-up availability

---

## Consultation Best Practices for Imams

### Before Consultation
✅ Review the user's description thoroughly
✅ Understand the context and their madhab preference
✅ Prepare relevant Islamic references
✅ Confirm scheduling details
✅ Have access to necessary resources (books, references)

### During Consultation
✅ Listen carefully without judgment
✅ Ask clarifying questions
✅ Explain Islamic principles clearly
✅ Be respectful and empathetic
✅ Provide practical, actionable advice
✅ Reference Quran and Hadith appropriately
✅ Acknowledge cultural context while prioritizing Islamic principles

### After Consultation
✅ Document the guidance provided
✅ Offer follow-up opportunities if needed
✅ Mark consultation as completed
✅ Encourage user to rate the consultation
✅ Maintain professional confidentiality

---

## Managing Ratings and Reviews

### How Ratings Work

- **Users** rate imams 1-5 stars after consultation
- **Platform** automatically calculates average rating
- **Display**: ImamListResponse shows average_rating and total_reviews
- **Filtering**: Users can filter imams by minimum rating

### Rating Distribution Example
```
⭐⭐⭐⭐⭐ (5 stars): 180 reviews
⭐⭐⭐⭐ (4 stars): 45 reviews
⭐⭐⭐ (3 stars): 12 reviews
⭐⭐ (2 stars): 5 reviews
⭐ (1 star): 3 reviews
```

### Responding to Low Ratings

If an imam receives low ratings:
1. Contact imam for feedback
2. Review specific complaints
3. Provide guidance for improvement
4. Monitor for patterns
5. Consider suspension if repeated issues
6. Always verify user reports before taking action

---

## Seasonal Availability

### Ramadan Considerations
- Many imams have increased consultation demands
- May need temporary unavailability markers
- Consider premium fees for consultation time

### Holiday Periods
- Set `is_available: false` during extended vacations
- Communicate availability changes in advance
- Resume consultations with clear restart date

**Example:**
```python
imam.is_available = False  # Ramadan consultation pause
imam.updated_at = datetime.now()
db.commit()
```

---

## Monitoring System Health

### Key Metrics to Track

```
Total Imams: 15
├─ Verified: 14
└─ Pending Verification: 1

Consultations (Last 30 days):
├─ Pending: 8
├─ Confirmed: 12
├─ Completed: 45
├─ Cancelled: 3
└─ Total: 68

Performance:
├─ Avg Confirmation Time: 8 hours
├─ Avg Rating: 4.8/5.0
├─ Consultation Completion Rate: 94%
└─ User Satisfaction: 96%
```

### Monitoring Queries

```python
from datetime import datetime, timedelta
from sqlalchemy import func

db = SessionLocal()

# Get consultations from last 30 days
last_30_days = datetime.now() - timedelta(days=30)
recent = db.query(Consultation).filter(
    Consultation.created_at >= last_30_days
).all()

# Get imam with highest rating
top_imam = db.query(Imam).order_by(
    Imam.average_rating.desc()
).first()

# Get uncompleted consultations
pending = db.query(Consultation).filter(
    Consultation.status.in_(["pending", "confirmed"])
).all()

# Calculate average confirmation time
# (Note: Would need actual_date and created_at comparison)
```

---

## Handling Issues

### User Complaints
1. Request detailed complaint
2. Review consultation records
3. Contact imam for response
4. Attempt mediation
5. Offer resolution (refund, re-consultation, etc.)

### Imam Performance Issues
1. Document specific incidents
2. Provide coaching/training
3. Monitor improvement
4. Escalate if needed
5. Consider removal from platform if unresolved

### Technical Issues
- Consultation not appearing in user's list
- Rating/review not updating
- Status not changing properly
- Contact support team

---

## Sample Imam Profiles

### Sample 1: General Islamic Scholar
```json
{
  "name": "Dr. Mohammad Ahmed",
  "title": "Mufti",
  "specializations": "general,fiqh",
  "madhab": "Hanafi",
  "bio": "Dr. Ahmad has over 20 years of Islamic knowledge and education.",
  "years_experience": 20,
  "qualifications": "Masters in Islamic Studies, Al-Azhar",
  "email": "dr.ahmad@example.com",
  "phone": "+1-555-0100",
  "consultation_methods": "phone,email,video",
  "consultation_fee": 50.0,
  "currency": "USD",
  "is_available": true,
  "languages": "English,Arabic",
  "timezone": "EST",
  "verified": true
}
```

### Sample 2: Family Counselor
```json
{
  "name": "Shaikh Abdullah Hassan",
  "title": "Shaikh",
  "specializations": "family,youth,spiritual",
  "madhab": "Maliki",
  "bio": "Specialized in family and youth counseling with Islamic principles.",
  "years_experience": 15,
  "qualifications": "Islamic Law degree, Islamic Counseling certification",
  "email": "shaikh.abdullah@example.com",
  "phone": "+44-20-7946-0958",
  "consultation_methods": "phone,email,video,messaging",
  "consultation_fee": 45.0,
  "currency": "GBP",
  "is_available": true,
  "languages": "English,Arabic,Urdu",
  "timezone": "GMT",
  "verified": true
}
```

### Sample 3: Business Ethics Expert
```json
{
  "name": "Dr. Karim Al-Rashid",
  "title": "Dr.",
  "specializations": "business,fiqh,madhab",
  "madhab": "Shafi'i",
  "bio": "Expert in Islamic business ethics and halal compliance.",
  "years_experience": 18,
  "qualifications": "PhD in Islamic Finance, CPA",
  "email": "dr.karim@example.com",
  "phone": "+966-11-4654-3210",
  "consultation_methods": "phone,email,video",
  "consultation_fee": 75.0,
  "currency": "SAR",
  "is_available": true,
  "languages": "English,Arabic",
  "timezone": "AST",
  "verified": true
}
```

---

## Database Maintenance

### Backup Important Data
```bash
# SQLite backup
cp ramadan.db ramadan.db.backup
```

### Monitoring Database Size
```python
import os
db_size = os.path.getsize('ramadan.db') / 1024 / 1024  # MB
print(f"Database size: {db_size:.2f} MB")
```

### Cleaning Up Old Data
```python
from datetime import datetime, timedelta

# Archive old completed consultations (older than 1 year)
old_date = datetime.now() - timedelta(days=365)
old_consultations = db.query(Consultation).filter(
    Consultation.status == "completed",
    Consultation.completed_at < old_date
).all()

# Export for archive before deleting
# ... then delete
```

---

## Privacy and Security

### Protecting User Data
✅ Encrypt sensitive information (phone, email)
✅ Don't share user details without permission
✅ Limit imam access to their own consultations
✅ Use secure communication methods
✅ Regular security audits

### Imam Confidentiality
✅ Protect imam contact information
✅ Only share with booked users
✅ Don't expose imam ratings without consent
✅ Secure imam availability data

---

## Future Admin Features to Implement

- [ ] Comprehensive admin dashboard
- [ ] Bulk imam import/export
- [ ] Consultation analytics
- [ ] User and imam account management
- [ ] Billing and payment processing
- [ ] Verification workflow for new imams
- [ ] Automated notifications
- [ ] Scheduling assistant for imams
- [ ] Multi-language support for responses
- [ ] Integration with calendar systems (Google, Outlook)

---

**Maintaining excellence in Islamic guidance through quality imam management! 📚**
