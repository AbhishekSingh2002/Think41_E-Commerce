from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Boolean, JSON
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class ConversationSession(Base):
    """Represents a single conversation session between a user and the AI"""
    __tablename__ = 'conversation_sessions'
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    title = Column(String(255), nullable=True)  # Optional title for the conversation
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    user = relationship("User", back_populates="conversation_sessions")
    messages = relationship("ConversationMessage", back_populates="session", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<ConversationSession {self.id} - User {self.user_id}>"

class ConversationMessage(Base):
    """Represents a single message in a conversation"""
    __tablename__ = 'conversation_messages'
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey('conversation_sessions.id'), nullable=False)
    content = Column(Text, nullable=False)
    is_from_user = Column(Boolean, nullable=False)  # True if message is from user, False if from AI
    created_at = Column(DateTime, default=datetime.utcnow)
    metadata = Column(JSON, nullable=True)  # Store additional metadata like intent, entities, etc.
    
    # Relationships
    session = relationship("ConversationSession", back_populates="messages")
    
    def __repr__(self):
        return f"<Message {self.id} - Session {self.session_id}>"

# Update the User model to include the relationship with conversations
from models.models import User

# Add the relationship to the existing User model
if not hasattr(User, 'conversation_sessions'):
    User.conversation_sessions = relationship(
        "ConversationSession", 
        back_populates="user",
        cascade="all, delete-orphan"
    )
