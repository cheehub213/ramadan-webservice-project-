# 🌙 Ramadan Helper - RESTful API Technical Report

---

## Project Information

| Field | Value |
|-------|-------|
| **Project Name** | Ramadan Helper - Islamic Web Application |
| **Version** | 3.0 (Final Version) |
| **Author** | Chiheb Bahri |
| **Date** | January 14, 2026 |
| **Repository** | https://github.com/cheehub213/ramadan-webservice-project- |
| **License** | MIT |

---

## 1. Executive Summary

**Ramadan Helper** is a comprehensive full-stack Islamic web application designed to support Muslims in their spiritual journey during Ramadan and beyond. The application provides a RESTful API backend built with FastAPI (Python) that serves multiple services including AI-powered Islamic Q&A, personalized dua generation, real-time chat with Imams, Islamic video search, and a Ramadan events platform specifically for Tunisia.

The system implements industry-standard JWT (JSON Web Token) authentication with email verification, role-based access control (User, Imam, Admin), and follows REST architectural principles for scalable and maintainable API design.

---

## 2. Project Description

### 2.1 Purpose
The Ramadan Helper application aims to:
- Provide Muslims with easy access to Islamic knowledge through AI-powered search
- Generate personalized duas (supplications) in both Arabic and English
- Enable consultation with qualified Imams through a real-time messaging system
- Offer curated Islamic video content from YouTube
- Create a platform for discovering and posting Ramadan events across Tunisia

### 2.2 Target Audience
- Muslims seeking spiritual guidance during Ramadan
- Islamic scholars (Imams) providing online consultations
- Event organizers in Tunisia promoting Ramadan activities
- Administrators managing the platform

---

## 3. Technical Architecture

### 3.1 Technology Stack

| Layer | Technology | Version |
|-------|------------|---------|
| **Backend Framework** | FastAPI | 0.104.1 |
| **ASGI Server** | Uvicorn | 0.24.0 |
| **Database ORM** | SQLAlchemy | 2.0.23 |
| **Database** | SQLite | 3.x |
| **Authentication** | JWT (python-jose) | - |
| **Password Hashing** | bcrypt | 5.0.0 |
| **HTTP Client** | httpx | 0.25.2 |
| **AI Service** | Groq API | 0.4.2 |
| **Data Validation** | Pydantic | 2.5.2 |
| **Environment** | python-dotenv | 1.0.0 |
| **Frontend** | HTML5, TailwindCSS, JavaScript | - |

### 3.2 Architecture Pattern

