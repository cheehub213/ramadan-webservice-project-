# 🌙 Ramadan Helper - Islamic Web Application

A comprehensive Islamic web application that provides spiritual guidance, personalized duas, AI-powered Islamic Q&A, imam consultations, and Islamic video search.

![Python](https://img.shields.io/badge/Python-3.12-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-green)
![SQLite](https://img.shields.io/badge/Database-SQLite-orange)
![License](https://img.shields.io/badge/License-MIT-purple)

---

## 📌 Project Description

**Ramadan Helper** is a full-stack web application designed to support Muslims in their spiritual journey. The application combines Islamic scholarship with AI technology to provide:

- 🤖 **AI-Powered Islamic Q&A** - Ask questions and receive relevant Quran verses (Ayahs) and Hadiths with explanations
- 📿 **Personalized Dua Generator** - Generate custom duas in both English and Arabic based on your specific situation
- 💬 **Chat with Imams** - Real-time messaging system to consult with qualified Islamic scholars
- 📺 **Islamic Video Search** - AI-powered YouTube video recommendations based on your spiritual needs
- 📚 **User History Tracking** - Keep track of your spiritual journey and previous interactions

---

## 📌 Features List

### 🤖 AI Analyzer (Ask AI)
- Ask any Islamic question in natural language
- Receive relevant Quran verses with surah and verse numbers
- Get authentic Hadiths with source attribution
- AI-generated explanations tailored to your question
- Semantic search through 6,236+ Quran verses

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
- Imam dashboard for responding to inquiries
- Conversation history preserved

### 📺 Islamic Video Search
- AI-powered keyword extraction from natural language
- YouTube integration for video search
- Personalized video recommendations
- Video metadata including duration, channel, and thumbnails

### 👤 User Management
- Simple email-based authentication
- Separate login for users and imams
- User activity history tracking
- Session persistence

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
```

### Step 4: Set Up Environment Variables
Create a `.env` file in the `backend/` folder:
```env
# AI Service API Key (OpenRouter/Deepseek)
OPENROUTER_API_KEY=your_api_key_here

# YouTube API Key (optional - for video search)
YOUTUBE_API_KEY=your_youtube_api_key
```

### Step 5: Run the Backend Server
```bash
cd backend
python main.py
```
The API will be available at: `http://localhost:8000`

### Step 6: Open the Frontend
Open `app/schemas/frontend webservice site/app.html` in your browser, or serve it with:
```bash
# From project root
python -m http.server 8080
```
Then visit: `http://localhost:8080/app/schemas/frontend%20webservice%20site/app.html`

---

## 📌 API Endpoints Documentation

Base URL: `http://localhost:8000/api`

### 👤 User Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/users/login` | Login or register a user |
| `GET` | `/users/{email}` | Get user by email |

### 📿 Dua Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/dua/categories` | Get all dua categories |
| `POST` | `/dua/generate` | Generate a personalized dua |
| `GET` | `/dua/history/{email}` | Get user's dua history |
| `POST` | `/dua/feedback` | Submit feedback on a dua |

### 🕌 Imam Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/imams` | Get all available imams |
| `GET` | `/imams/{imam_id}` | Get specific imam details |

### 💬 Chat Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/chat/conversations` | Create new conversation |
| `GET` | `/chat/conversations/{user_email}` | Get user's conversations |
| `POST` | `/chat/messages` | Send a message |
| `GET` | `/chat/messages/{conversation_id}` | Get messages in conversation |
| `GET` | `/chat/imam/conversations/{imam_email}` | Get imam's conversations |
| `GET` | `/chat/all-conversations` | Get all conversations (admin) |
| `PUT` | `/chat/messages/{message_id}/read` | Mark message as read |

### 🤖 AI Analyzer Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/analyzer/analyze` | Analyze question with AI |
| `GET` | `/analyzer/ayahs` | Get all Quranic verses |
| `GET` | `/analyzer/hadiths` | Get all Hadiths |

### 📺 Video Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/videos` | Get all videos |
| `GET` | `/videos/{video_id}` | Get specific video |
| `GET` | `/videos/search?query=` | Search videos |
| `POST` | `/videos/search-by-prompt` | AI-powered video search |
| `POST` | `/videos/add` | Add new video |

### 📜 History Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/history/{user_email}` | Get user activity history |
| `POST` | `/history/log` | Log user action |

### ❤️ Health Check

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/health` | Check API health status |

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
│  🌙 Ramadan Helper                         [Home] [Ask AI]  │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│           Welcome to Ramadan Helper                         │
│     Your personal Islamic companion for duas,               │
│         guidance, and spiritual connection                  │
│                                                             │
│    [🤖 Ask AI]  [📿 Generate Dua]  [📺 Videos]  [💬 Chat]   │
│                                                             │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐       │
│  │ 🤖 Ask   │ │ 📿 Dua   │ │ 📺 Videos│ │ 💬 Chat  │       │
│  │    AI    │ │Generator │ │          │ │with Imam │       │
│  │          │ │          │ │          │ │          │       │
│  │ AI-power │ │Bilingual │ │ YouTube  │ │ Real     │       │
│  │ guidance │ │ duas     │ │ search   │ │ scholars │       │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘       │
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

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| **Backend** | FastAPI (Python) |
| **Database** | SQLite with SQLAlchemy ORM |
| **AI Service** | OpenRouter / Deepseek API |
| **Frontend** | HTML, TailwindCSS, Vanilla JS |
| **Video API** | YouTube Data API v3 |
| **Deployment** | Railway / Render / Docker |

---

## 📁 Project Structure

```
ramadan-webservice-project/
├── backend/
│   ├── main.py                    # FastAPI application entry
│   ├── routes_comprehensive.py    # All API routes
│   ├── models_extended.py         # SQLAlchemy models
│   ├── database.py                # Database configuration
│   ├── services_dua.py            # Dua generation service
│   ├── services_chat.py           # Chat service
│   ├── services_ai_analyzer.py    # AI analyzer service
│   ├── services_youtube_ai.py     # YouTube search service
│   └── requirements.txt           # Python dependencies
├── app/schemas/frontend webservice site/
│   ├── app.html                   # Main frontend application
│   └── config/                    # Frontend configuration
├── requirements.txt               # Root dependencies
├── Dockerfile                     # Docker configuration
├── docker-compose.yml             # Docker Compose setup
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

---

## 📞 Contact

For questions or support, please open an issue on GitHub.

---

**Made with ❤️ for the Muslim Ummah**
