"""Configuration settings for the application."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""

    # LangSmith configuration
    langsmith_api_key: str = ""
    langsmith_project: str = "agent-immo"
    langsmith_tracing: bool = True

    # Database configuration
    database_url: str = "postgresql://user:password@localhost:5432/agentimmo"

    # API configuration
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_reload: bool = True

    # Frontend configuration
    frontend_url: str = "http://localhost:5173"

    # OpenAI configuration
    openai_api_key: str = ""

    class Config:
        """Pydantic config."""

        env_file = ".env"
        case_sensitive = False


settings = Settings()
