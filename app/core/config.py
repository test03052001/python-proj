from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Enterprise Platform API"
    app_version: str = "0.1.0"
    debug: bool = True
    database_url: str = (
        "mysql+pymysql://root:root@localhost:3306/enterprise_platform?charset=utf8mb4"
    )

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


@lru_cache
def get_settings() -> Settings:
    return Settings()
