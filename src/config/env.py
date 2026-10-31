from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    SECRET_KEY: SecretStr
    DEBUG: bool
    ALLOWED_HOSTS: list[str]
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: SecretStr
    DB_HOST: str
    DB_PORT: int

    model_config = SettingsConfigDict(
        env_file=".env", env_file_depth=2, env_file_encoding="utf-8", extra="ignore"
    )


config = Settings()
