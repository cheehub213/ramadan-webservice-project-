from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Database
    database_url: str = "postgresql://user:password@localhost:5432/ramadan_db"
    
    # Deepseek API
    deepseek_api_key: str
    deepseek_api_base_url: str = "https://api.deepseek.com/v1"
    
    # Server
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    debug: bool = False
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()
