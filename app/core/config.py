# FILE: docgen_tool_service/app/core/config.py

import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    """
    Manages application settings for the DocGen Service.
    """
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding='utf-8', extra='ignore')

    # --- API Keys ---
    # We NEED the Google API Key for the LLM
    GOOGLE_API_KEY: str | None = os.getenv("GOOGLE_API_KEY")

    # You can add any settings specific to DocGen here if needed.
    # Example:
    # DEFAULT_FONT_PATH: str = "DejaVuSans.ttf"

# Create a single, globally accessible instance of the settings
settings = Settings()