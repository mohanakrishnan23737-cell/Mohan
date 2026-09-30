from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

from qna import answer_question
from explanation_module import explain_topic
from quiz_module import generate_quiz
from summary_module import summarize_text
from learning_path import get_learning_recommendations

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(
    title="EduGenie - Google Gemini Powered Learning Assistant",
    version="1.0.0",
    description="An educational assistant for Q&A, explanations, quizzes, summaries and learning paths.",
)

app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


class TextRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=30000)


class QuestionRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=10000)


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/health")
async def health():
    return {"status": "ok", "service": "EduGenie"}


@app.post("/qa")
async def qa(payload: QuestionRequest):
    return {"answer": answer_question(payload.question)}


@app.post("/explain")
async def explain(payload: TextRequest):
    return {"answer": explain_topic(payload.text)}


@app.post("/quiz")
async def quiz(payload: TextRequest):
    return {"quiz": generate_quiz(payload.text)}


@app.post("/summarize")
async def summarize(payload: TextRequest):
    return {"summary": summarize_text(payload.text)}


@app.post("/learn/recommendations")
async def learning_recommendations(payload: TextRequest):
    return {"recommendations": get_learning_recommendations(payload.text)}
