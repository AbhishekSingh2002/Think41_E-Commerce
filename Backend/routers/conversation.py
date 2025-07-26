from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..database import get_db
from ..auth import get_current_active_user

router = APIRouter(prefix="/conversations", tags=["conversations"])

@router.post("/", response_model=schemas.conversation.Conversation)
def create_conversation(
    conversation: schemas.conversation.ConversationCreate,
    db: Session = Depends(get_db),
    current_user: schemas.user.User = Depends(get_current_active_user)
):
    """Create a new conversation"""
    if conversation.user_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to create conversation for this user"
        )
    return crud.create_conversation(db=db, conversation=conversation)

@router.get("/", response_model=List[schemas.conversation.ConversationList])
def list_conversations(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: schemas.user.User = Depends(get_current_active_user)
):
    """List all conversations for the current user"""
    conversations = crud.get_conversations(
        db=db, 
        user_id=current_user.id, 
        skip=skip, 
        limit=limit
    )
    
    # Convert to ConversationList objects with last message info
    result = []
    for conv in conversations:
        last_message = None
        if conv.messages:
            last_message = conv.messages[-1]
        
        result.append({
            "id": conv.id,
            "title": conv.title,
            "updated_at": conv.updated_at,
            "last_message": last_message.content if last_message else None,
            "last_message_time": last_message.created_at if last_message else None
        })
    
    return result

@router.get("/{conversation_id}", response_model=schemas.conversation.Conversation)
def get_conversation(
    conversation_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.user.User = Depends(get_current_active_user)
):
    """Get a specific conversation"""
    db_conversation = crud.get_conversation(
        db=db, 
        conversation_id=conversation_id, 
        user_id=current_user.id
    )
    if db_conversation is None:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return db_conversation

@router.patch("/{conversation_id}", response_model=schemas.conversation.Conversation)
def update_conversation(
    conversation_id: int,
    title: str,
    db: Session = Depends(get_db),
    current_user: schemas.user.User = Depends(get_current_active_user)
):
    """Update a conversation's title"""
    return crud.update_conversation_title(
        db=db,
        conversation_id=conversation_id,
        user_id=current_user.id,
        new_title=title
    )

@router.delete("/{conversation_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_conversation(
    conversation_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.user.User = Depends(get_current_active_user)
):
    """Delete a conversation and all its messages"""
    crud.delete_conversation(
        db=db,
        conversation_id=conversation_id,
        user_id=current_user.id
    )
    return {"ok": True}

@router.post("/{conversation_id}/messages", response_model=schemas.conversation.Message)
def create_message(
    conversation_id: int,
    message: schemas.conversation.MessageCreate,
    db: Session = Depends(get_db),
    current_user: schemas.user.User = Depends(get_current_active_user)
):
    """Add a message to a conversation"""
    db_message = crud.add_message(
        db=db,
        conversation_id=conversation_id,
        message=message,
        user_id=current_user.id
    )
    if db_message is None:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return db_message

@router.get("/{conversation_id}/messages", response_model=List[schemas.conversation.Message])
def list_messages(
    conversation_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: schemas.user.User = Depends(get_current_active_user)
):
    """List messages in a conversation"""
    return crud.get_messages(
        db=db,
        conversation_id=conversation_id,
        user_id=current_user.id,
        skip=skip,
        limit=limit
    )
