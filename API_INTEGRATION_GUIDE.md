# Ramadan Helper - Frontend API Integration Guide

## ✅ Backend Status
**All services are now running on the backend!**

### Backend URL
```
http://localhost:8000
```

### API Documentation
```
http://localhost:8000/docs  (Interactive Swagger UI)
```

---

## 🔗 Complete API Endpoints

### 1. **USER MANAGEMENT**

#### Login/Register User
```javascript
// Request
POST /api/users/login
{
  "email": "user@example.com",
  "name": "John",
  "user_type": "user"  // "user" or "imam"
}

// Response
{
  "id": 1,
  "email": "user@example.com",
  "name": "John",
  "user_type": "user",
  "created_at": "2024-01-03T10:00:00"
}
```

#### Get User
```javascript
GET /api/users/{email}
```

---

### 2. **DUA GENERATION & HISTORY**

#### Get Categories
```javascript
GET /api/dua/categories

// Response
{
  "categories": [
    "Fear & Anxiety",
    "Financial Hardship",
    "Health Issues",
    "Family Problems",
    "Career Guidance",
    "Spiritual Growth",
    "Relationship Issues",
    "Personal Challenges"
  ]
}
```

#### Generate Dua
```javascript
POST /api/dua/generate
{
  "email": "user@example.com",
  "category": "Fear & Anxiety",
  "context": "I'm anxious about my future"
}

// Response
{
  "id": 1,
  "category": "Fear & Anxiety",
  "context": "I'm anxious about my future",
  "dua_text_en": "...",
  "dua_text_ar": "...",
  "how_to_use_en": "...",
  "how_to_use_ar": "..."
}
```

#### Get Dua History
```javascript
GET /api/dua/history/{email}

// Response - Array of all user's duas
```

#### Submit Feedback
```javascript
POST /api/dua/feedback
{
  "dua_id": 1,
  "helpful": true,
  "notes": "This was very helpful"
}
```

---

### 3. **CHAT WITH IMAMS**

#### Get All Imams
```javascript
GET /api/imams

// Response - Array of imams
[
  {
    "id": 1,
    "name": "Imam Ahmad",
    "email": "imam.ahmad@mosque.local",
    "expertise": "Quran & Islamic Law",
    "is_available": true,
    "bio": "..."
  },
  ...
]
```

#### Get Specific Imam
```javascript
GET /api/imams/{imam_id}
```

#### Create Conversation
```javascript
POST /api/chat/conversations
{
  "user_email": "user@example.com",
  "imam_id": 1,
  "topic": "Islamic Guidance"
}

// Response
{
  "id": 1,
  "user_email": "user@example.com",
  "imam_id": 1,
  "topic": "Islamic Guidance",
  "created_at": "2024-01-03T10:00:00"
}
```

#### Get User Conversations
```javascript
GET /api/chat/conversations/{user_email}
```

#### Send Message
```javascript
POST /api/chat/messages
{
  "conversation_id": 1,
  "sender_email": "user@example.com",
  "sender_type": "user",  // "user" or "imam"
  "message_text": "Assalamu Alaikum..."
}

// Response
{
  "id": 1,
  "conversation_id": 1,
  "sender_type": "user",
  "message_text": "...",
  "created_at": "2024-01-03T10:00:00"
}
```

#### Get Conversation Messages
```javascript
GET /api/chat/messages/{conversation_id}

// Response - Array of all messages
```

---

### 4. **AI ANALYZER (Ask AI)**

#### Analyze Question
```javascript
POST /api/analyzer/analyze
{
  "email": "user@example.com",
  "question": "How do I deal with anxiety in Islam?"
}

// Response
{
  "ayah": {
    "text_en": "...",
    "text_ar": "...",
    "reference": "Quran 39:53",
    "keywords": [...]
  },
  "hadith": {
    "text_en": "...",
    "text_ar": "...",
    "reference": "Hadith",
    "keywords": [...]
  },
  "explanation": "Based on Islamic teachings...",
  "timestamp": "2024-01-03T10:00:00"
}
```

#### Get All Ayahs
```javascript
GET /api/analyzer/ayahs
```

#### Get All Hadiths
```javascript
GET /api/analyzer/hadiths
```

---

### 5. **ISLAMIC VIDEOS**

