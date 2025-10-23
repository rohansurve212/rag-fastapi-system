from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import uvicorn
from config import settings
from routers import chat_router, documents_router, search_router, rag_router
from models import HealthResponse, APIStatusResponse
from database import db_manager
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI application
app = FastAPI(
    title="RAG System API",
    description="A Retrieval-Augmented Generation system for document Q&A",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(chat_router)
app.include_router(documents_router)
app.include_router(search_router)
app.include_router(rag_router)


@app.get("/")
async def root():
    """
    Root endpoint - Welcome message
    """
    return {
        "message": "Welcome to RAG System API",
        "version": "1.0.0",
        "documentation": "/docs",
        "endpoints": {
            "health": "/health",
            "status": "/api/v1/status",
            "chat": "/api/v1/chat",
            "rag_chat": "/api/v1/rag/chat",
            "rag_health": "/api/v1/rag/health",
            "upload_document": "/api/v1/documents/upload",
            "list_documents": "/api/v1/documents/",
            "search_semantic": "/api/v1/search/semantic",
            "search_hybrid": "/api/v1/search/hybrid",
            "search_stats": "/api/v1/search/stats",
            "test_parser": "/api/v1/documents/test/parse-text",
            "test_chunking": "/api/v1/documents/test/chunking"
        }
    }


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint to verify the API is running
    """
    # Check if OpenAI API key is configured
    openai_configured = bool(settings.openai_api_key)
    
    # Check database connection
    db_connected = db_manager.test_connection()
    
    return HealthResponse(
        status="healthy" if db_connected else "degraded",
        timestamp=datetime.utcnow(),
        service="RAG System API",
        openai_configured=openai_configured
    )


@app.get("/api/v1/status", response_model=APIStatusResponse)
async def api_status():
    """
    API status endpoint with detailed information
    """
    # Check OpenAI configuration
    openai_configured = bool(settings.openai_api_key)
    openai_status = {
        "configured": openai_configured,
        "model": settings.openai_model if openai_configured else None,
        "embedding_model": settings.openai_embedding_model if openai_configured else None
    }
    
    return APIStatusResponse(
        api_version="1.0.0",
        status="operational",
        timestamp=datetime.utcnow(),
        endpoints={
            "root": "/",
            "health": "/health",
            "chat": "/api/v1/chat",
            "rag_chat": "/api/v1/rag/chat",
            "rag_health": "/api/v1/rag/health",
            "test_openai": "/api/v1/chat/test",
            "upload_document": "/api/v1/documents/upload",
            "list_documents": "/api/v1/documents/",
            "search_semantic": "/api/v1/search/semantic",
            "search_keyword": "/api/v1/search/keyword",
            "search_hybrid": "/api/v1/search/hybrid",
            "search_context": "/api/v1/search/context",
            "search_stats": "/api/v1/search/stats",
            "docs": "/docs",
            "openapi": "/openapi.json"
        },
        openai_status=openai_status
    )


@app.on_event("startup")
async def startup_event():
    """
    Run on application startup
    """
    logger.info("=" * 50)
    logger.info("RAG System API Starting...")
    logger.info(f"Environment: {settings.environment}")
    logger.info(f"OpenAI Configured: {bool(settings.openai_api_key)}")
    logger.info(f"OpenAI Model: {settings.openai_model}")
    logger.info("=" * 50)
    
    # Test database connection
    logger.info("Testing database connection...")
    if db_manager.test_connection():
        logger.info("✓ Database connection successful")
        
        # Create tables if they don't exist
        try:
            db_manager.create_tables()
            logger.info("✓ Database tables verified/created")
        except Exception as e:
            logger.error(f"✗ Failed to create tables: {str(e)}")
    else:
        logger.error("✗ Database connection failed")
    
    logger.info("=" * 50)


@app.on_event("shutdown")
async def shutdown_event():
    """
    Run on application shutdown
    """
    logger.info("RAG System API Shutting Down...")
    
    # Close database connection
    try:
        db_manager.close()
        logger.info("✓ Database connection closed")
    except Exception as e:
        logger.error(f"✗ Error closing database: {str(e)}")


if __name__ == "__main__":
    # Run the application
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )