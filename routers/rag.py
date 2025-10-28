from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field

from models import ErrorResponse, ChatMessage
from database import get_db
from services import rag_service
import logging

logger = logging.getLogger(__name__)


# Request/Response Models
class RAGChatRequest(BaseModel):
    """Request model for RAG chat"""
    query: str = Field(..., description="User question", min_length=1, max_length=2000)
    conversation_history: Optional[List[ChatMessage]] = Field(
        default=None,
        description="Previous conversation messages"
    )
    document_id: Optional[str] = Field(
        default=None,
        description="Filter search to specific document"
    )
    top_k: int = Field(
        default=8,
        description="Number of chunks to retrieve",
        ge=1,
        le=20
    )
    temperature: float = Field(
        default=0.7,
        description="Response temperature",
        ge=0.0,
        le=2.0
    )
    max_tokens: int = Field(
        default=500,
        description="Maximum response tokens",
        ge=50,
        le=2000
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "query": "What is machine learning?",
                "top_k": 5,
                "temperature": 0.7,
                "max_tokens": 500
            }
        }


class Source(BaseModel):
    """Source information"""
    source_number: int
    document_name: str
    document_id: str
    chunk_index: int
    relevance_score: float
    text_preview: str


class RAGChatResponse(BaseModel):
    """Response model for RAG chat"""
    success: bool
    query: str
    answer: str
    sources: List[Source]
    context_used: int
    model: str
    tokens_used: int
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "query": "What is machine learning?",
                "answer": "According to Source 1, machine learning is...",
                "sources": [
                    {
                        "source_number": 1,
                        "document_name": "ai_guide.txt",
                        "document_id": "doc_abc123",
                        "chunk_index": 2,
                        "relevance_score": 0.85,
                        "text_preview": "Machine learning is a subset..."
                    }
                ],
                "context_used": 3,
                "model": "gpt-4",
                "tokens_used": 250,
                "timestamp": "2025-10-19T12:00:00"
            }
        }


# Create router
router = APIRouter(
    prefix="/api/v1/rag",
    tags=["RAG (Retrieval-Augmented Generation)"],
    responses={
        500: {"model": ErrorResponse, "description": "Internal server error"},
        400: {"model": ErrorResponse, "description": "Bad request"}
    }
)


@router.post("/chat", response_model=RAGChatResponse)
async def rag_chat(
    request: RAGChatRequest,
    db: Session = Depends(get_db)
):
    """
    RAG-powered chat with automatic context retrieval
    
    **Retrieval-Augmented Generation (RAG)** combines:
    1. **Retrieval**: Search your documents for relevant information
    2. **Generation**: Use AI to generate answers based on retrieved context
    
    **How it works:**
    1. Your question is used to search uploaded documents
    2. Most relevant chunks are retrieved
    3. AI generates an answer using only the retrieved context
    4. Sources are provided for verification
    
    **Request Body:**
    - query: Your question (required)
    - conversation_history: Previous messages for context (optional)
    - document_id: Limit search to specific document (optional)
    - top_k: Number of chunks to retrieve (1-10, default: 5)
    - temperature: Response creativity (0.0-2.0, default: 0.7)
    - max_tokens: Maximum response length (50-2000, default: 500)
    
    **Returns:**
    - answer: AI-generated response based on your documents
    - sources: List of source chunks with relevance scores
    - context_used: Number of chunks used
    - model: AI model used
    - tokens_used: Total tokens consumed
    
    **Example:**
    ```json
    {
      "query": "How does deep learning work?",
      "top_k": 5,
      "temperature": 0.7
    }
    ```
    
    **Features:**
    - ✅ Automatic context retrieval from your documents
    - ✅ Source attribution for transparency
    - ✅ Multi-turn conversation support
    - ✅ Document filtering
    - ✅ Configurable retrieval and generation parameters
    
    **Best Practices:**
    - Ask specific questions for better results
    - Use conversation_history for follow-up questions
    - Lower temperature (0.3-0.5) for factual answers
    - Higher temperature (0.7-1.0) for creative responses
    """
    try:
        logger.info(f"RAG chat request: '{request.query}'")
        
        # Generate RAG response
        rag_response = rag_service.generate_rag_response(
            db=db,
            query=request.query,
            conversation_history=[msg.dict() for msg in request.conversation_history] if request.conversation_history else None,
            document_id=request.document_id,
            top_k=request.top_k,
            temperature=request.temperature,
            max_tokens=request.max_tokens
        )
        
        # Build response
        response = RAGChatResponse(
            success=True,
            query=request.query,
            answer=rag_response["answer"],
            sources=[Source(**src) for src in rag_response["sources"]],
            context_used=rag_response["context_used"],
            model=rag_response["model"],
            tokens_used=rag_response["tokens_used"]
        )
        
        logger.info(f"RAG chat completed: {len(rag_response['sources'])} sources used")
        return response
        
    except Exception as e:
        logger.error(f"RAG chat error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"RAG chat failed: {str(e)}"
        )


@router.post("/chat/stream")
async def rag_chat_stream(
    request: RAGChatRequest,
    db: Session = Depends(get_db)
):
    """
    RAG chat with streaming response (placeholder for future implementation)
    
    **Note**: Streaming is not yet implemented. This endpoint will:
    1. Retrieve context as usual
    2. Stream the AI response token by token
    3. Provide sources after streaming completes
    
    For now, use the regular `/chat` endpoint.
    """
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Streaming is not yet implemented. Please use /api/v1/rag/chat"
    )


@router.get("/health")
async def rag_health_check(db: Session = Depends(get_db)):
    """
    Check RAG system health
    
    Verifies:
    - Database connection
    - Documents available
    - Chunks with embeddings
    - Search functionality
    
    **Returns:**
    - Status of RAG system components
    - Readiness indicators
    """
    try:
        from database.crud import DocumentCRUD, ChunkCRUD
        from config import settings

        # Check database connection
        database_connection = True
        try:
            db.execute(text("SELECT 1"))
        except:
            database_connection = False

        # Check OpenAI configuration
        openai_configured = bool(settings.openai_api_key)

        # Check document availability
        total_docs = DocumentCRUD.count_documents(db, status='completed')
        total_chunks = ChunkCRUD.count_chunks(db)
        chunks_with_embeddings = ChunkCRUD.count_chunks_with_embeddings(db)

        # Check if embeddings are ready
        embedding_ready = chunks_with_embeddings > 0

        is_ready = (
            database_connection and
            openai_configured and
            total_docs > 0 and
            chunks_with_embeddings > 0
        )

        return {
            "status": "healthy" if is_ready else "not_ready",
            "database_connection": database_connection,
            "openai_configured": openai_configured,
            "embedding_ready": embedding_ready,
            "total_documents": total_docs,
            "total_chunks": total_chunks,
            "indexed_chunks": chunks_with_embeddings,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"RAG health check failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Health check failed: {str(e)}"
        )