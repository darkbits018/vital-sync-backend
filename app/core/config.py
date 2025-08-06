# app/core/config.py
from functools import lru_cache
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    APP_ENV: str = Field("development", validation_alias="APP_ENV")
    DEBUG: bool = Field(True, validation_alias="DEBUG")

    FIREBASE_CREDENTIALS_PATH: str = Field(validation_alias="FIREBASE_CREDENTIALS_PATH")
    DATABASE_URL: str = Field(validation_alias="DATABASE_URL")

    SECRET_KEY: str = Field(validation_alias="SECRET_KEY")
    ALGORITHM: str = Field("HS256", validation_alias="ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(60, validation_alias="ACCESS_TOKEN_EXPIRE_MINUTES")

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "extra": "ignore"  # or "allow" if needed
    }


@lru_cache()
def get_settings():
    return Settings()
