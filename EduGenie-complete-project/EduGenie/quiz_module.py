import json
import re

from gemini_client import generate_text


def clean_json_block(text: str) -> str:
    """Remove Markdown code fences and isolate a JSON object/array."""
    cleaned = text.strip()
    cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"\s*```$", "", cleaned)
    start = min(
        [i for i in (cleaned.find("["), cleaned.find("{")) if i >= 0],
        default=0,
    )
    end_candidates = [cleaned.rfind("]"), cleaned.rfind("}")]
    end = max(end_candidates)
    if end >= start:
        cleaned = cleaned[start : end + 1]
    return cleaned.strip()


def _validate_quiz(data):
    if isinstance(data, dict):
        data = data.get("questions", data.get("quiz", []))
    if not isinstance(data, list) or len(data) != 3:
        raise ValueError("Quiz must contain exactly three questions.")

    validated = []
    for index, item in enumerate(data, start=1):
        if not isinstance(item, dict):
            raise ValueError(f"Question {index} is not an object.")

        question = str(item.get("question", "")).strip()
        options = item.get("options", [])
        answer = str(item.get("answer", item.get("correct_answer", ""))).strip()

        if not question or not isinstance(options, list) or len(options) != 4 or not answer:
            raise ValueError(f"Question {index} has an invalid structure.")

        options = [str(option).strip() for option in options]
        if any(not option for option in options):
            raise ValueError(f"Question {index} contains an empty option.")
        if answer not in options:
            # Allow an index-based answer from the model.
            if answer in {"A", "B", "C", "D"}:
                answer = options["ABCD".index(answer)]
            elif answer.isdigit() and 1 <= int(answer) <= 4:
                answer = options[int(answer) - 1]
            else:
                raise ValueError(f"Question {index} has no matching correct answer.")

        explanation = str(item.get("explanation", "")).strip()
        validated.append(
            {
                "id": index,
                "question": question,
                "options": options,
                "answer": answer,
                "explanation": explanation,
            }
        )
    return validated


def generate_quiz(passage: str):
    prompt = f"""
Create exactly 3 multiple-choice questions from the educational text below.

Return ONLY valid JSON. Do not use Markdown or code fences.
Use exactly this schema:
{{
  "questions": [
    {{
      "question": "string",
      "options": ["option 1", "option 2", "option 3", "option 4"],
      "answer": "exactly one of the four option strings",
      "explanation": "brief explanation of why the answer is correct"
    }}
  ]
}}

Text:
{passage}
""".strip()

    raw = generate_text(
        prompt,
        system_instruction="You generate reliable educational MCQs and strict JSON.",
        temperature=0.2,
        max_output_tokens=2500,
        response_mime_type="application/json",
    )

    try:
        return _validate_quiz(json.loads(clean_json_block(raw)))
    except (json.JSONDecodeError, ValueError, TypeError) as exc:
        raise RuntimeError(f"Quiz generation returned invalid JSON: {exc}") from exc
