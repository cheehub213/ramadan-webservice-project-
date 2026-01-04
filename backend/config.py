from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    # Database
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/ramadan_db")
    
    # YouTube API
    YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY", "")
    
    # FastAPI
    API_TITLE = "Ramadan Helper API"
    API_VERSION = "1.0.0"
    DEBUG = os.getenv("DEBUG", "True") == "True"
    
    # CORS
    ALLOWED_ORIGINS = [
        "http://localhost:3000",
        "http://localhost:8000",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8000",
        "file://",
    ]

settings = Settings()