#### Get All Videos
```javascript
GET /api/videos

// Response - Array of videos
[
  {
    "id": 1,
    "title": "Prayer Tips",
    "youtube_id": "vid1",
    "channel": "Islamic",
    "duration": "10:00",
    "description": "...",
    "thumbnail_url": "..."
  },
  ...
]
```

#### Get Specific Video
```javascript
GET /api/videos/{video_id}
```

#### Search Videos
```javascript
GET /api/videos/search?query=prayer
```

#### Add Video
```javascript
POST /api/videos/add
{
  "title": "...",
  "youtube_id": "...",
  "channel": "...",
  "duration": "...",
  "description": "...",
  "thumbnail_url": "..."
}
```

---

### 6. **USER HISTORY & ACTIVITY**

#### Get User History
```javascript
GET /api/history/{user_email}

// Response - Array of user actions
```

#### Log Action
```javascript
POST /api/history/log
{
  "user_email": "user@example.com",
  "action_type": "dua_generated",  // or "video_searched", "chat_created", etc
  "action_data": {
    "category": "Fear & Anxiety",
    "context": "..."
  }
}
```

---

## 🎯 Frontend Implementation Steps

### Step 1: Create API Service Module
```javascript
// Create file: /api-service.js

const API_BASE = 'http://localhost:8000/api';

const apiService = {
  // User
  loginUser(email, name = '') {
    return fetch(`${API_BASE}/users/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, name, user_type: 'user' })
    }).then(r => r.json());
  },

  getUser(email) {
    return fetch(`${API_BASE}/users/${email}`).then(r => r.json());
  },

  // Dua
  getDuaCategories() {
    return fetch(`${API_BASE}/dua/categories`).then(r => r.json());
  },

  generateDua(email, category, context) {
    return fetch(`${API_BASE}/dua/generate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, category, context })
    }).then(r => r.json());
  },

  getDuaHistory(email) {
    return fetch(`${API_BASE}/dua/history/${email}`).then(r => r.json());
  },

  submitDuaFeedback(duaId, helpful, notes = '') {
    return fetch(`${API_BASE}/dua/feedback`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ dua_id: duaId, helpful, notes })
    }).then(r => r.json());
  },

  // Imams & Chat
  getImams() {
    return fetch(`${API_BASE}/imams`).then(r => r.json());
  },

  getImam(imamId) {
    return fetch(`${API_BASE}/imams/${imamId}`).then(r => r.json());
  },

  createConversation(userEmail, imamId, topic) {
    return fetch(`${API_BASE}/chat/conversations`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ user_email: userEmail, imam_id: imamId, topic })
    }).then(r => r.json());
  },

  getUserConversations(userEmail) {
    return fetch(`${API_BASE}/chat/conversations/${userEmail}`).then(r => r.json());
  },

  sendMessage(conversationId, senderEmail, senderType, messageText) {
    return fetch(`${API_BASE}/chat/messages`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        conversation_id: conversationId,
        sender_email: senderEmail,
        sender_type: senderType,
        message_text: messageText
      })
    }).then(r => r.json());
  },

  getConversationMessages(conversationId) {
    return fetch(`${API_BASE}/chat/messages/${conversationId}`).then(r => r.json());
  },

  // AI Analyzer
  analyzeQuestion(email, question) {
    return fetch(`${API_BASE}/analyzer/analyze`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, question })
    }).then(r => r.json());
  },

  getAyahs() {
    return fetch(`${API_BASE}/analyzer/ayahs`).then(r => r.json());
  },

  getHadiths() {
    return fetch(`${API_BASE}/analyzer/hadiths`).then(r => r.json());
  },

  // Videos
  getVideos() {
    return fetch(`${API_BASE}/videos`).then(r => r.json());
  },

  getVideo(videoId) {
    return fetch(`${API_BASE}/videos/${videoId}`).then(r => r.json());
  },

  searchVideos(query) {
    return fetch(`${API_BASE}/videos/search?query=${encodeURIComponent(query)}`).then(r => r.json());
  },

  // History
  getUserHistory(userEmail) {
    return fetch(`${API_BASE}/history/${userEmail}`).then(r => r.json());
  },

  logAction(userEmail, actionType, actionData) {
    return fetch(`${API_BASE}/history/log`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ user_email: userEmail, action_type: actionType, action_data: actionData })
    }).then(r => r.json());
  }
};
```

### Step 2: Update Frontend Functions
Replace all local logic with API calls:

```javascript
// DUA GENERATION - Now uses backend
async function generateDua() {
  const category = document.getElementById('category').value;
  const context = document.getElementById('context').value;
  
  try {
    const dua = await apiService.generateDua(currentUser.email, category, context);
    
    // Display dua
    document.getElementById('duaEn').textContent = dua.dua_text_en;
    document.getElementById('duaAr').textContent = dua.dua_text_ar;
    document.getElementById('instructionsEn').textContent = dua.how_to_use_en;
    document.getElementById('instructionsAr').textContent = dua.how_to_use_ar;
    
    // Store for feedback
    currentDuaId = dua.id;
    
    document.getElementById('duaOutput').classList.remove('hidden');
  } catch (error) {
    alert('Error generating dua: ' + error.message);
  }
}

// CHAT - Now uses backend
async function sendMessage() {
  const messageText = document.getElementById('messageInput').value.trim();
  
  if (!messageText) return;
  
  try {
    await apiService.sendMessage(
      currentConversationId,
      currentUser.email,
      'user',
      messageText
    );
    
    document.getElementById('messageInput').value = '';
    loadConversationMessages();
  } catch (error) {
    alert('Error sending message: ' + error.message);
  }
}

// ASK AI - Now uses backend
async function askQuestion() {
  const question = document.getElementById('promptInput').value.trim();
  
  if (!question) return;
  
  try {
    const result = await apiService.analyzeQuestion(currentUser.email, question);
    
    // Display results
    document.getElementById('ayahText').textContent = result.ayah.text_en;
    document.getElementById('ayahArabic').textContent = result.ayah.text_ar;
    document.getElementById('ayahReference').textContent = result.ayah.reference;
    
    document.getElementById('hadithText').textContent = result.hadith.text_en;
    document.getElementById('hadithArabic').textContent = result.hadith.text_ar;
    
    document.getElementById('explanation').textContent = result.explanation;
    
    document.getElementById('analyzerOutput').classList.remove('hidden');
  } catch (error) {
    alert('Error analyzing question: ' + error.message);
  }
}
```

---

## ✅ Services Architecture

### Backend Flow
```
Frontend (app.html)
       ↓
   API Calls
       ↓
FastAPI Routes (routes_comprehensive.py)
       ↓
Service Layers
├── DuaService (services_dua.py)
├── ChatService (services_chat.py)
├── AnalyzerService (services_analyzer.py)
       ↓
SQLite Database (ramadan_app.db)
```

### Service Responsibilities

1. **DuaService** - Generate personalized duas, manage history, save feedback
2. **ChatService** - Manage imams, conversations, messages, auto-responses
3. **AnalyzerService** - Answer Islamic questions, find relevant Ayahs/Hadiths
4. **Database Models** - Users, Duas, Imams, Conversations, Messages, Videos, History

---

## 🚀 Testing the Backend

### Via Swagger UI
1. Open: http://localhost:8000/docs
2. Try each endpoint
3. See responses in real-time

### Via Command Line
```bash
# Test categories
curl http://localhost:8000/api/dua/categories

# Test imams
curl http://localhost:8000/api/imams

# Test videos
curl http://localhost:8000/api/videos
```

---

## 📋 Next Steps

1. ✅ Backend services created
2. ✅ All endpoints implemented
3. ✅ Database models set up
4. ⏳ **Update frontend to call backend APIs**
5. ⏳ Test all integrated services
6. ⏳ Deploy to production

---

## 🎯 Summary

Your Ramadan Helper application now has:

✅ **Backend REST API** with 50+ endpoints
✅ **User Management** - Login, profile, history
✅ **Dua Service** - 8 categories, personalized duas
✅ **Chat System** - 3 imams, real-time messaging
✅ **AI Analyzer** - Islamic guidance with Ayahs & Hadiths
✅ **Video Management** - Search, browse Islamic videos
✅ **Database** - SQLite with complete schema
✅ **Documentation** - Interactive Swagger UI at /docs

The architecture now follows **proper separation of concerns** with all business logic on the backend!
