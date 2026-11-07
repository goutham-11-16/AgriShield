import os
from typing import Optional
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "AgriShield"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = "agrishield-super-secret-key-change-in-production-min-32-chars"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 # 24 hours
    
    # Database
    DATABASE_URL: str = "sqlite+aiosqlite:///./agrishield.db"
    
    # External APIs
    DATA_GOV_IN_API_KEY: Optional[str] = None
    OPEN_METEO_API_KEY: Optional[str] = None
    BHASHINI_USER_ID: Optional[str] = None
    BHASHINI_API_KEY: Optional[str] = None
    BHASHINI_PIPELINE_ID: Optional[str] = None
    
    # Regional defaults
    PILOT_STATE: str = "Tamil Nadu"
    PILOT_DEFAULT_DISTRICT: str = "Dindigul"
    DEFAULT_LOCALE: str = "ta"
    
    # Storage
    STORAGE_LOCAL_DIR: str = "./uploads"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"

settings = Settings()
