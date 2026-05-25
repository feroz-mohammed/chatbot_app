from typing import Optional, List
from pydantic import BaseModel, Field

class MessageBase(BaseModel):
    role: str
    content: str

class MessageCreate(MessageBase):
    pass

class MessageOut(MessageBase):
    id: int
    conversation_id: int
    created_at: str

class ConversationOut(BaseModel):
    id: int
    title: Optional[str] = None

class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1)
    conversation_id: Optional[int] = None
    user_id: Optional[int] = None

class ChatResponse(BaseModel):
    conversation_id: int
    reply: str

class CreateUserRequest(BaseModel):
    name: Optional[str] = None

class CreateUserResponse(BaseModel):
    id: int
    name: Optional[str] = None

class MessagesResponse(BaseModel):
    conversation_id: int
    messages: List[MessageOut]
