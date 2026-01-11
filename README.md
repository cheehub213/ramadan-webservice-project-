# 🌙 Ramadan Helper - Islamic Web Application

A comprehensive Islamic web application that provides spiritual guidance, personalized duas, AI-powered Islamic Q&A, imam consultations, Islamic video search, and **Ramadan Events platform for Tunisia**.

![Python](https://img.shields.io/badge/Python-3.12-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-green)
![SQLite](https://img.shields.io/badge/Database-SQLite-orange)
![JWT](https://img.shields.io/badge/Auth-JWT-red)
![License](https://img.shields.io/badge/License-MIT-purple)

---

## 📌 Project Description

**Ramadan Helper** is a full-stack web application designed to support Muslims in their spiritual journey during Ramadan and beyond. The application combines Islamic scholarship with AI technology to provide:

- 🔐 **JWT Authentication** - Secure login with email verification and Bearer token authentication
- 🤖 **AI-Powered Islamic Q&A** - Ask questions and receive relevant Quran verses (Ayahs) using semantic search
- 📿 **Personalized Dua Generator** - Generate custom duas in both English and Arabic based on your specific situation
- 💬 **Chat with Imams** - Real-time messaging system to consult with qualified Islamic scholars
- 📺 **Islamic Video Search** - AI-powered YouTube video recommendations based on your spiritual needs
- 🎪 **Ramadan Events (Tunisia)** - Browse and post Ramadan events across all 24 Tunisian governorates with monetization
- 📚 **User History Tracking** - Keep track of your spiritual journey and previous interactions

### 💰 Events Monetization (Tunisia)
| Listing Type | Price | Features |
|--------------|-------|----------|
| **Basic** | 20 TND | Standard listing in search results |
| **Featured** | 50 TND | Premium placement, highlighted, top of results |

---

## 📌 Features List

### 🔐 Authentication & Security
- **JWT Bearer Tokens** - Secure API authentication
- **Email Verification** - 6-digit code verification system
- **Password Reset** - Secure password recovery flow
- **Role-Based Access** - Separate permissions for users and imams
- **Protected Endpoints** - 🔒 Lock icons in Swagger for secured routes

### 🤖 AI Analyzer (Ask AI)
- Ask any Islamic question in natural language
- Receive relevant Quran verses with surah and verse numbers
- **Semantic Search** through 6,236+ Quran verses
- Similarity scoring for verse relevance
- History tracking for all queries

### 📿 Dua Generator
- **7 Categories**: Fear & Anxiety, Financial Hardship, Health Issues, Family Problems, Career Guidance, Spiritual Growth, Relationship Issues
- **Bilingual Output**: Duas provided in both English and Arabic
- **Personalized**: AI generates duas specific to your described situation
- **Usage Instructions**: Guidance on when and how to recite the dua
- **History Tracking**: All generated duas saved to your account
- **Feedback System**: Rate the helpfulness of duas

### 💬 Chat with Imam
- Browse available Imams with their expertise areas
- Create private conversation threads
- Real-time messaging interface
- Message read/unread status tracking
- **Imam Dashboard** for responding to inquiries
- Conversation history preserved

### 📺 Islamic Video Search
- AI-powered keyword extraction from natural language
- YouTube integration for video search
- Personalized video recommendations
- Video metadata including duration, channel, and thumbnails

### 🎪 Ramadan Events (Tunisia) - NEW!
- **Browse Events** - Filter by city, category, date
- **24 Tunisian Cities** - All governorates supported
- **11 Event Categories**: Restaurant, Iftar, Suhoor, Charity, Entertainment, Religious, Concert, Family, Sports, Market, Other
- **Featured Events** - Premium placement for paid listings
- **Post Your Event** - Create and manage your own events
- **View Tracking** - Track event popularity
- **Organizer Dashboard** - Manage your event listings

### 👤 User Management
- Secure email-based authentication with JWT
- Separate login for users and imams
- User activity history tracking
- Session persistence with token storage

---

## 📌 How to Install/Run

### Prerequisites
- Python 3.10+ installed
- pip (Python package manager)
- Git (optional)

### Step 1: Clone the Repository
```bash
git clone https://github.com/cheehub213/ramadan-webservice-project-.git
cd ramadan-webservice-project-
```

### Step 2: Create Virtual Environment
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS/Linux
python3 -m venv .venv
source .venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt

# Additional packages for JWT authentication
pip install python-jose passlib bcrypt python-multipart
```

### Step 4: Set Up Environment Variables
Create a `.env` file in the `backend/` folder:
```env
# AI Service API Key (Groq)
GROQ_API_KEY=your_groq_api_key_here

# YouTube API Key (optional - for video search)
YOUTUBE_API_KEY=your_youtube_api_key
```

### Step 5: Run the Backend Server
```bash
cd backend
python run_server.py
```
The API will be available at: `http://localhost:8000`
API Documentation: `http://localhost:8000/docs`

### Step 6: Run the Frontend Server
```bash
# From project root
python start_frontend.py
```
Then visit: `http://localhost:8080/app.html`

---

## 📌 API Endpoints Documentation

Base URL: `http://localhost:8000/api`

> 🔒 = Requires JWT Authentication (Bearer Token)

### 🔐 Authentication Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| `POST` | `/auth/signup` | Register new user | ❌ |
| `POST` | `/auth/verify` | Verify email with 6-digit code | ❌ |
| `POST` | `/auth/login` | Login and get JWT token | ❌ |
| `POST` | `/auth/token` | OAuth2 token (for Swagger) | ❌ |
| `POST` | `/auth/resend-code` | Resend verification code | ❌ |
| `POST` | `/auth/forgot-password` | Request password reset | ❌ |
| `POST` | `/auth/reset-password` | Reset password with code | ❌ |

### 👤 User Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| `GET` | `/users/me` | Get current user profile | 🔒 |
| `GET` | `/users/{email}` | Get user by email | 🔒 |
| `PUT` | `/users/{email}` | Update user profile | 🔒 |
| `DELETE` | `/users/{email}` | Delete user account | 🔒 |

### 📿 Dua Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| `GET` | `/dua/categories` | Get all dua categories | ❌ |
| `POST` | `/dua/generate` | Generate a personalized dua | 🔒 |
| `GET` | `/dua/history` | Get current user's dua history | 🔒 |
| `GET` | `/dua/history/{email}` | Get user's dua history by email | 🔒 |
| `POST` | `/dua/feedback` | Submit feedback on a dua | 🔒 |

### 🕌 Chat Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| `GET` | `/chat/imams` | Get all available imams | ❌ |
| `GET` | `/chat/imams/{imam_id}` | Get specific imam details | ❌ |
| `POST` | `/chat/conversations` | Create new conversation | 🔒 |
| `GET` | `/chat/my-conversations` | Get current user's conversations | 🔒 |
| `GET` | `/chat/conversations/{user_email}` | Get user's conversations | 🔒 |
| `POST` | `/chat/messages` | Send a message | 🔒 |
| `GET` | `/chat/messages/{conversation_id}` | Get messages in conversation | 🔒 |
| `GET` | `/chat/all-conversations` | Get all conversations (Imam only) | 🔒 Imam |
| `GET` | `/chat/imam/{imam_id}/conversations` | Get imam's conversations | 🔒 Imam |

### 🤖 AI Analyzer Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| `POST` | `/analyzer/analyze` | Analyze question with semantic search | 🔒 |
| `GET` | `/analyzer/topics` | Get available topics | ❌ |
| `GET` | `/analyzer/ayahs` | Get all Quranic verses | ❌ |

### 📺 Video Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| `POST` | `/videos/search` | AI-powered video search | 🔒 |

### 🎪 Events Endpoints (Tunisia) - NEW!

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| `GET` | `/events` | Get all events (with filters) | ❌ |
| `GET` | `/events/cities` | Get all Tunisia cities | ❌ |
| `GET` | `/events/categories` | Get event categories | ❌ |
| `GET` | `/events/featured` | Get featured/premium events | ❌ |
| `GET` | `/events/{event_id}` | Get event details | ❌ |
| `POST` | `/events` | Create new event | 🔒 |
| `GET` | `/events/my-events` | Get current user's events | 🔒 |
| `GET` | `/events/organizer/{email}` | Get organizer's events | 🔒 |
| `DELETE` | `/events/{event_id}` | Delete event | 🔒 |

### 📊 Statistics Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| `GET` | `/stats/dashboard` | Get platform statistics | 🔒 |
| `GET` | `/stats/user/{email}` | Get user statistics | 🔒 |

### ❤️ Health Check

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| `GET` | `/health` | Check API health status | ❌ |

---

## 📌 Sample Responses

### Generate Dua Response
```json
POST /api/dua/generate
{
  "email": "user@example.com",
  "category": "Fear & Anxiety",
  "context": "I'm feeling anxious about my upcoming job interview"
}

Response:
{
  "id": 1,
  "category": "Fear & Anxiety",
  "context": "I'm feeling anxious about my upcoming job interview",
  "dua_text_en": "O Allah, the Most Merciful, calm my heart and ease my anxiety as I face this job interview. Grant me confidence in Your plan and help me trust that You are the best of planners. Remove the fear from my heart and replace it with peace and certainty in Your wisdom.",
  "dua_text_ar": "اللَّهُمَّ يَا أَرْحَمَ الرَّاحِمِينَ، سَكِّنْ قَلْبِي وَأَزِلْ قَلَقِي وَأَنَا أُوَاجِهُ هَذِهِ الْمُقَابَلَةَ. امْنَحْنِي الثِّقَةَ فِي خُطَّتِكَ وَأَعِنِّي عَلَى التَّوَكُّلِ عَلَيْكَ فَأَنْتَ خَيْرُ الْمَاكِرِينَ.",
  "how_to_use_en": "Recite this dua before your interview, preferably after Fajr prayer. Take deep breaths and trust in Allah's plan.",
  "how_to_use_ar": "اقرأ هذا الدعاء قبل المقابلة، ويُفضَّل بعد صلاة الفجر",
  "ai_generated": true,
  "timestamp": "2026-01-11T10:30:00"
}
```

### AI Analyzer Response
```json
POST /api/analyzer/analyze
{
  "email": "user@example.com",
  "question": "How do I deal with anxiety?"
}

Response:
{
  "quran_verse": {
    "surah": "Ar-Ra'd",
    "surah_number": 13,
    "verse_number": 28,
    "arabic": "أَلَا بِذِكْرِ اللَّهِ تَطْمَئِنُّ الْقُلُوبُ",
    "english": "Verily, in the remembrance of Allah do hearts find rest.",
    "relevance_score": 0.95
  },
  "hadith": {
    "narrator": "Abu Hurairah",
    "source": "Sahih Muslim",
    "arabic": "مَنْ نَفَّسَ عَنْ مُؤْمِنٍ كُرْبَةً مِنْ كُرَبِ الدُّنْيَا نَفَّسَ اللَّهُ عَنْهُ كُرْبَةً مِنْ كُرَبِ يَوْمِ الْقِيَامَةِ",
    "english": "Whoever relieves a believer's distress of the distressful aspects of this world, Allah will rescue him from a difficulty of the difficulties of the Hereafter."
  },
  "ai_explanation": "Islam provides powerful tools for managing anxiety. The Quran emphasizes that remembrance of Allah (dhikr) brings peace to the heart. Regular prayer, recitation of Quran, and making dua are recommended practices. Trust in Allah's plan (tawakkul) also helps reduce anxiety about the future."
}
```

### Chat Conversation Response
```json
POST /api/chat/conversations
{
  "user_email": "user@example.com",
  "imam_id": 1,
  "topic": "Questions about Ramadan fasting"
}

Response:
{
  "id": 1,
  "user_email": "user@example.com",
  "imam_id": 1,
  "topic": "Questions about Ramadan fasting",
  "created_at": "2026-01-11T10:00:00"
}
```

### Get Imams Response
```json
GET /api/imams

Response:
[
  {
    "id": 1,
    "name": "Sheikh Ahmad Al-Rashid",
    "email": "sheikh.ahmad@mosque.com",
    "expertise": "Fiqh & Islamic Jurisprudence",
    "is_available": true,
    "bio": "20+ years of Islamic scholarship"
  },
  {
    "id": 2,
    "name": "Imam Muhammad Hassan",
    "email": "imam.hassan@mosque.com",
    "expertise": "Quran Interpretation & Tafsir",
    "is_available": true,
    "bio": "Specialist in Quranic studies"
  }
]
```

### Events Response (Tunisia)
```json
GET /api/events?city=Tunis&category=iftar

Response:
{
  "events": [
    {
      "id": 1,
      "title": "Community Iftar at Grand Mosque",
      "description": "Join us for a blessed iftar gathering with the community",
      "city": "Tunis",
      "location": "Zitouna Mosque, Medina",
      "category": "iftar",
      "event_date": "2026-03-15",
      "event_time": "18:30",
      "organizer_email": "mosque@example.com",
      "organizer_name": "Zitouna Mosque Committee",
      "contact_phone": "+216 71 123 456",
      "is_featured": true,
      "listing_type": "featured",
      "price": 50,
      "created_at": "2026-03-01T10:00:00"
    },
    {
      "id": 2,
      "title": "Tarawih Prayer Night",
      "description": "Special tarawih prayer with renowned Qari",
      "city": "Tunis",
      "location": "Al-Fath Mosque",
      "category": "tarawih",
      "event_date": "2026-03-16",
      "event_time": "20:00",
      "organizer_email": "alfath@example.com",
      "is_featured": false,
      "listing_type": "basic",
      "price": 20,
      "created_at": "2026-03-02T14:30:00"
    }
  ],
  "total": 2
}
```

### Create Event Response
```json
POST /api/events
Authorization: Bearer <your_jwt_token>

{
  "title": "Ramadan Food Drive",
  "description": "Help distribute food to families in need",
  "city": "Sfax",
  "location": "Central Market, Downtown",
  "category": "charity",
  "event_date": "2026-03-20",
  "event_time": "09:00",
  "contact_phone": "+216 74 123 456",
  "listing_type": "featured"
}

Response:
{
  "id": 3,
  "title": "Ramadan Food Drive",
  "description": "Help distribute food to families in need",
  "city": "Sfax",
  "location": "Central Market, Downtown",
  "category": "charity",
  "event_date": "2026-03-20",
  "event_time": "09:00",
  "organizer_email": "user@example.com",
  "organizer_name": "Ahmed Ben Ali",
  "contact_phone": "+216 74 123 456",
  "is_featured": true,
  "listing_type": "featured",
  "price": 50,
  "created_at": "2026-03-10T08:00:00"
}
```

### Get Cities Response
```json
GET /api/events/cities

Response:
{
  "cities": [
    "Tunis", "Sfax", "Sousse", "Kairouan", "Bizerte",
    "Gabès", "Ariana", "Gafsa", "Monastir", "Ben Arous",
    "Kasserine", "Médenine", "Nabeul", "Tataouine", "Béja",
    "Jendouba", "Mahdia", "Sidi Bouzid", "Tozeur", "Siliana",
    "Kébili", "Zaghouan", "Manouba", "Le Kef"
  ]
}
```

### Health Check Response
```json
GET /api/health

Response:
{
  "status": "healthy",
  "message": "Backend is running",
  "database": "sqlite",
  "timestamp": "2026-01-11T10:30:00"
}
```

---

## 📌 Screenshots

### 🏠 Home Page
```
┌─────────────────────────────────────────────────────────────┐
│  🌙 Ramadan Helper                    [Home] [Login/Signup] │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│           ☪️ Welcome to Ramadan Helper                      │
│     Your personal Islamic companion for duas,               │
│         guidance, and spiritual connection                  │
│                                                             │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐       │
│  │ 🤖 Ask   │ │ 📿 Dua   │ │ 📺 Videos│ │ 💬 Chat  │       │
│  │    AI    │ │Generator │ │          │ │with Imam │       │
│  │          │ │          │ │          │ │          │       │
│  │ AI-power │ │Bilingual │ │ YouTube  │ │ Real     │       │
│  │ guidance │ │ duas     │ │ search   │ │ scholars │       │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘       │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ 🎪 Ramadan Events in Tunisia                         │  │
│  │    Discover iftars, tarawih, charity events & more   │  │
│  │    📍 24 cities | 💰 Basic: 20 TND | Featured: 50 TND│  │
│  │                    [🎪 View Events]                  │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### 📿 Dua Generator
```
┌─────────────────────────────────────────────────────────────┐
│              Personalized Dua Generator                     │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────────┐  ┌─────────────────────────────┐  │
│  │ Tell us your need   │  │   Your Personalized Dua     │  │
│  │                     │  │                             │  │
│  │ Category:           │  │ 🇬🇧 English:                │  │
│  │ [Fear & Anxiety ▼]  │  │ "O Allah, calm my heart..." │  │
│  │                     │  │                             │  │
│  │ Your Situation:     │  │ 🇸🇦 Arabic:                  │  │
│  │ ┌─────────────────┐ │  │ "اللَّهُمَّ سَكِّنْ قَلْبِي" │  │
│  │ │ Describe your   │ │  │                             │  │
│  │ │ situation...    │ │  │ 📖 How to use:              │  │
│  │ └─────────────────┘ │  │ Recite after Fajr prayer    │  │
│  │                     │  │                             │  │
│  │ [📿 Generate Dua]   │  └─────────────────────────────┘  │
│  └─────────────────────┘                                   │
└─────────────────────────────────────────────────────────────┘
```

### 💬 Chat with Imam
```
┌─────────────────────────────────────────────────────────────┐
│                   Chat with Imam                            │
├─────────────────────────────────────────────────────────────┤
│  Available Imams:                                           │
│  ┌────────────────────────────────────────┐                 │
│  │ 🕌 Sheikh Ahmad Al-Rashid              │                 │
│  │    Expertise: Fiqh & Islamic Law       │                 │
│  │    Status: 🟢 Available                │                 │
│  │    [Start Conversation]                │                 │
│  └────────────────────────────────────────┘                 │
│                                                             │
│  Your Conversations:                                        │
│  ┌────────────────────────────────────────┐                 │
│  │ 📝 Questions about Ramadan fasting     │                 │
│  │    with Sheikh Ahmad                   │                 │
│  │    Last message: 2 hours ago           │                 │
│  └────────────────────────────────────────┘                 │
└─────────────────────────────────────────────────────────────┘
```

### 🤖 Ask AI (Analyzer)
```
┌─────────────────────────────────────────────────────────────┐
│            Ask AI - Islamic Guidance                        │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────┐   │
│  │ Ask any Islamic question...                         │   │
│  │ "How do I deal with anxiety?"                       │   │
│  └─────────────────────────────────────────────────────┘   │
│                    [🤖 Analyze with AI]                     │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ 📖 Quran Verse                                      │   │
│  │ Surah Ar-Ra'd (13:28)                               │   │
│  │ "Verily, in the remembrance of Allah                │   │
│  │  do hearts find rest."                              │   │
│  ├─────────────────────────────────────────────────────┤   │
│  │ 📜 Hadith                                           │   │
│  │ Narrated by Abu Hurairah (Sahih Muslim)             │   │
│  │ "Whoever relieves a believer's distress..."         │   │
│  ├─────────────────────────────────────────────────────┤   │
│  │ 💡 AI Explanation                                   │   │
│  │ Islam provides powerful tools for managing          │   │
│  │ anxiety through dhikr, prayer, and tawakkul...     │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

### 🎪 Ramadan Events (Tunisia)
```
┌─────────────────────────────────────────────────────────────┐
│          🎪 Ramadan Events in Tunisia                       │
├─────────────────────────────────────────────────────────────┤
│  Filter Events:                                             │
│  City: [Tunis ▼]  Category: [All Categories ▼]  [🔍 Search] │
│                                                             │
│  ⭐ Featured Events                                         │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ ⭐ Community Iftar at Grand Mosque                  │   │
│  │ 📍 Zitouna Mosque, Tunis                            │   │
│  │ 📅 March 15, 2026 at 18:30                          │   │
│  │ 🏷️ Category: Iftar                                  │   │
│  │ 📞 +216 71 123 456                                  │   │
│  │ ──────────────────────────────────────              │   │
│  │ Join us for a blessed iftar gathering...            │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  📋 All Events                                              │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ Tarawih Prayer Night                                │   │
│  │ 📍 Al-Fath Mosque, Tunis | 📅 March 16, 20:00      │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  [➕ Post Your Event - Basic: 20 TND | Featured: 50 TND]    │
└─────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| **Backend** | FastAPI (Python 3.10+) |
| **Database** | SQLite with SQLAlchemy ORM |
| **Authentication** | JWT (python-jose, passlib, bcrypt) |
| **AI Service** | Groq API (Llama 3.1) |
| **Frontend** | HTML5, TailwindCSS, Vanilla JS |
| **Fonts** | Google Fonts (Poppins, Amiri Arabic) |
| **Video API** | YouTube Data API v3 |
| **Deployment** | Railway / Render / Docker |

---

## 🎨 Design Theme

The application features a beautiful **Ramadan Night Theme**:
- **Primary Colors**: Gold (#D4AF37), Purple (#4A1A6B), Night Blue (#1A1A2E)
- **Accent Colors**: Emerald Green (#0D5C2E)
- **Typography**: Poppins (UI), Amiri (Arabic text)
- **Animations**: Subtle hover effects, gradient backgrounds

---

## 📁 Project Structure

```
ramadan-webservice-project/
├── backend/
│   ├── main.py                    # FastAPI application entry
│   ├── run_server.py              # Server runner with uvicorn
│   ├── routes_api.py              # All API routes with JWT auth
│   ├── models_extended.py         # SQLAlchemy models (User, Imam, Event...)
│   ├── database.py                # Database configuration
│   ├── services_dua.py            # Dua generation service (Groq AI)
│   ├── services_chat.py           # Chat service
│   ├── services_ai_analyzer.py    # AI analyzer with semantic search
│   ├── services_quran_semantic.py # Quran embedding & search
│   └── requirements.txt           # Python dependencies
├── app/schemas/frontend webservice site/
│   └── app.html                   # Main frontend application
├── start_frontend.py              # Frontend server launcher
├── requirements.txt               # Root dependencies
├── Dockerfile                     # Docker configuration
├── docker-compose.yml             # Docker Compose setup
├── PROJECT_HISTORY.md             # Development history
└── README.md                      # This file
```

---

## 🚀 Deployment

### Docker
```bash
docker-compose up --build
```

### Railway
1. Connect your GitHub repository
2. Set environment variables in Railway dashboard
3. Deploy automatically on push

### Render
1. Create a new Web Service
2. Connect repository
3. Set build command: `pip install -r backend/requirements.txt`
4. Set start command: `cd backend && python main.py`

---

## 📄 License

This project is licensed under the MIT License.

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📞 Contact

For questions or support, please open an issue on GitHub.

**Repository**: [github.com/cheehub213/ramadan-webservice-project-](https://github.com/cheehub213/ramadan-webservice-project-)

---

<div align="center">

**Made with ❤️ for the Muslim Ummah**

🌙 Ramadan Mubarak! 🌙

*© 2026 Ramadan Helper - All Rights Reserved*

</div>
