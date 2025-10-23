from fastapi import APIRouter, HTTPException, status, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime

from models import ErrorResponse
from database import get_db
from services import search_service
import logging

logger = logging.getLogger(__name__)

# Create router
router = APIRouter(
    prefix="/api/v1/search",
    tags=["Search"],
    responses={
        500: {"model": ErrorResponse, "description": "Internal server error"},
        400: {"model": ErrorResponse, "description": "Bad request"}
    }
)


@router.get("/semantic")
async def semantic_search(
    query: str = Query(..., description="Search query text", min_length=1),
    top_k: int = Query(5, description="Number of results to return", ge=1, le=20),
    document_id: Optional[str] = Query(None, description="Filter by document ID"),
    min_similarity: float = Query(0.0, description="Minimum similarity threshold (0.0-1.0)", ge=0.0, le=1.0),
    db: Session = Depends(get_db)
):
    """
    Perform semantic search using vector similarity
    
    **Semantic search** uses AI embeddings to find conceptually similar content,
    even if the exact words don't match.
    
    **Query Parameters:**
    - query: Search text (required)
    - top_k: Number of results (1-20, default: 5)
    - document_id: Filter by specific document (optional)
    - min_similarity: Minimum similarity score (0.0-1.0, default: 0.0)
    
    **Returns:**
    - List of relevant chunks ranked by similarity
    - Similarity scores (0.0 to 1.0)
    - Source document information
    
    **Example:**
    ```
    GET /api/v1/search/semantic?query=machine%20learning&top_k=5
    ```
    """
    try:
        logger.info(f"Semantic search request: '{query}'")
        
        results = search_service.semantic_search(
            db=db,
            query=query,
            top_k=top_k,
            document_id=document_id,
            min_similarity=min_similarity
        )
        
        return {
            "success": True,
            "query": query,
            "search_type": "semantic",
            "results_count": len(results),
            "results": results,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Semantic search error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Search failed: {str(e)}"
        )


@router.get("/keyword")
async def keyword_search(
    query: str = Query(..., description="Search query text", min_length=1),
    top_k: int = Query(5, description="Number of results to return", ge=1, le=20),
    document_id: Optional[str] = Query(None, description="Filter by document ID"),
    db: Session = Depends(get_db)
):
    """
    Perform keyword-based search using text matching
    
    **Keyword search** finds exact or partial text matches in documents.
    Useful for finding specific terms or phrases.
    
    **Query Parameters:**
    - query: Search text (required)
    - top_k: Number of results (1-20, default: 5)
    - document_id: Filter by specific document (optional)
    
    **Returns:**
    - List of matching chunks
    - Relevance scores based on match frequency
    - Source document information
    
    **Example:**
    ```
    GET /api/v1/search/keyword?query=neural%20networks&top_k=5
    ```
    """
    try:
        logger.info(f"Keyword search request: '{query}'")
        
        results = search_service.keyword_search(
            db=db,
            query=query,
            top_k=top_k,
            document_id=document_id
        )
        
        return {
            "success": True,
            "query": query,
            "search_type": "keyword",
            "results_count": len(results),
            "results": results,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Keyword search error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Search failed: {str(e)}"
        )


