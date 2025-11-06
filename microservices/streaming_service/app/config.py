from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/videohub_db"
    
    # Media
    MEDIA_ROOT: str = ""
    
    # API
    API_V1_PREFIX: str = "/api/v1"
    PROJECT_NAME: str = "VideoHub Streaming Service"
    
    # CORS
    DJANGO_HOST: str = "http://localhost:8000"
    
    class Config:
        env_file = ".env"

settings = Settings()