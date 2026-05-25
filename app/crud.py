from sqlalchemy.orm import Session
from . import models

def get_or_create_user(db: Session, name: str | None = None):
   
    user = models.User(name=name)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def create_conversation(db: Session, user_id: int | None):
    conv = models.Conversation(user_id=user_id, title=None)
    db.add(conv)
    db.commit()
    db.refresh(conv)
    return conv

def add_message(db: Session, conversation_id: int, role: str, content: str):
    msg = models.Message(conversation_id=conversation_id, role=role, content=content)
    db.add(msg)
    db.commit()
    db.refresh(msg)
    return msg

def get_messages(db: Session, conversation_id: int):
    from sqlalchemy import select
    stmt = select(models.Message).where(models.Message.conversation_id == conversation_id).order_by(models.Message.id.asc())
    return db.execute(stmt).scalars().all()
