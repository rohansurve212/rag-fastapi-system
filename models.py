from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class ChatMessage(BaseModel):
    """
    Represents a single message in a conversation
    """
    role: str = Field(..., description="Role of the message sender (user/assistant/system)")
    content: str = Field(..., description="Content of the message")


class ChatRequest(BaseModel):
    """
    Request model for chat endpoint
    """
    message: str = Field(..., description="User's message", min_length=1, max_length=4000)
    conversation_history: Optional[List[ChatMessage]] = Field(
        default=None,
        description="Optional conversation history for context"
    )
    temperature: Optional[float] = Field(
        default=0.7,
        description="Controls randomness in responses (0.0 to 2.0)",
        ge=0.0,
        le=2.0
    )
    max_tokens: Optional[int] = Field(
        default=500,
        description="Maximum tokens in the response",
        ge=1,
        le=4000
    )

    class Config:
        json_schema_extra = {
            "example": {
                "message": "What is FastAPI?",
                "temperature": 0.7,
                "max_tokens": 500
            }
        }


class ChatResponse(BaseModel):
    """
    Response model for chat endpoint
    """
    response: str = Field(..., description="AI assistant's response")
    message_count: int = Field(..., description="Number of messages in conversation")
    tokens_used: Optional[int] = Field(None, description="Total tokens used in the request")
    model: str = Field(..., description="Model used for generation")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Response timestamp")

    class Config:
        json_schema_extra = {
            "example": {
                "response": "FastAPI is a modern, fast web framework for building APIs with Python.",
                "message_count": 1,
                "tokens_used": 150,
                "model": "gpt-4",
                "timestamp": "2025-10-18T12:00:00"
            }
        }


class ErrorResponse(BaseModel):
    """
    Standard error response model
    """
    error: str = Field(..., description="Error type")
    message: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Detailed error information")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Error timestamp")

    class Config:
        json_schema_extra = {
            "example": {
                "error": "OpenAIError",
                "message": "Failed to generate response",
                "detail": "API rate limit exceeded",
                "timestamp": "2025-10-18T12:00:00"
            }
        }


class HealthResponse(BaseModel):
    """
    Health check response model
    """
    status: str
    timestamp: datetime
    service: str
    openai_configured: bool = Field(..., description="Whether OpenAI API key is configured")


class APIStatusResponse(BaseModel):
    """
    Detailed API status response
    """
    api_version: str
    status: str
    timestamp: datetime
    endpoints: dict
    openai_status: dict = Field(..., description="OpenAI configuration status")


class DocumentMetadata(BaseModel):
    """
    Metadata for uploaded documents
    """
    document_id: str
    filename: str
    file_type: str
    file_size: int
    file_hash: str
    character_count: Optional[int] = None
    word_count: Optional[int] = None
    page_count: Optional[int] = None
    chunk_count: Optional[int] = None
    uploaded_at: datetime = Field(default_factory=datetime.utcnow)


class DocumentUploadResponse(BaseModel):
    """
    Response for document upload
    """
    success: bool
    message: str
    document_id: str = Field(..., description="Unique identifier for the document")
    filename: str
    file_size: int
    file_hash: str
    chunks_created: int
    metadata: DocumentMetadata
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Document uploaded and processed successfully",
                "document_id": "doc_abc123",
                "filename": "example.pdf",
                "file_size": 52428,
                "file_hash": "a1b2c3d4e5f6",
                "chunks_created": 5,
                "metadata": {
                    "filename": "example.pdf",
                    "file_type": "pdf",
                    "file_size": 52428,
                    "file_hash": "a1b2c3d4e5f6",
                    "page_count": 3,
                    "word_count": 1500,
                    "chunk_count": 5
                },
                "timestamp": "2025-10-18T12:00:00"
            }
        }


class ChunkData(BaseModel):
    """
    Represents a chunk of text from a document
    """
    chunk_id: str
    text: str
    chunk_index: int
    document_id: str
    metadata: dict = Field(default_factory=dict)


class DocumentListResponse(BaseModel):
    """
    Response for listing documents
    """
    documents: List[DocumentMetadata]
    total_count: int
    timestamp: datetime = Field(default_factory=datetime.utcnow)