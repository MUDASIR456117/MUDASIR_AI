import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent

class Settings(BaseSettings):
    PROJECT_NAME: str = "AI Financial Advisor"
    VERSION: str = "1.0.0"
    DEBUG: bool = True
    API_V1_STR: str = "/api/v1"

    # Database
    MONGODB_URI: str = "mongodb+srv://pathanmudasirali6_db_user:mk12345lk-42-9@mudasir.91bebio.mongodb.net/?retryWrites=true&w=majority&appName=mudasir"
    DATABASE_NAME: str = "ai_financial_advisor"

    # Security
    JWT_SECRET: str = "ai_financial_advisor_super_secure_jwt_secret_key_2026_change_in_production"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours

    # AI & External APIs
    AI_API_KEY: str = ""

    # File Uploads
    MAX_UPLOAD_SIZE_MB: int = 10
    UPLOAD_DIR: str = str(BASE_DIR / "uploads")
    MODELS_DIR: str = str(BASE_DIR / "models")

    # Host & Port
    BACKEND_HOST: str = "0.0.0.0"
    BACKEND_PORT: int = 8000
    FRONTEND_PORT: int = 8501

    model_config = SettingsConfigDict(
        env_file=str(BASE_DIR / ".env"),
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()

# Ensure directories exist
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
os.makedirs(settings.MODELS_DIR, exist_ok=True)
