from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

# Base schemas
class MessageBase(BaseModel):
    content: str
    is_user: bool = True

class MessageCreate(MessageBase):
    pass

class Message(MessageBase):
    id: int
    conversation_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class ConversationBase(BaseModel):
    title: str = "New Conversation"

class ConversationCreate(ConversationBase):
    user_id: int

class Conversation(ConversationBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    messages: List[Message] = []

    class Config:
        from_attributes = True

class ConversationList(BaseModel):
    id: int
    title: str
    updated_at: datetime
    last_message: Optional[str] = None
    last_message_time: Optional[datetime] = None
