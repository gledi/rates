from pydantic import BaseSettings, Field

from rates.utils import Environment


class Settings(BaseSettings):
    environment: Environment = Field(Environment.production, env="ENVIRONMENT")
    db_url: str = Field(..., env="DATABASE_URL")
    db_migrations_url: str | None = Field(env="DATABASE_MIGRATIONS_URL")


settings = Settings()
