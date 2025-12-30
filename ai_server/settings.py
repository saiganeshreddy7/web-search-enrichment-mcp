"""
Settings module for managing OpenAI configuration.
Compatible with your existing settings pattern.
"""

import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Settings:
    """Settings class that mimics your existing settings pattern."""

    def __init__(self):
        # OpenAI Configuration
        self.OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")

        # Model Configuration
        self.OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4o")
        self.OPENAI_TEMPERATURE: float = float(os.getenv("OPENAI_TEMPERATURE", "0.0"))
        self.OPENAI_MAX_TOKENS: Optional[int] = None
        max_tokens_env = os.getenv("OPENAI_MAX_TOKENS")
        if max_tokens_env:
            self.OPENAI_MAX_TOKENS = int(max_tokens_env)

        # Timeout and Retry Configuration
        self.OPENAI_TIMEOUT: float = float(os.getenv("OPENAI_TIMEOUT", "60.0"))
        self.OPENAI_MAX_RETRIES: int = int(os.getenv("OPENAI_MAX_RETRIES", "3"))
        self.OPENAI_RETRY_DELAY: float = float(os.getenv("OPENAI_RETRY_DELAY", "1.0"))

        # Rate Limiting
        self.OPENAI_MAX_CONCURRENT: int = int(os.getenv("OPENAI_MAX_CONCURRENT", "5"))

        # Logging
        self.OPENAI_LOG_LEVEL: str = os.getenv("OPENAI_LOG_LEVEL", "INFO")

    @property
    def openai_config_dict(self) -> dict:
        """Return OpenAI configuration as a dictionary."""
        return {
            "api_key": self.OPENAI_API_KEY,
            "model_name": self.OPENAI_MODEL,
            "temperature": self.OPENAI_TEMPERATURE,
            "max_tokens": self.OPENAI_MAX_TOKENS,
            "timeout": self.OPENAI_TIMEOUT,
            "max_retries": self.OPENAI_MAX_RETRIES,
            "retry_delay": self.OPENAI_RETRY_DELAY,
        }


# Create global settings instance
settings = Settings()
