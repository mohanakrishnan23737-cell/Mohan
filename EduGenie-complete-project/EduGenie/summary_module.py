from gemini_client import generate_text


def summarize_text(text: str) -> str:
    prompt = f"""
Summarize the educational passage below for quick revision.

Requirements:
- Keep the core facts and meaning.
- Remove repetition and unnecessary detail.
- Use simple language.
- Prefer short paragraphs and bullet points.
- Do not add facts that are not present in the passage.

Passage:
{text}
""".strip()
    return generate_text(
        prompt,
        system_instruction="You are an educational summarization assistant.",
        temperature=0.25,
        max_output_tokens=1800,
    )
