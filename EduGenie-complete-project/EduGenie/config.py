import os
from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")


class Settings:
    APP_NAME: str = os.getenv("APP_NAME", "EduGenie")
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")
    EXPLANATION_MODEL: str = os.getenv("EXPLANATION_MODEL", "gemini-3.8-flash")
    USE_LOCAL_EXPLAINER: bool = os.getenv("USE_LOCAL_EXPLAINER", "false").lower() == "true"
    LOCAL_EXPLAINER_MODEL: str = os.getenv(
        "LOCAL_EXPLAINER_MODEL",
        "MBZUAI/LaMini-Flan-T5-783M",
    )
    MAX_INPUT_CHARS: int = int(os.getenv("MAX_INPUT_CHARS", "30000"))


@lru_cache
def get_settings() -> Settings:
    return Settings()
