from pydantic_settings import BaseSettings
from typing import Optional
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Random Forest Prediction API"
    
    # Model settings
    MODEL_PATH: str = os.getenv("MODEL_PATH", "models/modelo_random_forest.pkl")
    
    # API settings
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    class Config:
        case_sensitive = True

settings = Settings() 