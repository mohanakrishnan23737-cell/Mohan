# EduGenie — Google Gemini Powered Learning Assistant

EduGenie is a lightweight educational web application based on the supplied project documentation. It provides:

- Question answering
- Beginner-friendly topic explanations
- 3-question MCQ quiz generation
- Text summarization
- Beginner-to-advanced learning paths
- Interactive quiz answer checking

## Architecture

```text
EduGenie/
├── main.py
├── config.py
├── gemini_client.py
├── qna.py
├── explanation_module.py
├── quiz_module.py
├── summary_module.py
├── learning_path.py
├── requirements.txt
├── requirements-local-explainer.txt
├── .env.example
├── .gitignore
├── pyproject.toml
├── templates/
│   └── index.html
├── static/
│   └── style.css
└── tests/
    ├── test_api.py
    └── test_modules.py
```

## Requirements

- Python 3.10+
- A Google Gemini API key
- VS Code (recommended)

## 1. Open the project

Extract the ZIP and open the `EduGenie` folder in VS Code.

## 2. Create a virtual environment

### Windows PowerShell

```powershell
py -3.10 -m venv .venv
.venv\Scripts\Activate.ps1
```

If `py` is unavailable:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### macOS/Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 4. Configure Gemini

Copy `.env.example` to `.env`:

```powershell
Copy-Item .env.example .env
```

Then open `.env` and replace:

```text
GEMINI_API_KEY=put_your_google_ai_api_key_here
```

with your actual API key.

Do not commit `.env` to Git.

## 5. Run the application

```bash
uvicorn main:app --reload
```

Open:

```text
http://127.0.0.1:8000
```

API health check:

```text
http://127.0.0.1:8000/health
```

## 6. Test

Install dependencies first, then run:

```bash
pytest
```

The tests mock Gemini responses, so they do not consume API quota.

## API endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | Web application |
| GET | `/health` | Health check |
| POST | `/qa` | Question answering |
| POST | `/explain` | Topic explanation |
| POST | `/quiz` | Generate exactly 3 MCQs |
| POST | `/summarize` | Summarize educational text |
| POST | `/learn/recommendations` | Generate learning path |

Example Q&A request:

```json
{
  "question": "What is photosynthesis?"
}
```

Example quiz request:

```json
{
  "text": "Photosynthesis is the process by which green plants..."
}
```

## Optional local explanation model

The supplied documentation describes LaMini-Flan-T5-783M for explanations. This implementation supports that architecture as an optional mode.

Install the extra dependencies:

```bash
pip install -r requirements-local-explainer.txt
```

Then set:

```text
USE_LOCAL_EXPLAINER=true
```

The model is downloaded on first use by Hugging Face Transformers. Because local model availability and hardware vary, the app automatically falls back to Gemini if the local model cannot be loaded.

For the simplest setup, keep:

```text
USE_LOCAL_EXPLAINER=false
```

## Troubleshooting

### `GEMINI_API_KEY is not configured`

Make sure `.env` exists beside `main.py` and contains a valid key.

### Gemini request fails

Check:
1. Internet connection.
2. API key validity.
3. Gemini model availability for your account.
4. The value of `GEMINI_MODEL` in `.env`.

You can change the model without changing application code.

### PowerShell does not allow activation

You can run the environment's Python directly:

```powershell
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe -m uvicorn main:app --reload
```

### Port 8000 is already in use

```bash
uvicorn main:app --reload --port 8001
```

Then open `http://127.0.0.1:8001`.

## Security notes

- Keep API keys in `.env`.
- Never put the Gemini API key in frontend JavaScript.
- `.env` is excluded by `.gitignore`.
- The backend performs all Gemini calls.
- Input fields have maximum lengths to reduce accidental oversized requests.

## Notes on the supplied documentation

The original document names Gemini 1.5 Pro and LaMini-Flan-T5-783M. The project keeps the optional LaMini integration, but the default Gemini integration uses the current Google GenAI Python SDK and a configurable current Gemini model rather than the older SDK/API pattern.
