from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from ..models.models import Conversation, Message
from ..schemas.conversation import ConversationCreate, MessageCreate

def get_conversation(db: Session, conversation_id: int, user_id: int):
    """Get a single conversation by ID for a specific user"""
    return db.query(Conversation).filter(
        Conversation.id == conversation_id,
        Conversation.user_id == user_id
    ).first()

def get_conversations(
    db: Session, 
    user_id: int, 
    skip: int = 0, 
    limit: int = 100
):
    """Get a list of conversations for a user with pagination"""
    return db.query(Conversation).filter(
        Conversation.user_id == user_id
    ).order_by(
        Conversation.updated_at.desc()
    ).offset(skip).limit(limit).all()

def create_conversation(db: Session, conversation: ConversationCreate):
    """Create a new conversation"""
    db_conversation = Conversation(
        user_id=conversation.user_id,
        title=conversation.title
    )
    db.add(db_conversation)
    db.commit()
    db.refresh(db_conversation)
    return db_conversation

def update_conversation_title(
    db: Session, 
    conversation_id: int, 
    user_id: int, 
    new_title: str
):
    """Update a conversation's title"""
    db_conversation = get_conversation(db, conversation_id, user_id)
    if db_conversation:
        db_conversation.title = new_title
        db.commit()
        db.refresh(db_conversation)
    return db_conversation

def delete_conversation(db: Session, conversation_id: int, user_id: int):
    """Delete a conversation and all its messages"""
    db_conversation = get_conversation(db, conversation_id, user_id)
    if db_conversation:
        db.delete(db_conversation)
        db.commit()
    return db_conversation

def add_message(
    db: Session, 
    conversation_id: int, 
    message: MessageCreate, 
    user_id: int
):
    """Add a message to a conversation"""
    # Verify the conversation exists and belongs to the user
    db_conversation = get_conversation(db, conversation_id, user_id)
    if not db_conversation:
        return None
    
    db_message = Message(
        conversation_id=conversation_id,
        content=message.content,
        is_user=message.is_user
    )
    db.add(db_message)
    
    # Update conversation's updated_at timestamp
    db_conversation.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(db_message)
    return db_message

def get_messages(
    db: Session, 
    conversation_id: int, 
    user_id: int,
    skip: int = 0,
    limit: int = 100
):
    """Get messages for a conversation with pagination"""
    # Verify the conversation exists and belongs to the user
    db_conversation = get_conversation(db, conversation_id, user_id)
    if not db_conversation:
        return []
    
    return db.query(Message).filter(
        Message.conversation_id == conversation_id
    ).order_by(
        Message.created_at.asc()
    ).offset(skip).limit(limit).all()