```
┌─────────────────────────────────────────────────────────────┐
│                      Frontend (HTML/JS)                     │
│                    http://localhost:8080                    │
└─────────────────────────┬───────────────────────────────────┘
                          │ HTTP/REST
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                   FastAPI Application                        │
│                    http://localhost:8000                    │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │   Routes    │  │  Services   │  │    Middleware       │  │
│  │  (7 modules)│  │ (AI, Email) │  │  (CORS, Auth)       │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
├─────────────────────────────────────────────────────────────┤
│                     SQLAlchemy ORM                          │
├─────────────────────────────────────────────────────────────┤
│                    SQLite Database                          │
│                   (ramadan_app.db)                          │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                   External Services                         │
│  ┌───────────────┐  ┌───────────────┐  ┌────────────────┐  │
│  │   Groq AI     │  │   YouTube     │  │  SMTP Email    │  │
│  │   (LLM API)   │  │   Data API    │  │  (Gmail)       │  │
│  └───────────────┘  └───────────────┘  └────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### 3.3 Project Structure

```
ramadan-webservice-project-/
├── backend/
│   ├── main.py                    # FastAPI application entry point
│   ├── database.py                # SQLAlchemy database configuration
│   ├── models_extended.py         # SQLAlchemy ORM models (10 models)
│   ├── requirements.txt           # Python dependencies
│   ├── routes/
│   │   ├── __init__.py           # Route aggregator
│   │   ├── auth.py               # Authentication endpoints (16 endpoints)
│   │   ├── dua.py                # Dua generator endpoints (4 endpoints)
│   │   ├── chat.py               # Imam chat endpoints (7 endpoints)
│   │   ├── analyzer.py           # AI analyzer endpoints (3 endpoints)
│   │   ├── events.py             # Events endpoints (5 endpoints)
│   │   ├── videos.py             # Video search endpoints (3 endpoints)
│   │   └── admin.py              # Admin panel endpoints (18 endpoints)
│   ├── schemas/
│   │   ├── auth.py               # Authentication Pydantic schemas
│   │   ├── dua.py                # Dua Pydantic schemas
│   │   ├── chat.py               # Chat Pydantic schemas
│   │   ├── events.py             # Events Pydantic schemas
│   │   └── videos.py             # Video Pydantic schemas
│   ├── services/
│   │   └── email_service.py      # SMTP email service
│   ├── services_ai_analyzer.py   # Groq AI integration
│   ├── services_dua.py           # Dua generation service
│   ├── services_chat.py          # Chat service
│   └── services_youtube_ai.py    # YouTube search service
├── app/schemas/frontend webservice site/
│   └── app.html                  # Single-page frontend application
└── README.md                     # Project documentation
```

---

## 4. Database Design

### 4.1 Entity-Relationship Diagram

```
┌──────────────────┐       ┌──────────────────┐
│      Users       │       │      Imams       │
├──────────────────┤       ├──────────────────┤
│ id (PK)          │       │ id (PK)          │
│ email            │       │ name             │
│ name             │       │ email            │
│ password_hash    │       │ expertise        │
│ user_type        │       │ is_available     │
│ is_verified      │       │ phone            │
│ is_active        │       │ bio              │
│ last_login       │       │ created_at       │
│ login_attempts   │       └────────┬─────────┘
│ locked_until     │                │
│ created_at       │                │
│ updated_at       │                │
└────────┬─────────┘                │
         │                          │
         │ 1:N                      │ 1:N
         ▼                          ▼
┌──────────────────┐       ┌──────────────────┐
│   DuaHistory     │       │  Conversations   │
├──────────────────┤       ├──────────────────┤
│ id (PK)          │       │ id (PK)          │
│ user_id (FK)     │       │ user_id (FK)     │
│ email            │       │ user_email       │
│ category         │       │ imam_id (FK)     │
│ context          │       │ topic            │
│ dua_text_en      │       │ created_at       │
│ dua_text_ar      │       │ updated_at       │
│ how_to_use_en    │       └────────┬─────────┘
│ how_to_use_ar    │                │
│ helpful          │                │ 1:N
│ feedback_notes   │                ▼
│ created_at       │       ┌──────────────────┐
└──────────────────┘       │    Messages      │
                           ├──────────────────┤
┌──────────────────┐       │ id (PK)          │
│     Events       │       │ conversation_id  │
├──────────────────┤       │ imam_id (FK)     │
│ id (PK)          │       │ sender_type      │
│ title            │       │ sender_email     │
│ description      │       │ message_text     │
│ city             │       │ is_read          │
│ location         │       │ created_at       │
│ category         │       └──────────────────┘
│ event_date       │
│ start_time       │       ┌──────────────────┐
│ end_time         │       │  TokenBlacklist  │
│ organizer_name   │       ├──────────────────┤
│ organizer_contact│       │ id (PK)          │
│ is_verified      │       │ token_jti        │
│ is_featured      │       │ user_email       │
│ created_at       │       │ token_type       │
└──────────────────┘       │ expires_at       │
                           │ blacklisted_at   │
┌──────────────────┐       └──────────────────┘
│   AIAnalysis     │
├──────────────────┤       ┌──────────────────┐
│ id (PK)          │       │ EmailVerification│
│ user_email       │       │     Token        │
│ question         │       ├──────────────────┤
│ ayah (JSON)      │       │ id (PK)          │
│ hadith (JSON)    │       │ user_email       │
│ explanation      │       │ token            │
│ created_at       │       │ expires_at       │
└──────────────────┘       │ used             │
                           │ created_at       │
                           └──────────────────┘
```

### 4.2 Database Models Summary

| Model | Description | Key Fields |
|-------|-------------|------------|
| **User** | Application users (user/imam/admin) | email, password_hash, user_type, is_verified |
| **Imam** | Islamic scholars for consultations | name, expertise, is_available, bio |
| **DuaHistory** | Generated duas history | category, dua_text_en, dua_text_ar |
| **Conversation** | Chat threads between users and imams | user_id, imam_id, topic |
| **Message** | Individual chat messages | sender_type, message_text, is_read |
| **Event** | Ramadan events in Tunisia | title, city, category, is_featured |
| **AIAnalysis** | AI-powered question analyses | question, ayah, hadith, explanation |
| **TokenBlacklist** | Revoked JWT tokens | token_jti, expires_at |
| **EmailVerificationToken** | Email verification codes | token, expires_at, used |
| **PasswordResetToken** | Password reset tokens | token, expires_at, used |

---

## 5. API Endpoints Documentation

### 5.1 Authentication Endpoints (`/api/auth`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/signup` | Register new user account | ❌ |
| POST | `/verify-email` | Verify email with 6-digit code | ❌ |
| POST | `/resend-verification` | Resend verification email | ❌ |
| POST | `/token` | OAuth2 token login (form data) | ❌ |
| POST | `/login` | JSON login endpoint | ❌ |
| POST | `/refresh` | Refresh access token | 🔒 |
| POST | `/logout` | Logout and blacklist tokens | 🔒 |
| GET | `/me` | Get current user profile | 🔒 |
| PUT | `/me` | Update current user profile | 🔒 |
| POST | `/change-password` | Change user password | 🔒 |
| POST | `/forgot-password` | Request password reset email | ❌ |
| POST | `/reset-password` | Reset password with token | ❌ |
| GET | `/verify-token` | Verify if token is valid | 🔒 |
| GET | `/users` | List all users (admin only) | 🔒 Admin |
| PUT | `/users/{id}/deactivate` | Deactivate user account | 🔒 Admin |
| PUT | `/users/{id}/activate` | Activate user account | 🔒 Admin |

### 5.2 Dua Generator Endpoints (`/api/dua`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/categories` | Get available dua categories | ❌ |
| POST | `/generate` | Generate personalized dua | ❌ |
| GET | `/history/{email}` | Get user's dua history | ❌ |
| POST | `/feedback/{dua_id}` | Submit feedback on dua | ❌ |

**Dua Categories:**
- Fear & Anxiety
- Financial Hardship
- Health Issues
- Family Problems
- Career Guidance
- Spiritual Growth
- Relationship Issues

### 5.3 Chat with Imam Endpoints (`/api/chat`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/imams` | List available imams | ❌ |
| POST | `/conversations` | Create new conversation | 🔒 |
| GET | `/conversations/{email}` | Get user's conversations | ❌ |
| GET | `/imam-conversations/{email}` | Get imam's conversations | 🔒 Imam |
| GET | `/all-conversations` | Get all conversations (admin) | 🔒 Admin |
| POST | `/messages` | Send a message | 🔒 |
| GET | `/messages/{conversation_id}` | Get conversation messages | ❌ |

### 5.4 AI Analyzer Endpoints (`/api/analyzer`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/` | Analyze Islamic question | ❌ |
| POST | `/analyze` | Analyze with Quran verses | ❌ |
| POST | `/semantic-search` | Semantic search in Quran | ❌ |

**Features:**
- Semantic search through 6,236+ Quran verses
- AI-powered explanation using Groq LLM
- Hadith references
- Similarity scoring for verse relevance

### 5.5 Events Endpoints (`/api/events`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/cities` | Get 24 Tunisian cities | ❌ |
| GET | `/categories` | Get event categories | ❌ |
| POST | `/` | Create new event | 🔒 |
| GET | `/` | List all events | ❌ |
| GET | `/{event_id}` | Get event details | ❌ |
| DELETE | `/{event_id}` | Delete event | 🔒 |

**Supported Cities (24 Tunisian Governorates):**
Tunis, Ariana, Ben Arous, Manouba, Nabeul, Zaghouan, Bizerte, Béja, Jendouba, Kef, Siliana, Sousse, Monastir, Mahdia, Sfax, Kairouan, Kasserine, Sidi Bouzid, Gabès, Medenine, Tataouine, Gafsa, Tozeur, Kebili

