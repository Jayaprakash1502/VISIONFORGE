import json
from functools import lru_cache
from typing import List, Union
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Centralized Application Configuration loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    # Project Identifiers
    PROJECT_NAME: str = "VISIONFORGE API"
    VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    LOG_LEVEL: str = "INFO"

    # API Configuration
    API_HOST: str = "127.0.0.1"
    API_PORT: int = 8000
    API_V1_PREFIX: str = "/api/v1"

    # Security & CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
    ]

    # Database Configuration (PostgreSQL / Supabase)
    DATABASE_URL: str = (
        "postgresql://visionforge_user:visionforge_password@localhost:5432/visionforge_db"
    )
    DB_CONNECT_TIMEOUT: int = 5
    DB_POOL_SIZE: int = 5
    DB_MAX_OVERFLOW: int = 10

    # Configurable AI & Analytics Thresholds (Phase 5+)
    AI_CONFIDENCE_THRESHOLD: float = 0.45
    AI_INFERENCE_FPS: int = 5
    CROWD_THRESHOLD_HIGH: int = 40
    LOITERING_THRESHOLD_SECONDS: int = 15
    EVENT_COOLDOWN_SECONDS: int = 10

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def parse_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        """Parse CORS origins if passed as JSON string or comma-separated string."""
        if isinstance(v, str):
            if v.startswith("[") and v.endswith("]"):
                try:
                    return json.loads(v)
                except json.JSONDecodeError:
                    pass
            return [origin.strip() for origin in v.split(",") if origin.strip()]
        return v


@lru_cache()
def get_settings() -> Settings:
    """Retrieve cached application settings instance."""
    return Settings()


settings = get_settings()
