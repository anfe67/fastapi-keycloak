from functools import lru_cache
from pathlib import Path

from pydantic import ConfigDict
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="example_app_",
        env_file=Path(__file__).parent.parent / ".env",
        extra="ignore"
    )

    debug: bool = False
    host: str = "127.0.0.1"
    port: int = 8000

    cors_allow_origins: list[str] = [
        "http://localhost:8000",
        "http://127.0.0.1:8000",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
    ]
    context: str = "umm"

@lru_cache()
def get_settings():
    return Settings()