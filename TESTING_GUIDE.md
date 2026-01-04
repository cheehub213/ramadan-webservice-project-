# 🧪 Quick Start Guide - Testing the Backend

## ✅ Prerequisites
- Backend running on `http://localhost:8000`
- Browser or API testing tool (curl, Postman, etc.)

---

## 🌐 Testing via Browser

### 1. Open Swagger UI
```
http://localhost:8000/docs
```
This interactive interface lets you test all endpoints without writing code.

---

## 🧪 Testing via Command Line (PowerShell)

### 1. Test User Login
```powershell
$body = @{
    email = "user@example.com"
    name = "Test User"
    user_type = "user"
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://localhost:8000/api/users/login" `
  -Method POST `
  -ContentType "application/json" `
  -Body $body | Select-Object -ExpandProperty Content | ConvertFrom-Json
```

### 2. Get Dua Categories
```powershell
Invoke-WebRequest -Uri "http://localhost:8000/api/dua/categories" `
  -UseBasicParsing | Select-Object -ExpandProperty Content | ConvertFrom-Json
```

### 3. Generate Dua
```powershell
$body = @{
    email = "user@example.com"
    category = "Fear & Anxiety"
    context = "I am anxious about my future"
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://localhost:8000/api/dua/generate" `
  -Method POST `
  -ContentType "application/json" `
  -Body $body | Select-Object -ExpandProperty Content | ConvertFrom-Json
```

### 4. Get Imams
```powershell
Invoke-WebRequest -Uri "http://localhost:8000/api/imams" `
  -UseBasicParsing | Select-Object -ExpandProperty Content | ConvertFrom-Json
```

### 5. Analyze Question
```powershell
$body = @{
    email = "user@example.com"
    question = "How do I deal with anxiety in Islam?"
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://localhost:8000/api/analyzer/analyze" `
  -Method POST `
  -ContentType "application/json" `
  -Body $body | Select-Object -ExpandProperty Content | ConvertFrom-Json
```

### 6. Get Videos
```powershell
Invoke-WebRequest -Uri "http://localhost:8000/api/videos" `
  -UseBasicParsing | Select-Object -ExpandProperty Content | ConvertFrom-Json
```

---

## 📝 Testing via Curl

### 1. Login
```bash
curl -X POST http://localhost:8000/api/users/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "name": "Test User",
    "user_type": "user"
  }'
```

### 2. Generate Dua
```bash
curl -X POST http://localhost:8000/api/dua/generate \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "category": "Fear & Anxiety",
    "context": "I am anxious about my future"
  }'
```

### 3. Get Imams
```bash
curl http://localhost:8000/api/imams
```

### 4. Analyze Question
```bash
curl -X POST http://localhost:8000/api/analyzer/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "question": "How do I deal with anxiety in Islam?"
  }'
```

---

## 🔧 Testing via JavaScript