**Event Categories:**
Iftar, Tarawih, Lecture, Charity, Quran Study, Community, Youth, Sisters, Family, Sports, Other

### 5.6 Video Search Endpoints (`/api/videos`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/search` | Search YouTube for Islamic videos | ❌ |
| POST | `/search-by-prompt` | AI-powered keyword extraction | ❌ |
| GET | `/curated` | Get curated video list | ❌ |

### 5.7 Admin Panel Endpoints (`/api/admin`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/users` | List all users with filters | 🔒 Admin |
| GET | `/users/{id}` | Get user details | 🔒 Admin |
| PUT | `/users/{id}/role` | Change user role | 🔒 Admin |
| PUT | `/users/{id}/activate` | Activate user | 🔒 Admin |
| PUT | `/users/{id}/deactivate` | Deactivate user | 🔒 Admin |
| DELETE | `/users/{id}` | Delete user | 🔒 Admin |
| POST | `/users/create-admin` | Create admin account | 🔒 Admin |
| GET | `/imams` | List all imams | 🔒 Admin |
| POST | `/imams` | Create new imam | 🔒 Admin |
| PUT | `/imams/{id}` | Update imam | 🔒 Admin |
| DELETE | `/imams/{id}` | Delete imam | 🔒 Admin |
| GET | `/events` | List all events | 🔒 Admin |
| PUT | `/events/{id}/verify` | Verify event | 🔒 Admin |
| PUT | `/events/{id}/unverify` | Unverify event | 🔒 Admin |
| DELETE | `/events/{id}` | Delete event | 🔒 Admin |
| GET | `/stats` | Get platform statistics | 🔒 Admin |
| POST | `/seed-admin` | Seed initial admin | ❌ |

---

## 6. Security Implementation

### 6.1 Authentication Flow

```
┌─────────────┐      ┌─────────────┐      ┌─────────────┐
│   Client    │      │   FastAPI   │      │   Database  │
└──────┬──────┘      └──────┬──────┘      └──────┬──────┘
       │                    │                    │
       │  1. POST /signup   │                    │
       │ ──────────────────>│                    │
       │                    │  2. Hash password  │
       │                    │  3. Create user    │
       │                    │ ──────────────────>│
       │                    │  4. Send email     │
       │  5. Verification   │                    │
       │     required       │                    │
       │ <──────────────────│                    │
       │                    │                    │
       │ 6. POST /verify    │                    │
       │ ──────────────────>│                    │
       │                    │  7. Verify token   │
       │                    │ ──────────────────>│
       │  8. User verified  │                    │
       │ <──────────────────│                    │
       │                    │                    │
       │  9. POST /login    │                    │
       │ ──────────────────>│                    │
       │                    │ 10. Verify creds   │
       │                    │ ──────────────────>│
       │ 11. JWT Tokens     │                    │
       │ <──────────────────│                    │
       │                    │                    │
       │ 12. Request + JWT  │                    │
       │ ──────────────────>│                    │
       │                    │ 13. Validate JWT   │
       │ 14. Protected data │                    │
       │ <──────────────────│                    │
```

### 6.2 JWT Token Structure

**Access Token (30 minutes expiry):**
```json
{
  "sub": "user@example.com",
  "user_type": "user",
  "exp": 1736884800,
  "iat": 1736883000,
  "jti": "uuid-v4-token-id",
  "type": "access"
}
```

**Refresh Token (7 days expiry):**
```json
{
  "sub": "user@example.com",
  "user_type": "user",
  "exp": 1737489600,
  "iat": 1736884800,
  "jti": "uuid-v4-token-id",
  "type": "refresh"
}
```

### 6.3 Security Features

| Feature | Implementation |
|---------|----------------|
| **Password Hashing** | bcrypt with salt |
| **Token Type** | JWT Bearer tokens |
| **Token Expiry** | Access: 30min, Refresh: 7 days |
| **Token Revocation** | Blacklist table with JTI |
| **Email Verification** | 6-digit code, 24h expiry |
| **Brute Force Protection** | Account lockout after 5 attempts |
| **Lockout Duration** | 15 minutes |
| **CORS** | Configured for cross-origin requests |
| **Role-Based Access** | User, Imam, Admin roles |

