from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # Supabase Configuration
    supabase_url: str
    supabase_key: str

    # Security
    secret_key: str

    # API Configuration
    api_v1_prefix: str = "/api/v1"
    project_name: str = "Efiko"

    # Vector Search Configuration
    vector_similarity_threshold: float = 0.7
    max_search_results: int = 5

    # Document Processing
    max_document_size: int = 10485760  # 10MB in bytes

    # Gemini Configuration
    gemini_api_key: str

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings() -> Settings:
    return Settings()