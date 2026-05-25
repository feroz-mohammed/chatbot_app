import os
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from .database import Base, engine, get_db
from . import models, schemas, crud
from .llm import generate_reply

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Chatbot App (FastAPI + DB)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", include_in_schema=False)
def root():
    return FileResponse("static/index.html")

@app.post("/api/users", response_model=schemas.CreateUserResponse)
def create_user(req: schemas.CreateUserRequest, db: Session = Depends(get_db)):
    user = crud.get_or_create_user(db, name=req.name)
    return schemas.CreateUserResponse(id=user.id, name=user.name)

@app.post("/api/chat", response_model=schemas.ChatResponse)
def chat(req: schemas.ChatRequest, db: Session = Depends(get_db)):
  
    conv_id = req.conversation_id
    if conv_id is None:
        user_id = req.user_id
        conv = crud.create_conversation(db, user_id=user_id)
        conv_id = conv.id

    crud.add_message(db, conversation_id=conv_id, role="user", content=req.message)

    messages = [{"role": "system", "content": "You are a helpful assistant."}]
    for m in crud.get_messages(db, conversation_id=conv_id):
        messages.append({"role": m.role, "content": m.content})

    reply = generate_reply(messages)
    crud.add_message(db, conversation_id=conv_id, role="assistant", content=reply)

    return {"conversation_id": conv_id, "reply": reply}

@app.get("/api/conversations/{conversation_id}/messages", response_model=schemas.MessagesResponse)
def list_messages(conversation_id: int, db: Session = Depends(get_db)):
    from .models import Conversation
    conv = db.get(Conversation, conversation_id)
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")
    msgs = crud.get_messages(db, conversation_id=conversation_id)
    out = [{
        "id": m.id,
        "role": m.role,
        "content": m.content,
        "conversation_id": m.conversation_id,
        "created_at": m.created_at.isoformat() if m.created_at else None
    } for m in msgs]
    return {"conversation_id": conversation_id, "messages": out}
