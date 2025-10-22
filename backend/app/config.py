from pydantic import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    SECRET_KEY: str = "your-secret-key-change-in-production-min-32-chars-long"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 480
    DATABASE_PATH: str = "./data/app.db"
    DEFAULT_ADMIN_USERNAME: str = "adsadmin"
    DEFAULT_ADMIN_PASSWORD: str = "Mm123567"
    DEFAULT_WHATSAPP_URL: str = "https://api.whatsapp.com/send/?phone=14433589251&text=Hi"

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
