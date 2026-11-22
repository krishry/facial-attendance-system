"""Application configuration management using Pydantic Settings."""

from sqlalchemy.engine import URL
from functools import lru_cache
from typing import List, Optional
from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables and .env file."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Application Information
    PROJECT_NAME: str = "Facial Recognition Attendance System"
    VERSION: str = "0.1.0"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    LOG_LEVEL: str = "INFO"

    # Server Networking
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    API_V1_STR: str = "/api/v1"

    # CORS Settings (comma-separated string in env, parsed to list)
    ALLOWED_ORIGINS: str = "http://localhost:3000,http://127.0.0.1:3000"

    @computed_field
    @property
    def cors_origins(self) -> List[str]:
        """Parse comma-separated ALLOWED_ORIGINS into a list."""
        if not self.ALLOWED_ORIGINS:
            return []
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",") if origin.strip()]

    # Database Configuration (PostgreSQL)
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "attendance_db"
    DATABASE_URL: Optional[str] = None

    @computed_field
    @property
    def async_database_uri(self) -> str:
        if self.DATABASE_URL:
            url = self.DATABASE_URL
            if url.startswith("postgresql://"):
                url = url.replace("postgresql://", "postgresql+asyncpg://", 1)
            elif url.startswith("postgresql+psycopg2://"):
                url = url.replace("postgresql+psycopg2://", "postgresql+asyncpg://", 1)
            return url

        return URL.create(
            drivername="postgresql+asyncpg",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_SERVER,
            port=self.POSTGRES_PORT,
            database=self.POSTGRES_DB,
        ).render_as_string(hide_password=False)

    @computed_field
    @property
    def sync_database_uri(self) -> str:
        if self.DATABASE_URL:
            url = self.DATABASE_URL
            if url.startswith("postgresql+asyncpg://"):
                url = url.replace("postgresql+asyncpg://", "postgresql+psycopg2://", 1)
            elif url.startswith("postgresql://"):
                url = url.replace("postgresql://", "postgresql+psycopg2://", 1)
            return url

        return URL.create(
            drivername="postgresql+psycopg2",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_SERVER,
            port=self.POSTGRES_PORT,
            database=self.POSTGRES_DB,
        ).render_as_string(hide_password=False)


    # Biometric / ML Configuration (InsightFace: SCRFD + ArcFace)
    INSIGHTFACE_MODEL_NAME: str = "buffalo_sc"
    DETECTION_CONFIDENCE_THRESHOLD: float = 0.60
    DETECTION_INPUT_SIZE: int = 640
    USE_GPU: bool = True
    FACE_SIMILARITY_THRESHOLD: float = 0.60
    FAISS_INDEX_PATH: str = "models/faiss.index"

    # Real-Time Camera & Tracking Configuration
    CAMERA_INDEX: int = 0
    CAMERA_FPS: int = 30
    CAMERA_WIDTH: int = 1280
    CAMERA_HEIGHT: int = 720
    TRACKER_IOU_THRESHOLD: float = 0.30
    TRACKER_MAX_LOST_FRAMES: int = 15
    RECOGNITION_INTERVAL_FRAMES: int = 10
    TEMPORAL_WINDOW_SIZE: int = 5
    TEMPORAL_MIN_CONFIRMATIONS: int = 3

    # Attendance Engine Configuration
    ATTENDANCE_MIN_SIMILARITY: float = 0.60
    ATTENDANCE_MIN_CONFIRMATIONS: int = 3
    ATTENDANCE_REQUIRE_ACTIVE_SESSION: bool = True
    ATTENDANCE_REQUIRE_ACTIVE_STUDENT: bool = True

    # Anti-Spoofing & Liveness Detection Configuration
    LIVENESS_ENABLED: bool = True
    LIVENESS_METHOD: str = "heuristic"  # "heuristic", "challenge_response", "disabled", "model"
    LIVENESS_MIN_SCORE: float = 0.50
    LIVENESS_STRICT_MODE: bool = False  # If True, rejects attendance when is_live is None or False
    LIVENESS_REQUIRED_FRAMES: int = 5  # Temporal frames needed to verify dynamic cues
    LIVENESS_POSE_VARIANCE_THRESHOLD: float = 0.015  # Minimum landmark pose variance to reject static photos
    LIVENESS_BLINK_EAR_THRESHOLD: float = 0.20  # Eye patch difference threshold for blink detection
    LIVENESS_LOG_EVALUATIONS: bool = True  # Log liveness decisions for auditing
    LIVENESS_LOG_PATH: str = "logs/liveness_audit.log"


@lru_cache()
def get_settings() -> Settings:
    """Return a cached instance of application settings."""
    return Settings()


# Global settings instance for convenient imports
settings = get_settings()
