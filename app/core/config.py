from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Deployment & Security
    API_KEY: str  # The x-api-key YOU define for GUVI to use
    PORT: int = 8000
    ENVIRONMENT: str = "dev"
    
    # AI Providers
    GROQ_API_KEY: str
    
    # Data Store (Railway provides REDIS_URL)
    REDIS_URL: str
    
    # Callback
    GUVI_CALLBACK_URL: str = "https://hackathon.guvi.in/api/updateHoneyPotFinalResult"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()