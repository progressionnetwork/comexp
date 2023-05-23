import os
from functools import lru_cache
from pathlib import Path

from kombu import Queue
from pydantic import BaseSettings
from user.models import User

DEBUG = True


class Settings(BaseSettings):
    user_model = User
    database_url: str
    database_sync_url: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    refresh_token_expire_minutes: int
    celery_broker_url: str
    celery_result_backend: str
    files_path: str = str(Path(Path(__file__).parent, "files", "data"))

    class Config:
        env_file = "env/dev" if DEBUG else "env/prod"


@lru_cache()
def get_settings():
    return Settings()
