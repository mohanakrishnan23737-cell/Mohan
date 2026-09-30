import pytest

import qna
import explanation_module
import summary_module
import learning_path
import quiz_module


def test_quiz_validation_accepts_three_questions():
    raw = [
        {
            "question": "2 + 2 = ?",
            "options": ["3", "4", "5", "6"],
            "answer": "4",
            "explanation": "Four is the sum of two and two.",
        },
        {
            "question": "Capital of France?",
            "options": ["Rome", "Paris", "Berlin", "Madrid"],
            "answer": "Paris",
        },
        {
            "question": "Water freezes at?",
            "options": ["0 C", "10 C", "50 C", "100 C"],
            "answer": "0 C",
        },
    ]
    assert len(quiz_module._validate_quiz(raw)) == 3


def test_quiz_clean_json_block():
    text = '```json\n{"questions": []}\n```'
    assert quiz_module.clean_json_block(text) == '{"questions": []}'


@pytest.mark.parametrize(
    "module_name,function_name",
    [
        ("qna", "answer_question"),
        ("explanation_module", "explain_topic"),
        ("summary_module", "summarize_text"),
        ("learning_path", "get_learning_recommendations"),
    ],
)
def test_modules_can_be_mocked(monkeypatch, module_name, function_name):
    module = {
        "qna": qna,
        "explanation_module": explanation_module,
        "summary_module": summary_module,
        "learning_path": learning_path,
    }[module_name]

    monkeypatch.setattr(module, "generate_text", lambda *args, **kwargs: "Mocked response")

    result = getattr(module, function_name)("Test topic")
    assert result == "Mocked response"
