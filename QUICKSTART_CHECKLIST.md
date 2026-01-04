# ✅ Imam Consultation Feature - Quick Start Checklist

## 🚀 Get Started in 5 Minutes

Use this checklist to get the Imam Consultation system up and running.

---

## Step 1: Restart API Server (1 minute)

### Command
```bash
python -m uvicorn app.main:app --host localhost --port 8001 --reload
```

### What Happens
- ✅ Creates `imam` table with 8 fields
- ✅ Creates `consultation` table with 17 fields
- ✅ Database ready for data

### Expected Output
```
INFO:     Uvicorn running on http://127.0.0.1:8001
INFO:     Application startup complete
```

---

## Step 2: Populate Sample Data (1 minute)

### Command
```bash
python scripts/populate_sample_imams.py
```

### What Happens
- ✅ Creates 8 sample imams
- ✅ Creates 3 sample consultations
- ✅ Ready for testing

### Expected Output
```
✅ Created: Dr. Mohammad Ahmed Hassan (Hanafi) - ID: 1
✅ Created: Shaikh Abdullah Hassan Al-Rashid (Maliki) - ID: 2
... (6 more imams)
✅ Created: Marriage Communication Issues - ID: 1
✅ Created: Youth Islamic Identity - ID: 2
✅ Created: Business Partnership Ethics - ID: 3
```

---

## Step 3: Test via Swagger UI (3 minutes)

### URL
```
http://localhost:8001/docs
```

### Quick Tests

#### Test 1: List All Imams
```
1. Click "GET /api/v1/imam/imams"
2. Click "Try it out"
3. Click "Execute"
4. ✅ Should see 8 imams returned
```

#### Test 2: Filter by Specialization
```
1. Click "GET /api/v1/imam/imams"
2. Click "Try it out"
3. Enter specialization: "family"
4. Click "Execute"
5. ✅ Should see 3-4 imams with family specialization
```

#### Test 3: Get Imam Details
```
1. Click "GET /api/v1/imam/imams/{imam_id}"
2. Click "Try it out"
3. Enter imam_id: "1"
4. Click "Execute"
5. ✅ Should see Dr. Mohammad Ahmed Hassan's full profile
```

#### Test 4: Book a Consultation
```
1. Click "POST /api/v1/imam/consultations/book"
2. Click "Try it out"
3. Copy-paste this request body:
{
  "imam_id": 1,
  "title": "Test Marriage Issue",
  "description": "Testing the consultation booking system",
  "category": "family",
  "madhab_preference": "Hanafi",
  "user_email": "test@example.com",
  "preferred_method": "phone",
  "preferred_date": "2026-02-01T18:00:00"
}
4. Click "Execute"
5. ✅ Should get back consultation with ID and status "pending"
```

#### Test 5: Rate a Consultation
```
1. Note the consultation ID from Test 4 (e.g., ID: 4)
2. Click "PUT /api/v1/imam/consultations/{consultation_id}/rate"
3. Click "Try it out"
4. Enter consultation_id: "4"
5. Enter request body:
{
  "rating": 5,
  "review": "Great system!"
}
6. Click "Execute"
7. ✅ Should see consultation with rating updated
```

---

## ✅ Validation Checklist

### Database
- [ ] `imam` table exists with 8 records
- [ ] `consultation` table exists with 3 records
- [ ] Can query both tables without errors

### API Endpoints
- [ ] GET `/api/v1/imam/imams` works
- [ ] GET `/api/v1/imam/imams/1` works
- [ ] GET `/api/v1/imam/imams/by-specialization/family` works
- [ ] POST `/api/v1/imam/consultations/book` works
- [ ] GET `/api/v1/imam/consultations/{id}` works
- [ ] PUT `/api/v1/imam/consultations/{id}/confirm` works
- [ ] PUT `/api/v1/imam/consultations/{id}/complete` works
- [ ] PUT `/api/v1/imam/consultations/{id}/rate` works

### Filtering
- [ ] Can filter imams by specialization
- [ ] Can filter imams by madhab
- [ ] Can filter imams by min_rating
- [ ] Can filter imams by available_only

### Data Integrity
- [ ] Sample imams display correctly
- [ ] Sample consultations display correctly
- [ ] Ratings update imam's average_rating
- [ ] Consultation status changes properly

---

## 🎯 Next Steps

### Immediate (Do Now)
- [ ] Complete Steps 1-3 above
- [ ] Run all validation checks
- [ ] Bookmark documentation files

### Short Term (Today)
- [ ] Read [Imam Consultation Guide](IMAM_CONSULTATION_GUIDE.md)
- [ ] Read [API Reference](API_REFERENCE_COMPLETE.md)
- [ ] Test all 10 endpoints via Swagger

### Medium Term (This Week)
- [ ] Integrate with your frontend
- [ ] Build imam listing UI
- [ ] Build consultation booking form
- [ ] Add notification system

### Long Term (This Month)
- [ ] Add admin imam management
- [ ] Implement payment processing
- [ ] Create imam dashboard
- [ ] Deploy to production

---

## 📚 Documentation Map

| Document | Purpose | Read Time |
|----------|---------|-----------|
| **IMAM_FEATURE_GUIDE.md** | Feature overview and quick start | 10 min |
| **IMAM_CONSULTATION_GUIDE.md** | User guide with workflows | 15 min |
| **IMAM_MANAGEMENT_GUIDE.md** | Admin guide and best practices | 15 min |
| **API_REFERENCE_COMPLETE.md** | Complete API documentation | 20 min |
| **IMPLEMENTATION_COMPLETE.md** | Technical summary | 10 min |

**Total: ~70 minutes to read all documentation**

---

## 🐛 Troubleshooting

### Issue: Tables Not Created

