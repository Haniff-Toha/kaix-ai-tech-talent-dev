"""
Kaix — Application settings.

All configuration is loaded from environment variables via pydantic-settings.
Copy .env.example to .env and fill in the values.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # ─── App ───
    app_env: str = "development"
    app_debug: bool = True
    app_host: str = "0.0.0.0"
    app_port: int = 8000

    # ─── Database ───
    database_url: str = "postgresql+asyncpg://user:pass@localhost:5432/db"

    # ─── Supabase Auth ───
    supabase_url: str = ""
    supabase_anon_key: str = ""
    supabase_jwt_secret: str = ""

    # ─── NVIDIA NIM (Reasoning — primary) ───
    nvidia_api_key: str = ""
    nvidia_base_url: str = "https://integrate.api.nvidia.com/v1"
    nvidia_model: str = "minimaxai/minimax-m2.7"

    # ─── Groq (Reasoning fallback + Fast + Vision) ───
    groq_api_key: str = ""
    groq_base_url: str = "https://api.groq.com/openai/v1"
    groq_reasoning_model: str = "openai/gpt-oss-120b"
    groq_fast_model: str = "google/gemma-3-27b-it"
    groq_vision_model: str = "meta-llama/llama-4-scout-17b-16e-instruct"

    # ─── Google Gemini (Embeddings) ───
    gemini_api_key: str = ""
    gemini_embedding_model: str = "gemini-embedding-2-preview"

    # ─── Embedding Config ───
    embedding_dimension: int = 768

    # ─── YouTube Data API ───
    youtube_api_key: str = ""  # Falls back to gemini_api_key if empty

    # ─── Email — Brevo (primary) ───
    brevo_smtp_host: str = "smtp-relay.brevo.com"
    brevo_smtp_port: int = 587
    brevo_smtp_login: str = ""
    brevo_smtp_key: str = ""
    brevo_api_key: str = ""
    email_from: str = "Kaix <kaix.companion@gmail.com>"

    # ─── Email — Resend (fallback) ───
    resend_api_key: str = ""

    # ─── CORS ───
    cors_origins: list[str] = ["http://localhost:5173", "http://localhost:5174", "http://localhost:3000"]

    @property
    def is_development(self) -> bool:
        return self.app_env == "development"


settings = Settings()
