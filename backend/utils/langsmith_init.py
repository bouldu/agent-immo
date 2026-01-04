"""LangSmith initialization utilities."""

import logging
import os

from backend.config import settings

logger = logging.getLogger(__name__)


def init_langsmith() -> None:
    """Initialize LangSmith with configuration from settings."""
    # Only enable tracing if we have a valid API key
    if settings.langsmith_api_key and settings.langsmith_tracing:
        os.environ["LANGSMITH_API_KEY"] = settings.langsmith_api_key
        os.environ["LANGCHAIN_TRACING_V2"] = "true"
        os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
        if settings.langsmith_project:
            os.environ["LANGSMITH_PROJECT"] = settings.langsmith_project
        logger.info("LangSmith tracing enabled for project: %s", settings.langsmith_project)
    else:
        # Explicitly disable tracing when no API key is configured
        os.environ["LANGCHAIN_TRACING_V2"] = "false"
        if not settings.langsmith_api_key:
            logger.warning(
                "LangSmith API key not configured. Tracing disabled. "
                "Set LANGSMITH_API_KEY in your .env file to enable tracing."
            )
