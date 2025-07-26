from fastapi import APIRouter, Depends, HTTPException, status
from typing import Optional
from sqlalchemy.orm import Session
import logging

from ..database import get_db
from ..auth import get_current_active_user
from ..schemas.chat import ChatRequest, ChatResponse
from ..schemas.conversation import MessageCreate
from ..crud import conversation as crud_conversation
from ..services.chat_service import chat_service

router = APIRouter(prefix="/api", tags=["chat"])
logger = logging.getLogger(__name__)

@router.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user)
):
    """
    Handle chat messages from users.
    
    - If conversation_id is provided, adds to existing conversation
    - If no conversation_id, creates a new conversation
    - Returns AI response and conversation details
    """
    try:
        # Create a new conversation if no ID is provided
        if not request.conversation_id:
            conversation = crud_conversation.create_conversation(
                db=db,
                conversation={"user_id": current_user.id, "title": "New Chat"}
            )
            conversation_id = conversation.id
        else:
            # Verify the conversation exists and belongs to the user
            conversation = crud_conversation.get_conversation(
                db=db,
                conversation_id=request.conversation_id,
                user_id=current_user.id
            )
            if not conversation:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Conversation not found"
                )
            conversation_id = conversation.id
        
        # Save the user's message
        user_message = crud_conversation.add_message(
            db=db,
            conversation_id=conversation_id,
            message=MessageCreate(content=request.message, is_user=True),
            user_id=current_user.id
        )
        
        if not user_message:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to save user message"
            )
        
        # Get conversation context
        context = chat_service.get_conversation_context(conversation_id)
        
        # Get AI response
        ai_response_text = await chat_service.get_ai_response(
            message=request.message,
            context=context
        )
        
        # Save the AI's response
        ai_message = crud_conversation.add_message(
            db=db,
            conversation_id=conversation_id,
            message=MessageCreate(content=ai_response_text, is_user=False),
            user_id=current_user.id
        )
        
        if not ai_message:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to save AI response"
            )
        
        # Update conversation title if it's the first message
        if not request.conversation_id and conversation:
            # Use first few words of first user message as title
            title = request.message[:30] + (request.message[30:] and '...')
            crud_conversation.update_conversation_title(
                db=db,
                conversation_id=conversation_id,
                user_id=current_user.id,
                new_title=title
            )
        
        return {
            "response": ai_response_text,
            "conversation_id": conversation_id,
            "message_id": ai_message.id
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while processing your request"
        )
