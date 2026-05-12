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
    
    def __init__(self, **values):
        super().__init__(**values)
        if not self.DATABASE_URL:
             # Try loading manually if Pydantic didn't pick it up
             from dotenv import load_dotenv
             load_dotenv()
             load_dotenv("../../.env")
             self.DATABASE_URL = os.getenv("DATABASE_URL")
             if not self.DATABASE_URL:
                 raise ValueError("DATABASE_URL environment variable is not set")
    
    class Config:
        case_sensitive = True
        env_file = ".env"
        extra = "ignore"

settings = Settings()

