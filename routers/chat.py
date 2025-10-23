from fastapi import APIRouter, HTTPException, status  # pyright: ignore[reportMissingImports]
from typing import List, Dict
from models import ChatRequest, ChatResponse, ErrorResponse
from services import openai_service
from openai import OpenAIError
import logging

# Configure logging
logger = logging.getLogger(__name__)

# Create router
router = APIRouter(
    prefix="/api/v1/chat",
    tags=["Chat"],
    responses={
        500: {"model": ErrorResponse, "description": "Internal server error"},
        400: {"model": ErrorResponse, "description": "Bad request"}
    }
)


@router.post("", response_model=ChatResponse, status_code=status.HTTP_200_OK)
async def chat(request: ChatRequest):
    """
    Chat with the AI assistant
    
    This endpoint allows you to have a conversation with the AI assistant.
    You can optionally provide conversation history to maintain context.
    
    **Request Body:**
    - message: Your message to the assistant (required)
    - conversation_history: Previous messages for context (optional)
    - temperature: Control response randomness, 0.0-2.0 (default: 0.7)
    - max_tokens: Maximum response length (default: 500)
    
    **Returns:**
    - response: AI assistant's reply
    - message_count: Total messages in conversation
    - tokens_used: Total tokens consumed
    - model: Model used for generation
    - timestamp: Response timestamp
    """
    try:
        # Build messages list for OpenAI API
        messages: List[Dict[str, str]] = []
        
        # Add system message
        messages.append({
            "role": "system",
            "content": "You are a helpful AI assistant. Provide clear, accurate, and helpful responses."
        })
        
        # Add conversation history if provided
        if request.conversation_history:
            for msg in request.conversation_history:
                messages.append({
                    "role": msg.role,
                    "content": msg.content
                })
        
        # Add the current user message
        messages.append({
            "role": "user",
            "content": request.message
        })
        
        logger.info(f"Processing chat request with {len(messages)} messages")
        
        # Get response from OpenAI
        result = openai_service.chat_completion(
            messages=messages,
            temperature=request.temperature,
            max_tokens=request.max_tokens
        )
        
        # Create response
        response = ChatResponse(
            response=result["response"],
            message_count=len(messages),
            tokens_used=result["tokens_used"],
            model=result["model"]
        )
        
        logger.info("Chat request processed successfully")
        return response
        
    except OpenAIError as e:
        logger.error(f"OpenAI API error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"OpenAI API error: {str(e)}"
        )
    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Unexpected error in chat endpoint: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while processing your request"
        )


@router.get("/test", status_code=status.HTTP_200_OK)
async def test_openai_connection():
    """
    Test OpenAI API connection
    
    This endpoint tests whether the OpenAI API is properly configured
    and accessible.
    
    **Returns:**
    - status: Connection status
    - message: Status message
    - model: Configured model name
    """
    try:
        is_connected = openai_service.test_connection()
        
        if is_connected:
            return {
                "status": "success",
                "message": "OpenAI API is properly configured and accessible",
                "model": openai_service.model,
                "embedding_model": openai_service.embedding_model
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to connect to OpenAI API"
            )
            
    except Exception as e:
        logger.error(f"Error testing OpenAI connection: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error testing OpenAI connection: {str(e)}"
        )