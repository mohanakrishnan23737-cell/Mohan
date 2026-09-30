from gemini_client import generate_text, GeminiServiceError
from config import get_settings


def _gemini_explanation(topic: str) -> str:
    prompt = f"""
Explain the following topic to a beginner.

Topic:
{topic}

Requirements:
- Start with a one-sentence definition.
- Explain the idea in simple language.
- Give one small example or analogy when appropriate.
- Finish with 3 key points.
- Avoid unnecessary jargon.
""".strip()
    return generate_text(
        prompt,
        system_instruction="You are an expert teacher who explains difficult ideas simply.",
        temperature=0.35,
        max_output_tokens=1800,
    )


def _local_explanation(topic: str) -> str:
    try:
        from transformers import pipeline
    except ImportError as exc:
        raise GeminiServiceError(
            "Local explanation mode requires transformers and torch. "
            "Install the optional dependencies or set USE_LOCAL_EXPLAINER=false."
        ) from exc

    settings = get_settings()
    try:
        generator = pipeline(
            "text2text-generation",
            model=settings.LOCAL_EXPLAINER_MODEL,
            max_new_tokens=220,
        )
        prompt = (
            "Explain this educational topic simply for a beginner. "
            "Include a definition, a short example, and three key points: "
            f"{topic}"
        )
        result = generator(prompt)[0]["generated_text"].strip()
        if not result:
            raise GeminiServiceError("The local explanation model returned no text.")
        return result
    except GeminiServiceError:
        raise
    except Exception as exc:
        raise GeminiServiceError(f"Local explanation model failed: {exc}") from exc


def explain_topic(topic: str) -> str:
    settings = get_settings()
    if settings.USE_LOCAL_EXPLAINER:
        try:
            return _local_explanation(topic)
        except GeminiServiceError:
            # Cloud fallback keeps the application usable if the optional local model
            # is not installed or cannot load.
            return _gemini_explanation(topic)
    return _gemini_explanation(topic)