---

## 7. API Request/Response Examples

### 7.1 User Signup

**Request:**
```http
POST /api/auth/signup
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "SecurePass123!",
  "name": "Ahmad"
}
```

**Response (200 OK):**
```json
{
  "message": "Verification email sent. Please check your inbox.",
  "email": "user@example.com",
  "requires_verification": true,
  "demo_token": null
}
```

### 7.2 User Login

**Request:**
```http
POST /api/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "SecurePass123!"
}
```

**Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 1800,
  "user": {
    "email": "user@example.com",
    "name": "Ahmad",
    "user_type": "user",
    "is_verified": true
  }
}
```

### 7.3 Generate Dua

**Request:**
```http
POST /api/dua/generate
Content-Type: application/json

{
  "category": "health",
  "context": "I am struggling with anxiety and seeking peace",
  "email": "user@example.com"
}
```

**Response (200 OK):**
```json
{
  "id": 1,
  "category": "health",
  "context": "I am struggling with anxiety and seeking peace",
  "dua_text_en": "O Allah, I seek refuge in You from anxiety and sorrow...",
  "dua_text_ar": "اللَّهُمَّ إِنِّي أَعُوذُ بِكَ مِنَ الْهَمِّ وَالْحَزَنِ...",
  "how_to_use_en": "Recite this dua after every prayer...",
  "how_to_use_ar": "اقرأ هذا الدعاء بعد كل صلاة...",
  "created_at": "2026-01-14T12:00:00"
}
```

### 7.4 Create Event

**Request:**
```http
POST /api/events
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json

{
  "title": "Community Iftar",
  "description": "Join us for a community iftar gathering",
  "city": "Tunis",
  "location": "Mosque Al-Zaytuna",
  "category": "iftar",
  "event_date": "2026-03-15",
  "start_time": "18:30",
  "organizer_name": "Islamic Center",
  "organizer_contact": "+216 71 123 456",
  "is_featured": false
}
```

**Response (200 OK):**
```json
{
  "id": 1,
  "title": "Community Iftar",
  "description": "Join us for a community iftar gathering",
  "city": "Tunis",
  "location": "Mosque Al-Zaytuna",
  "category": "iftar",
  "event_date": "2026-03-15",
  "start_time": "18:30",
  "organizer_name": "Islamic Center",
  "is_verified": false,
  "is_featured": false,
  "created_at": "2026-01-14T12:00:00"
}
```

### 7.5 AI Analysis

**Request:**
```http
POST /api/analyzer/analyze
Content-Type: application/json

{
  "question": "What does Islam say about patience?",
  "email": "user@example.com"
}
```

**Response (200 OK):**
```json
{
  "question": "What does Islam say about patience?",
  "ayah": {
    "surah": "Al-Baqarah",
    "surah_number": 2,
    "verse_number": 153,
    "arabic": "يَا أَيُّهَا الَّذِينَ آمَنُوا اسْتَعِينُوا بِالصَّبْرِ وَالصَّلَاةِ...",
    "english": "O you who believe! Seek help through patience and prayer...",
    "similarity_score": 0.89
  },
  "explanation": "This verse emphasizes the importance of patience (sabr) in Islam..."
}
```

---

## 8. Events Monetization Model

### 8.1 Pricing Structure (Tunisia)

| Listing Type | Price | Features |
|--------------|-------|----------|
| **Basic** | 20 TND | Standard listing in search results |
| **Featured** | 50 TND | Premium placement, highlighted, top of results |

### 8.2 Event Categories

| Category | Emoji | Description |
|----------|-------|-------------|
| Iftar | 🍽️ | Evening meal gatherings |
| Tarawih | 🕌 | Night prayers during Ramadan |
| Lecture | 📚 | Islamic educational sessions |
| Charity | 💝 | Donation and volunteer events |
| Quran Study | 📖 | Quran reading and memorization |
| Community | 👥 | General community gatherings |
| Youth | 🌟 | Youth-focused activities |
| Sisters | 👩 | Women-only events |
| Family | 👨‍👩‍👧‍👦 | Family-friendly activities |
| Sports | ⚽ | Sports and fitness events |
| Other | ✨ | Miscellaneous events |

---

## 9. External Services Integration

### 9.1 Groq AI (LLM Service)

- **Purpose:** AI-powered dua generation and Islamic Q&A
- **Model:** LLaMA-based models via Groq API
- **Features:** 
  - Bilingual output (Arabic/English)
  - Context-aware dua generation
  - Quran verse explanation
- **Fallback:** Intelligent fallback when API unavailable

### 9.2 YouTube Data API

- **Purpose:** Islamic video search and recommendations
- **Features:**
  - Keyword-based search
  - AI-powered keyword extraction from natural language
  - Video metadata retrieval

### 9.3 SMTP Email Service

- **Purpose:** Email verification and notifications
- **Provider:** Gmail SMTP
- **Features:**
  - Email verification codes
  - Password reset emails
  - Welcome emails

---

## 10. Installation & Deployment

### 10.1 Prerequisites

- Python 3.10+
- pip (Python package manager)
- Git

### 10.2 Installation Steps

```bash
# 1. Clone repository
git clone https://github.com/cheehub213/ramadan-webservice-project-.git
cd ramadan-webservice-project-

