from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class ChatMessage(BaseModel):
    """Schema for a single chat message"""
    role: str = Field(..., description="The role of the message sender (user/assistant)")
    content: str = Field(..., description="The content of the message")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="When the message was created")

class ChatRequest(BaseModel):
    """Schema for chat request"""
    message: str = Field(..., description="The user's message")
    conversation_id: Optional[int] = Field(
        None,
        description="Optional conversation ID. If not provided, a new conversation will be created"
    )

class ChatResponse(BaseModel):
    """Schema for chat response"""
    response: str = Field(..., description="The AI's response message")
    conversation_id: int = Field(..., description="The ID of the conversation")
    message_id: int = Field(..., description="The ID of the AI's message in the database")
