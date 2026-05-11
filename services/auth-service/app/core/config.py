import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "India Electoral Management Platform"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "CHANGEME_PROD_SECRET")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8 # 8 days
    
    # Production Security
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    SHOW_DOCS: bool = os.getenv("SHOW_DOCS", "False").lower() == "true"
    
    # ECI specific
    AGENCY_CODE: str = "ECI-INDIA"
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    
    class Config:
        case_sensitive = True

settings = Settings()