**Solution:**
```bash
# Check if database file exists
ls ramadan.db

# If missing, create it:
python -c "from app.database import Base, engine; Base.metadata.create_all(engine)"

# Restart server
python -m uvicorn app.main:app --reload
```

### Issue: Sample Data Not Appearing

**Solution:**
```bash
# Check if script ran successfully
python scripts/populate_sample_imams.py

# Look for "Created: 8" in output
# If not, check error messages and fix conflicts
```

### Issue: Endpoint Returns 404

**Solution:**
1. Verify router imported in `app/main.py`:
   ```python
   from app.routes import search, health, imam
   app.include_router(imam.router)
   ```
2. Restart server
3. Check Swagger UI for endpoint availability

### Issue: Email Conflict

**Solution:**
If getting "Email already exists":
```bash
# Clear imam table (careful!)
python -c "from app.database import SessionLocal; from app.models.imam import Imam; db = SessionLocal(); db.query(Imam).delete(); db.commit()"

# Repopulate
python scripts/populate_sample_imams.py
```

---

## 🔧 Quick Commands Reference

### Start Server
```bash
python -m uvicorn app.main:app --host localhost --port 8001 --reload
```

### Populate Sample Data
```bash
python scripts/populate_sample_imams.py
```

### View Swagger UI
```bash
# Open in browser:
http://localhost:8001/docs
```

### Check Database
```bash
# List all imams
curl http://localhost:8001/api/v1/imam/imams

# Get specific imam
curl http://localhost:8001/api/v1/imam/imams/1

# List imams by specialization
curl http://localhost:8001/api/v1/imam/imams/by-specialization/family
```

---

## 📋 Feature Overview

### What You Can Do Now

✅ **List & Browse Imams**
- View all available imams
- Filter by specialization, madhab, rating
- Check imam profiles and credentials

✅ **Book Consultations**
- Schedule appointments with imams
- Choose consultation method (phone, video, email)
- Include context from Deepseek responses

✅ **Manage Consultations**
- Track consultation status
- Confirm/complete/cancel bookings
- Rate and review imams

✅ **Quality Assurance**
- 1-5 star rating system
- User reviews
- Automatic rating calculations

---

## 📞 Getting Help

### Documentation
- 📖 See all docs in workspace root
- 🔍 Search for specific topic in guides
- 📚 API Reference has all endpoints

### Testing
- 🧪 Use Swagger UI for endpoint testing
- 📝 Sample data available for testing
- 🔗 Integration examples in docs

### Issues
1. Check Troubleshooting section above
2. Review relevant documentation file
3. Check Swagger UI for endpoint availability
4. Verify database tables exist

---

## ✨ Key Features Summary

### For Users
- 🔍 Find imams by expertise and madhab
- ⭐ See ratings and reviews
- 📅 Schedule convenient consultations
- 💬 Multiple communication methods

### For Imams
- 📋 Manage consultations
- 💼 Build reputation through ratings
- 🌍 Reach global audience
- 📊 Track consultation history

### For Developers
- 🔌 10 REST API endpoints
- 📚 Comprehensive documentation
- 🧪 Sample data included
- 🔐 Validation and error handling

---

## 🎉 Success Indicators

✅ You're ready when:
- [ ] Server starts without errors
- [ ] Swagger UI shows Imam endpoints
- [ ] Sample imams appear in GET request
- [ ] Can book new consultation
- [ ] Can rate consultation
- [ ] Ratings update imam profile
- [ ] All tests in validation checklist pass

---

## 📊 What's Included

| Component | Count | Status |
|-----------|-------|--------|
| API Endpoints | 10 | ✅ Ready |
| Sample Imams | 8 | ✅ Loaded |
| Sample Consultations | 3 | ✅ Loaded |
| Database Tables | 2 | ✅ Created |
| Documentation Files | 5 | ✅ Complete |
| Code Files | 4 | ✅ Ready |

---

## 🚀 You're All Set!

**Your Imam Consultation System is ready to use.**

### Start Now:
1. Run server: `python -m uvicorn app.main:app --reload`
2. Populate data: `python scripts/populate_sample_imams.py`
3. Test: Open `http://localhost:8001/docs`
4. Read docs: Start with IMAM_CONSULTATION_GUIDE.md

### Expected Time
- Setup: 5 minutes
- Testing: 10 minutes  
- Learning: 30 minutes
- Total: **45 minutes to production ready**

---

**Happy consulting! 🕌**

*Version: 2.0.0 | Status: Production Ready ✅*

---

## Quick Reference - Sample Curl Commands

```bash
# List all imams
curl http://localhost:8001/api/v1/imam/imams

# Filter by family specialization
curl "http://localhost:8001/api/v1/imam/imams?specialization=family"

# Filter by Hanafi madhab with high rating
curl "http://localhost:8001/api/v1/imam/imams?madhab=Hanafi&min_rating=4.5"

# Get imam details
curl http://localhost:8001/api/v1/imam/imams/1

# Book consultation
curl -X POST http://localhost:8001/api/v1/imam/consultations/book \
  -H "Content-Type: application/json" \
  -d '{
    "imam_id": 1,
    "title": "Marriage Help",
    "description": "Need guidance",
    "category": "family",
    "user_email": "user@test.com",
    "preferred_method": "phone",
    "preferred_date": "2026-02-01T18:00:00"
  }'

# Get consultation details
curl http://localhost:8001/api/v1/imam/consultations/1

# Rate consultation  
curl -X PUT http://localhost:8001/api/v1/imam/consultations/1/rate \
  -H "Content-Type: application/json" \
  -d '{"rating": 5, "review": "Excellent!"}'
```

---

**Everything is ready. Start your engines! 🚀**
