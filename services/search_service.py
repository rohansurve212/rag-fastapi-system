from typing import List, Optional, Dict, Tuple
from sqlalchemy.orm import Session
from datetime import datetime
import logging

from database.crud import ChunkCRUD, DocumentCRUD
from database.models import DocumentChunk, Document
from services.openai_service import openai_service

logger = logging.getLogger(__name__)


class SearchService:
    """
    Service for semantic and hybrid search operations
    """
    
    def __init__(self):
        self.openai_service = openai_service
        logger.info("Search service initialized")
    
    
    def semantic_search(
        self,
        db: Session,
        query: str,
        top_k: int = 5,
        document_id: Optional[str] = None,
        min_similarity: float = 0.0
    ) -> List[Dict]:
        """
        Perform semantic search using vector similarity
        
        Args:
            db: Database session
            query: Search query text
            top_k: Number of results to return
            document_id: Optional filter by document
            min_similarity: Minimum similarity threshold (0.0 to 1.0)
            
        Returns:
            List of search results with metadata
        """
        try:
            logger.info(f"Semantic search: '{query}' (top_k={top_k})")
            
            # Generate query embedding
            query_embedding = self.openai_service.create_embedding(query)
            
            # Search for similar chunks
            results = ChunkCRUD.search_similar_chunks(
                db=db,
                query_embedding=query_embedding,
                limit=top_k * 2,  # Get more results for filtering
                document_id=document_id
            )
            
            # Filter by minimum similarity and format results
            formatted_results = []
            for chunk, similarity in results:
                if similarity >= min_similarity:
                    # Get document info
                    document = DocumentCRUD.get_document_by_id(db, chunk.document_id)
                    
                    result = {
                        "chunk_id": chunk.chunk_id,
                        "document_id": chunk.document_id,
                        "document_name": document.filename if document else "Unknown",
                        "text": chunk.chunk_text,
                        "chunk_index": chunk.chunk_index,
                        "similarity_score": round(similarity, 4),
                        "chunk_size": chunk.chunk_size,
                        "metadata": {
                            "file_type": document.file_type if document else None,
                            "uploaded_at": document.uploaded_at.isoformat() if document and document.uploaded_at else None
                        }
                    }
                    formatted_results.append(result)
                    
                    if len(formatted_results) >= top_k:
                        break
            
            logger.info(f"Found {len(formatted_results)} results")
            return formatted_results
            
        except Exception as e:
            logger.error(f"Semantic search failed: {str(e)}")
            raise
    
    
    def keyword_search(
        self,
        db: Session,
        query: str,
        top_k: int = 5,
        document_id: Optional[str] = None
    ) -> List[Dict]:
        """
        Perform keyword-based search using text matching
        
        Args:
            db: Database session
            query: Search query text
            top_k: Number of results to return
            document_id: Optional filter by document
            
        Returns:
            List of search results with metadata
        """
        try:
            logger.info(f"Keyword search: '{query}' (top_k={top_k})")
            
            # Convert query to lowercase for case-insensitive search
            search_term = f"%{query.lower()}%"
            
            # Query database for text matches
            from sqlalchemy import func
            
            query_obj = db.query(DocumentChunk).filter(
                func.lower(DocumentChunk.chunk_text).like(search_term)
            )
            
            if document_id:
                query_obj = query_obj.filter(DocumentChunk.document_id == document_id)
            
            chunks = query_obj.order_by(DocumentChunk.chunk_index).limit(top_k * 2).all()
            
            # Format results
            formatted_results = []
            for chunk in chunks:
                document = DocumentCRUD.get_document_by_id(db, chunk.document_id)
                
                # Calculate simple relevance score based on query term frequency
                text_lower = chunk.chunk_text.lower()
                query_lower = query.lower()
                frequency = text_lower.count(query_lower)
                relevance = min(frequency / 10.0, 1.0)  # Normalize to 0-1
                
                result = {
                    "chunk_id": chunk.chunk_id,
                    "document_id": chunk.document_id,
                    "document_name": document.filename if document else "Unknown",
                    "text": chunk.chunk_text,
                    "chunk_index": chunk.chunk_index,
                    "relevance_score": round(relevance, 4),
                    "chunk_size": chunk.chunk_size,
                    "match_count": frequency,
                    "metadata": {
                        "file_type": document.file_type if document else None,
                        "uploaded_at": document.uploaded_at.isoformat() if document and document.uploaded_at else None
                    }
                }
                formatted_results.append(result)
                
                if len(formatted_results) >= top_k:
                    break
            
            logger.info(f"Found {len(formatted_results)} keyword matches")
            return formatted_results
            
        except Exception as e:
            logger.error(f"Keyword search failed: {str(e)}")
            raise
    
    
    def hybrid_search(
        self,
        db: Session,
        query: str,
        top_k: int = 5,
        document_id: Optional[str] = None,
        semantic_weight: float = 0.7,
        keyword_weight: float = 0.3,
        min_similarity: float = 0.0
    ) -> List[Dict]:
        """
        Perform hybrid search combining semantic and keyword search
        
        Args:
            db: Database session
            query: Search query text
            top_k: Number of results to return
            document_id: Optional filter by document
            semantic_weight: Weight for semantic search (0.0 to 1.0)
            keyword_weight: Weight for keyword search (0.0 to 1.0)
            min_similarity: Minimum similarity threshold for semantic results
            
        Returns:
            List of search results ranked by combined score
        """
        try:
            logger.info(f"Hybrid search: '{query}' (semantic_w={semantic_weight}, keyword_w={keyword_weight})")
            
            # Normalize weights
            total_weight = semantic_weight + keyword_weight
            if total_weight > 0:
                semantic_weight = semantic_weight / total_weight
                keyword_weight = keyword_weight / total_weight
            
            # Get semantic results
            semantic_results = self.semantic_search(
                db=db,
                query=query,
                top_k=top_k * 2,
                document_id=document_id,
                min_similarity=min_similarity
            )
            
            # Get keyword results
            keyword_results = self.keyword_search(
                db=db,
                query=query,
                top_k=top_k * 2,
                document_id=document_id
            )
            
            # Combine results by chunk_id
            combined_scores = {}
            
            # Add semantic scores
            for result in semantic_results:
                chunk_id = result["chunk_id"]
                combined_scores[chunk_id] = {
                    "result": result,
                    "semantic_score": result["similarity_score"],
                    "keyword_score": 0.0
                }
            
            # Add/update with keyword scores
            for result in keyword_results:
                chunk_id = result["chunk_id"]
                if chunk_id in combined_scores:
                    combined_scores[chunk_id]["keyword_score"] = result["relevance_score"]
                else:
                    combined_scores[chunk_id] = {
                        "result": result,
                        "semantic_score": 0.0,
                        "keyword_score": result["relevance_score"]
                    }
            
            # Calculate combined scores
            ranked_results = []
            for chunk_id, data in combined_scores.items():
                combined_score = (
                    data["semantic_score"] * semantic_weight +
                    data["keyword_score"] * keyword_weight
                )
                
                result = data["result"].copy()
                result["combined_score"] = round(combined_score, 4)
                result["semantic_score"] = round(data["semantic_score"], 4)
                result["keyword_score"] = round(data["keyword_score"], 4)
                
                # Remove individual scores if they were added
                result.pop("similarity_score", None)
                result.pop("relevance_score", None)
                result.pop("match_count", None)
                
                ranked_results.append(result)
            
            # Sort by combined score
            ranked_results.sort(key=lambda x: x["combined_score"], reverse=True)
            
            # Return top_k results
            final_results = ranked_results[:top_k]
            
            logger.info(f"Hybrid search returned {len(final_results)} results")
            return final_results
            
        except Exception as e:
            logger.error(f"Hybrid search failed: {str(e)}")
            raise
    
    
    def search_with_context(
        self,
        db: Session,
        query: str,
        top_k: int = 5,
        context_window: int = 1,
        **kwargs
    ) -> List[Dict]:
        """
        Search and include surrounding chunks for context
        
        Args:
            db: Database session
            query: Search query text
            top_k: Number of results to return
            context_window: Number of chunks before/after to include
            **kwargs: Additional search parameters
            
        Returns:
            List of search results with context chunks
        """
        try:
            # Perform hybrid search
            results = self.hybrid_search(db=db, query=query, top_k=top_k, **kwargs)
            
            # Add context for each result
            for result in results:
                document_id = result["document_id"]
                chunk_index = result["chunk_index"]
                
                # Get surrounding chunks
                context_chunks = []
                
                # Get all chunks for this document
                all_chunks = ChunkCRUD.get_chunks_by_document(db, document_id)
                
                # Find chunks within context window
                for chunk in all_chunks:
                    if (chunk_index - context_window <= chunk.chunk_index <= chunk_index + context_window):
                        if chunk.chunk_index != chunk_index:  # Don't include the main chunk
                            context_chunks.append({
                                "chunk_index": chunk.chunk_index,
                                "text": chunk.chunk_text,
                                "position": "before" if chunk.chunk_index < chunk_index else "after"
                            })
                
                # Sort context chunks by index
                context_chunks.sort(key=lambda x: x["chunk_index"])
                result["context"] = context_chunks
            
            return results
            
        except Exception as e:
            logger.error(f"Search with context failed: {str(e)}")
            raise
    
    
    def get_search_statistics(self, db: Session) -> Dict:
        """
        Get statistics about searchable content
        
        Args:
            db: Database session
            
        Returns:
            Dictionary with statistics
        """
        try:
            from database.crud import ChunkCRUD, DocumentCRUD
            
            total_documents = DocumentCRUD.count_documents(db, status='completed')
            total_chunks = ChunkCRUD.count_chunks(db)
            chunks_with_embeddings = ChunkCRUD.count_chunks_with_embeddings(db)
            
            stats = {
                "total_documents": total_documents,
                "total_chunks": total_chunks,
                "chunks_with_embeddings": chunks_with_embeddings,
                "searchable_percentage": round(
                    (chunks_with_embeddings / total_chunks * 100) if total_chunks > 0 else 0,
                    2
                ),
                "average_chunks_per_document": round(
                    total_chunks / total_documents if total_documents > 0 else 0,
                    2
                )
            }
            
            return stats
            
        except Exception as e:
            logger.error(f"Failed to get search statistics: {str(e)}")
            raise


# Create singleton instance
search_service = SearchService()