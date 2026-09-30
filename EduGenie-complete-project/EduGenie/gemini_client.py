from functools import lru_cache

from google import genai
from google.genai import types

from config import get_settings


class GeminiServiceError(RuntimeError):
    """Raised when Gemini cannot be used successfully."""


@lru_cache
def get_client() -> genai.Client:
    settings = get_settings()
    if not settings.GEMINI_API_KEY:
        raise GeminiServiceError(
            "GEMINI_API_KEY is not configured. Copy .env.example to .env and add your Google AI API key."
        )
    try:
        return genai.Client(api_key=settings.GEMINI_API_KEY)
    except Exception as exc:
        raise GeminiServiceError(f"Could not initialize Gemini client: {exc}") from exc


def generate_text(
    prompt: str,
    *,
    system_instruction: str | None = None,
    temperature: float = 0.4,
    max_output_tokens: int = 2048,
    response_mime_type: str | None = None,
) -> str:
    settings = get_settings()
    config_kwargs = {
        "temperature": temperature,
        "max_output_tokens": max_output_tokens,
    }
    if system_instruction:
        config_kwargs["system_instruction"] = system_instruction
    if response_mime_type:
        config_kwargs["response_mime_type"] = response_mime_type

    try:
        response = get_client().models.generate_content(
            model=settings.GEMINI_MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(**config_kwargs),
        )
        text = (response.text or "").strip()
        if not text:
            raise GeminiServiceError("Gemini returned an empty response.")
        return text
    except GeminiServiceError:
        raise
    except Exception as exc:
        raise GeminiServiceError(f"Gemini request failed: {exc}") from exc
