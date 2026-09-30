from gemini_client import generate_text

SYSTEM = """
You are EduGenie, a friendly educational assistant.
Answer academic questions accurately and clearly.
Use simple language suitable for a learner.
When useful, organize the response with short headings or bullet points.
Do not invent sources, facts, quotations, or citations.
If a question is ambiguous, state the assumption you are making.
""".strip()


def answer_question(question: str) -> str:
    prompt = f"""
Answer this student's question:

{question}

Keep the answer focused. Explain important terms briefly when needed.
""".strip()
    return generate_text(
        prompt,
        system_instruction=SYSTEM,
        temperature=0.3,
        max_output_tokens=1800,
    )
