from fastapi.testclient import TestClient

import main
import qna
import explanation_module
import summary_module
import learning_path
import quiz_module


def test_health():
    client = TestClient(main.app)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_qa_endpoint(monkeypatch):
    monkeypatch.setattr(qna, "generate_text", lambda *args, **kwargs: "Test answer")
    client = TestClient(main.app)
    response = client.post("/qa", json={"question": "What is Python?"})
    assert response.status_code == 200
    assert response.json()["answer"] == "Test answer"


def test_explain_endpoint(monkeypatch):
    monkeypatch.setattr(explanation_module, "generate_text", lambda *args, **kwargs: "Simple explanation")
    client = TestClient(main.app)
    response = client.post("/explain", json={"text": "Python"})
    assert response.status_code == 200
    assert response.json()["answer"] == "Simple explanation"


def test_summary_endpoint(monkeypatch):
    monkeypatch.setattr(summary_module, "generate_text", lambda *args, **kwargs: "Summary")
    client = TestClient(main.app)
    response = client.post("/summarize", json={"text": "Long passage"})
    assert response.status_code == 200
    assert response.json()["summary"] == "Summary"


def test_learning_path_endpoint(monkeypatch):
    monkeypatch.setattr(learning_path, "generate_text", lambda *args, **kwargs: "Learning path")
    client = TestClient(main.app)
    response = client.post("/learn/recommendations", json={"text": "SQL"})
    assert response.status_code == 200
    assert response.json()["recommendations"] == "Learning path"


def test_quiz_endpoint(monkeypatch):
    fake_quiz = [
        {
            "question": "2 + 2?",
            "options": ["3", "4", "5", "6"],
            "answer": "4",
            "explanation": "2 + 2 is 4.",
        },
        {
            "question": "Capital of France?",
            "options": ["Rome", "Paris", "Berlin", "Madrid"],
            "answer": "Paris",
            "explanation": "Paris is the capital.",
        },
        {
            "question": "Water freezes at?",
            "options": ["0 C", "10 C", "50 C", "100 C"],
            "answer": "0 C",
            "explanation": "Fresh water freezes at 0 C under standard conditions.",
        },
    ]
    monkeypatch.setattr(quiz_module, "generate_quiz", lambda *args, **kwargs: fake_quiz)
    client = TestClient(main.app)
    response = client.post("/quiz", json={"text": "Basic facts"})
    assert response.status_code == 200
    assert len(response.json()["quiz"]) == 3
