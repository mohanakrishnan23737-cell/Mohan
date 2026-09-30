from gemini_client import generate_text


def get_learning_recommendations(topic: str) -> str:
    prompt = f"""
Create a personalized learning path for this topic:

{topic}

Structure it from beginner to advanced.
Include:
1. Prerequisites
2. Beginner stage
3. Intermediate stage
4. Advanced stage
5. A realistic suggested timeline
6. Practice/project ideas
7. Useful resource types (videos, articles, documentation, books)
8. A short checklist for knowing when the learner is ready to progress

Do not invent specific URLs. Mention resource names or types only when you are confident.
""".strip()
    return generate_text(
        prompt,
        system_instruction="You are a patient learning-path designer for students.",
        temperature=0.4,
        max_output_tokens=3000,
    )
