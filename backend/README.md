#  Ramadan Helper API v2.0

A professional REST API for Islamic guidance and resources.

##  Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run the server
python main.py
```

Server runs at: `http://localhost:8000`
API Documentation: `http://localhost:8000/docs`

##  API Endpoints

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/signup` | Register new user |
| POST | `/api/auth/verify` | Verify email with 6-digit code |
| POST | `/api/auth/login` | User login |
| POST | `/api/auth/resend-code` | Resend verification code |
| POST | `/api/auth/forgot-password` | Request password reset |
| POST | `/api/auth/reset-password` | Reset password with code |

### Users
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/users/{email}` | Get user profile |
| PUT | `/api/users/{email}` | Update user profile |
| DELETE | `/api/users/{email}` | Delete user account |

### Dua
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/dua/categories` | Get all dua categories |
| POST | `/api/dua/generate` | Generate personalized dua |
| GET | `/api/dua/history/{email}` | Get user's dua history |
| POST | `/api/dua/feedback` | Submit dua feedback |

### Chat with Scholars
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/chat/imams` | Get available imams |
| GET | `/api/chat/imams/{id}` | Get imam details |
| POST | `/api/chat/conversations` | Start conversation |
| GET | `/api/chat/conversations/{email}` | Get user conversations |
| POST | `/api/chat/messages` | Send message |
| GET | `/api/chat/messages/{id}` | Get conversation messages |

### AI Analyzer
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/analyzer/analyze` | Get relevant Quran verses & Hadiths |
| GET | `/api/analyzer/topics` | Get available guidance topics |
| GET | `/api/analyzer/ayahs` | Get all Quran verses |
| GET | `/api/analyzer/hadiths` | Get all Hadiths |

### Videos
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/videos/search` | Search Islamic videos |

### Statistics
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/stats/dashboard` | Get platform statistics |
| GET | `/api/stats/user/{email}` | Get user statistics |

### System
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health` | Health check |

##  Configuration

Create a `.env` file:

```env
# AI Service (Groq)
GROQ_API_KEY=your_groq_api_key

# Email Service (Gmail)
EMAIL_ADDRESS=your_gmail@gmail.com
EMAIL_PASSWORD=your_app_password

# YouTube API
YOUTUBE_API_KEY=your_youtube_api_key
```

##  Project Structure

```
backend/
 main.py                 # Application entry point
 routes_api.py           # All API endpoints
 database.py             # Database configuration
 models_extended.py      # SQLAlchemy models
 services_ai_analyzer.py # AI Quran/Hadith analyzer
 services_chat.py        # Chat with scholars
 services_dua.py         # Dua generation
 services_email.py       # Email service
 services_youtube_ai.py  # YouTube video search
 requirements.txt        # Dependencies
 .env                    # Environment variables
```

##  Security

- Passwords are hashed using SHA256
- Email verification required for signup
- Password reset via email code

##  License

MIT License  2026 Ramadan Helper
