from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class ChatHistory(Base):
    __tablename__ = "chat_history"
    id = Column(Integer, primary_key=True, index=True)
    thread_id = Column(String, index=True)
    role = Column(String)
    content = Column(String)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

# Pydantic models
from pydantic import BaseModel
from typing import List, Optional

class MessageRequest(BaseModel):
    text: str
    thread_id: Optional[str]
    user_id: Optional[str]

class MessageResponse(BaseModel):
    text: str
    thread_id: str

class RouteResult(BaseModel):
    assistant: int
    question: str

class AssistantRequest(BaseModel):
    assistant_id: int
    messages: List[dict]
    user_id: Optional[str]
    thread_id: str
