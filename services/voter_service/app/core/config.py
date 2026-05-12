import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "National Voter Management System - Voter Service"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "CHANGEME_PROD_SECRET")
    ALGORITHM: str = "HS256"
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    
    def __init__(self, **values):
        super().__init__(**values)
        if not self.DATABASE_URL:
             from dotenv import load_dotenv
             load_dotenv()
             load_dotenv("../../.env")
             self.DATABASE_URL = os.getenv("DATABASE_URL")

    class Config:
        case_sensitive = True
        extra = "ignore"

settings = Settings()