# 2. Create virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# 3. Install dependencies
cd backend
pip install -r requirements.txt

# 4. Configure environment
# Create .env file with:
# GROQ_API_KEY=your_api_key
# SMTP_USER=your_email
# SMTP_PASSWORD=your_app_password

# 5. Run backend
python main.py

# 6. Run frontend (new terminal)
cd "app/schemas/frontend webservice site"
python -m http.server 8080
```

### 10.3 Access Points

| Service | URL |
|---------|-----|
| Backend API | http://localhost:8000 |
| API Documentation (Swagger) | http://localhost:8000/docs |
| API Documentation (ReDoc) | http://localhost:8000/redoc |
| Frontend Application | http://localhost:8080/app.html |

---

## 11. Testing

### 11.1 API Testing with Swagger UI

Access `http://localhost:8000/docs` for interactive API testing:

1. Click "Authorize" button
2. Enter Bearer token from login response
3. Test protected endpoints with authentication

### 11.2 Test Files

| File | Purpose |
|------|---------|
| `test_simple_app.py` | Basic endpoint tests |
| `test_bilingual_api.py` | Bilingual dua tests |
| `test_chat_dua.py` | Chat and dua integration tests |
| `test_semantic_search.py` | AI semantic search tests |
| `test_imam_registration.py` | Imam workflow tests |

---

## 12. Error Handling

### 12.1 HTTP Status Codes

| Code | Meaning | Example |
|------|---------|---------|
| 200 | Success | Request completed |
| 201 | Created | Resource created |
| 400 | Bad Request | Invalid input |
| 401 | Unauthorized | Invalid/missing token |
| 403 | Forbidden | Insufficient permissions |
| 404 | Not Found | Resource doesn't exist |
| 422 | Validation Error | Invalid data format |
| 500 | Server Error | Internal error |

### 12.2 Error Response Format

```json
{
  "detail": "Error message description"
}
```

---

## 13. Conclusion

The Ramadan Helper RESTful API provides a comprehensive backend solution for Islamic spiritual guidance applications. Key achievements include:

- **56+ API endpoints** across 7 route modules
- **10 database models** with proper relationships
- **JWT authentication** with email verification
- **Role-based access control** (User, Imam, Admin)
- **AI integration** for personalized Islamic content
- **Events platform** for Tunisia's 24 governorates
- **RESTful design** following industry standards

The application successfully combines traditional Islamic knowledge with modern technology to provide accessible spiritual guidance to Muslims worldwide.

---

## 14. References

1. FastAPI Documentation - https://fastapi.tiangolo.com/
2. SQLAlchemy Documentation - https://docs.sqlalchemy.org/
3. Pydantic Documentation - https://docs.pydantic.dev/
4. JWT RFC 7519 - https://tools.ietf.org/html/rfc7519
5. Groq AI API - https://console.groq.com/docs
6. REST API Design Best Practices - https://restfulapi.net/

---

**Report Generated:** January 14, 2026  
**Version:** Final Version  
**Author:** Chiheb Bahri
