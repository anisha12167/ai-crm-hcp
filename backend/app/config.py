from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    DATABASE_URL: str
    GROQ_API_KEY: str
    LLM_MODEL: str = "gemma2-9b-it"
    LLM_FALLBACK_MODEL: str = "llama-3.3-70b-versatile"

    class Config:
        env_file = ".env"

settings = Settings()