```javascript
// Simple test function
async function testBackend() {
  const API = 'http://localhost:8000/api';
  
  try {
    // 1. Login
    const loginRes = await fetch(`${API}/users/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        email: 'user@example.com',
        name: 'Test User',
        user_type: 'user'
      })
    });
    console.log('Login:', await loginRes.json());
    
    // 2. Get categories
    const catRes = await fetch(`${API}/dua/categories`);
    console.log('Categories:', await catRes.json());
    
    // 3. Get imams
    const imamRes = await fetch(`${API}/imams`);
    console.log('Imams:', await imamRes.json());
    
    // 4. Generate dua
    const duaRes = await fetch(`${API}/dua/generate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        email: 'user@example.com',
        category: 'Fear & Anxiety',
        context: 'I am anxious about my future'
      })
    });
    console.log('Generated Dua:', await duaRes.json());
    
    // 5. Analyze question
    const analyzeRes = await fetch(`${API}/analyzer/analyze`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        email: 'user@example.com',
        question: 'How do I deal with anxiety in Islam?'
      })
    });
    console.log('Analysis:', await analyzeRes.json());
    
  } catch (error) {
    console.error('Error:', error);
  }
}

// Run test
testBackend();
```

---

## ✅ Testing Checklist

Use this checklist to verify all services are working:

### User Management
- [ ] POST /api/users/login - Returns user object
- [ ] GET /api/users/{email} - Returns user profile

### Dua Service
- [ ] GET /api/dua/categories - Returns 8 categories
- [ ] POST /api/dua/generate - Returns bilingual dua
- [ ] GET /api/dua/history/{email} - Returns user's duas
- [ ] POST /api/dua/feedback - Saves feedback

### Chat Service
- [ ] GET /api/imams - Returns 3 imams
- [ ] GET /api/imams/{id} - Returns specific imam
- [ ] POST /api/chat/conversations - Creates conversation
- [ ] GET /api/chat/conversations/{email} - Returns user conversations
- [ ] POST /api/chat/messages - Sends message
- [ ] GET /api/chat/messages/{id} - Returns conversation messages

### AI Analyzer
- [ ] POST /api/analyzer/analyze - Analyzes question with Ayah & Hadith
- [ ] GET /api/analyzer/ayahs - Returns all Ayahs
- [ ] GET /api/analyzer/hadiths - Returns all Hadiths

### Videos
- [ ] GET /api/videos - Returns all videos
- [ ] GET /api/videos/{id} - Returns specific video
- [ ] GET /api/videos/search?query=... - Searches videos

### History
- [ ] GET /api/history/{email} - Returns user history
- [ ] POST /api/history/log - Logs action

---

## 🐛 Troubleshooting

### Error: Connection Refused
```
Issue: Cannot connect to http://localhost:8000
Solution: Make sure backend is running
  cd backend
  python main.py
```

### Error: CORS Issues
```
Issue: Frontend can't call API from different origin
Solution: CORS is already enabled in main.py
```

### Error: 404 Not Found
```
Issue: Endpoint doesn't exist
Solution: Check API_INTEGRATION_GUIDE.md for correct endpoint path
```

### Error: 500 Internal Server Error
```
Issue: Backend error
Solution: Check terminal output for error details
```

---

## 📊 Sample Response Examples

### Dua Generation Response
```json
{
  "id": 1,
  "category": "Fear & Anxiety",
  "context": "I am anxious about my future",
  "dua_text_en": "O Allah, remove my fear and anxiety...",
  "dua_text_ar": "اللهم أذهب عني الخوف والقلق...",
  "how_to_use_en": "Recite this dua with sincere intention...",
  "how_to_use_ar": "اقرأ هذا الدعاء بنية صادقة...",
  "timestamp": "2024-01-03T10:00:00"
}
```

### Imam Response
```json
{
  "id": 1,
  "name": "Imam Ahmad",
  "email": "imam.ahmad@mosque.local",
  "expertise": "Quran & Islamic Law",
  "is_available": true,
  "bio": "Expert in Quranic interpretation..."
}
```

### Analysis Response
```json
{
  "ayah": {
    "text_en": "Do not despair of the mercy of Allah...",
    "text_ar": "لا تقنطوا من رحمة الله...",
    "reference": "Quran 39:53",
    "keywords": ["despair", "mercy", "forgive", "sin"]
  },
  "hadith": {
    "text_en": "The strongest person is the one who controls himself...",
    "text_ar": "الرجل القوي الذي يملك نفسه...",
    "reference": "Hadith",
    "keywords": ["anger", "control", "strength"]
  },
  "explanation": "Based on Islamic teachings...",
  "timestamp": "2024-01-03T10:00:00"
}
```

---

## 🎯 Success Indicators

✅ All endpoints return 200 OK or appropriate status codes
✅ Response data matches expected format
✅ Data persists in database (check subsequent GET requests)
✅ No CORS errors in browser console
✅ Swagger UI at /docs loads without errors

---

## 📞 Quick Reference

| Task | Command |
|------|---------|
| View Docs | http://localhost:8000/docs |
| Test API | Swagger UI or curl |
| Check DB | backend/ramadan_app.db |
| Restart Backend | python main.py |
| View Logs | Terminal output |

---

Great! Your backend is ready for testing! 🎉
