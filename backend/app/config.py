from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "llama3:8b"  # Default model; override with OLLAMA_MODEL env var
    llm_provider: str = "ollama"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


settings = Settings()