@router.get("/hybrid")
async def hybrid_search(
    query: str = Query(..., description="Search query text", min_length=1),
    top_k: int = Query(5, description="Number of results to return", ge=1, le=20),
    document_id: Optional[str] = Query(None, description="Filter by document ID"),
    semantic_weight: float = Query(0.7, description="Weight for semantic search", ge=0.0, le=1.0),
    keyword_weight: float = Query(0.3, description="Weight for keyword search", ge=0.0, le=1.0),
    min_similarity: float = Query(0.0, description="Minimum similarity for semantic results", ge=0.0, le=1.0),
    db: Session = Depends(get_db)
):
    """
    Perform hybrid search combining semantic and keyword search
    
    **Hybrid search** combines the best of both worlds:
    - Semantic search for conceptual similarity
    - Keyword search for exact matches
    
    Results are ranked by a weighted combination of both scores.
    
    **Query Parameters:**
    - query: Search text (required)
    - top_k: Number of results (1-20, default: 5)
    - document_id: Filter by specific document (optional)
    - semantic_weight: Weight for semantic scores (0.0-1.0, default: 0.7)
    - keyword_weight: Weight for keyword scores (0.0-1.0, default: 0.3)
    - min_similarity: Minimum similarity threshold (0.0-1.0, default: 0.0)
    
    **Returns:**
    - List of relevant chunks ranked by combined score
    - Individual semantic and keyword scores
    - Combined score
    - Source document information
    
    **Example:**
    ```
    GET /api/v1/search/hybrid?query=deep%20learning&top_k=5&semantic_weight=0.7&keyword_weight=0.3
    ```
    
    **Recommended weights:**
    - Balanced: semantic=0.5, keyword=0.5
    - Semantic-focused: semantic=0.7, keyword=0.3 (default)
    - Keyword-focused: semantic=0.3, keyword=0.7
    """
    try:
        logger.info(f"Hybrid search request: '{query}' (s={semantic_weight}, k={keyword_weight})")
        
        results = search_service.hybrid_search(
            db=db,
            query=query,
            top_k=top_k,
            document_id=document_id,
            semantic_weight=semantic_weight,
            keyword_weight=keyword_weight,
            min_similarity=min_similarity
        )
        
        return {
            "success": True,
            "query": query,
            "search_type": "hybrid",
            "results_count": len(results),
            "weights": {
                "semantic": semantic_weight,
                "keyword": keyword_weight
            },
            "results": results,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Hybrid search error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Search failed: {str(e)}"
        )


@router.get("/context")
async def search_with_context(
    query: str = Query(..., description="Search query text", min_length=1),
    top_k: int = Query(5, description="Number of results to return", ge=1, le=20),
    context_window: int = Query(1, description="Number of surrounding chunks to include", ge=0, le=5),
    document_id: Optional[str] = Query(None, description="Filter by document ID"),
    semantic_weight: float = Query(0.7, description="Weight for semantic search", ge=0.0, le=1.0),
    keyword_weight: float = Query(0.3, description="Weight for keyword search", ge=0.0, le=1.0),
    db: Session = Depends(get_db)
):
    """
    Search with surrounding context chunks
    
    **Context search** includes chunks before and after each result
    to provide better understanding of the content.
    
    **Query Parameters:**
    - query: Search text (required)
    - top_k: Number of results (1-20, default: 5)
    - context_window: Number of chunks before/after (0-5, default: 1)
    - document_id: Filter by specific document (optional)
    - semantic_weight: Weight for semantic search (default: 0.7)
    - keyword_weight: Weight for keyword search (default: 0.3)
    
    **Returns:**
    - Search results with context chunks
    - Main matching chunk
    - Preceding and following chunks
    
    **Example:**
    ```
    GET /api/v1/search/context?query=transformers&context_window=2
    ```
    
    **Use cases:**
    - Reading passages with context
    - Understanding narrative flow
    - Getting complete paragraphs
    """
    try:
        logger.info(f"Context search request: '{query}' (window={context_window})")
        
        results = search_service.search_with_context(
            db=db,
            query=query,
            top_k=top_k,
            context_window=context_window,
            document_id=document_id,
            semantic_weight=semantic_weight,
            keyword_weight=keyword_weight
        )
        
        return {
            "success": True,
            "query": query,
            "search_type": "context",
            "context_window": context_window,
            "results_count": len(results),
            "results": results,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Context search error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Search failed: {str(e)}"
        )


@router.get("/stats")
async def get_search_stats(db: Session = Depends(get_db)):
    """
    Get search statistics and system status
    
    **Returns:**
    - Total number of searchable documents
    - Total number of chunks
    - Number of chunks with embeddings
    - Percentage of searchable content
    - Average chunks per document
    
    **Example:**
    ```
    GET /api/v1/search/stats
    ```
    """
    try:
        stats = search_service.get_search_statistics(db)
        
        return {
            "success": True,
            "statistics": stats,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Failed to get search stats: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get statistics: {str(e)}"
        )