"""
app/core/config.py

Central configuration for the Mafilika Business Automation Suite backend.
All environment-dependent values (database URL, JWT secret, CORS origins, etc.)
are loaded here so the rest of the app never touches os.environ directly.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # --- App ---
    APP_NAME: str = "Mafilika Business Automation Suite"
    APP_ENV: str = "development"

    # --- Database ---
    DATABASE_URL: str

    # --- JWT ---
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # --- CORS ---
    # Comma-separated string in .env, split into a list here.
    CORS_ORIGINS: str = "http://localhost:5500"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    @property
    def cors_origins_list(self) -> list[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]


# Single shared settings instance used across the whole app
settings = Settings()
