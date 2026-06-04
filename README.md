# Chatbot App (FastAPI + SQLite + Simple Web UI)

A minimal end-to-end chatbot you can run locally. It stores chats in a database and can call an LLM
(OpenAI if `OPENAI_API_KEY` is set), otherwise it replies with a safe fallback.

## 1) Prerequisites
- Python 3.10+
- (Optional) An OpenAI API key if you want real AI responses.

## 2) Setup
```bash
cd chatbot_app
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1


pip install -r requirements.txt
copy .env.example .env   
```

Open `.env` and set:
- `DATABASE_URL` (defaults to sqlite:///./chat.db)
- `OPENAI_API_KEY` (optional)
- `OPENAI_MODEL` (e.g., gpt-4o-mini or gpt-3.5-turbo)
- `SYSTEM_PROMPT` (optional bot personality)

## 3) Run
```bash
uvicorn app.main:app --reload
```
Visit: http://127.0.0.1:8000

## 4) How it works
- `app/models.py`: SQLAlchemy models (`User`, `Conversation`, `Message`).
- `app/crud.py`: helpers to create/read rows.
- `app/llm.py`: calls OpenAI if configured, else uses a fallback.
- `app/main.py`: FastAPI endpoints to send messages and list history.
- `static/`: Very simple HTML/CSS/JS chat UI.

## 5) Next steps (ideas)
- Auth (JWT) and per-user conversations.
- Titles for conversations (use first user message or LLM to summarize).
- Streaming responses (Server-Sent Events / WebSocket) for typewriter effect.
- Postgres in production + Docker.
- Rate limiting, logging, and analytics.
- Tools (RAG, function calling) via your LLM provider.
