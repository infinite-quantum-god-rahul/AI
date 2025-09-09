from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    # Database settings
    database_url: str = "sqlite:///./resume_analyzer.db"
    
    # JWT settings
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # File upload settings
    max_file_size: int = 10 * 1024 * 1024  # 10MB
    allowed_file_types: list = [".pdf", ".docx", ".doc"]
    upload_directory: str = "uploads"
    
    # AI Model settings
    spacy_model: str = "en_core_web_sm"
    similarity_threshold: float = 0.7
    
    # External API settings
    job_api_key: Optional[str] = None
    job_api_url: str = "https://api.example.com/jobs"
    
    # Redis settings (for caching)
    redis_url: str = "redis://localhost:6379"
    
    # Email settings
    smtp_server: str = "smtp.gmail.com"
    smtp_port: int = 587
    smtp_username: Optional[str] = None
    smtp_password: Optional[str] = None
    
    # Security settings
    cors_origins: list = ["http://localhost:3000", "https://your-domain.com"]
    
    # Rate limiting
    rate_limit_requests: int = 100
    rate_limit_window: int = 3600  # 1 hour
    
    class Config:
        env_file = ".env"
        case_sensitive = False

# Create settings instance
settings = Settings()

# Ensure upload directory exists
os.makedirs(settings.upload_directory, exist_ok=True)
