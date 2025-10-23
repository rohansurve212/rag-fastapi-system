from typing import List, Dict, Optional, Tuple
from sqlalchemy.orm import Session
import logging

from services.search_service import search_service
from services.openai_service import openai_service
from database.crud import DocumentCRUD

logger = logging.getLogger(__name__)


class RAGService:
    """
    Service for Retrieval-Augmented Generation (RAG)
    Combines search retrieval with LLM generation
    """
    
    def __init__(self):
        self.search_service = search_service
        self.openai_service = openai_service
        self.max_context_length = 6000  # Maximum characters for context
        self.max_sources = 10  # Maximum number of sources to include
        logger.info("RAG service initialized")
    
    
    def retrieve_context(
        self,
        db: Session,
        query: str,
        top_k: int = 5,
        document_id: Optional[str] = None,
        use_hybrid: bool = True
    ) -> Tuple[List[Dict], str]:
        """
        Retrieve relevant context for a query
        
        Args:
            db: Database session
            query: User query
            top_k: Number of chunks to retrieve
            document_id: Optional filter by document
            use_hybrid: Use hybrid search (recommended)
            
        Returns:
            Tuple of (search_results, assembled_context)
        """
        try:
            logger.info(f"Retrieving context for query: '{query}'")
            
            # Perform search
            if use_hybrid:
                results = self.search_service.hybrid_search(
                    db=db,
                    query=query,
                    top_k=top_k,
                    document_id=document_id,
                    semantic_weight=0.7,
                    keyword_weight=0.3
                )
            else:
                results = self.search_service.semantic_search(
                    db=db,
                    query=query,
                    top_k=top_k,
                    document_id=document_id
                )
            
            # Assemble context from results
            context = self._assemble_context(results)
            
            logger.info(f"Retrieved {len(results)} chunks, context length: {len(context)} chars")
            return results, context
            
        except Exception as e:
            logger.error(f"Context retrieval failed: {str(e)}")
            raise
    
    
    def _assemble_context(self, search_results: List[Dict]) -> str:
        """
        Assemble context from search results
        
        Args:
            search_results: List of search result dictionaries
            
        Returns:
            Assembled context string
        """
        context_parts = []
        total_length = 0
        
        for i, result in enumerate(search_results):
            chunk_text = result.get('text', '')
            document_name = result.get('document_name', 'Unknown')
            
            # Create context part with source attribution
            context_part = f"[Source {i+1}: {document_name}]\n{chunk_text}\n"
            
            # Check if adding this would exceed max length
            if total_length + len(context_part) > self.max_context_length:
                break
            
            context_parts.append(context_part)
            total_length += len(context_part)
        
        return "\n".join(context_parts)
    
    
    def generate_rag_response(
        self,
        db: Session,
        query: str,
        conversation_history: Optional[List[Dict]] = None,
        document_id: Optional[str] = None,
        top_k: int = 5,
        temperature: float = 0.7,
        max_tokens: int = 500
    ) -> Dict:
        """
        Generate RAG response with retrieved context

        Args:
            db: Database session
            query: User query
            conversation_history: Previous conversation messages
            document_id: Optional filter by document
            top_k: Number of chunks to retrieve
            temperature: LLM temperature
            max_tokens: Maximum response tokens

        Returns:
            Dictionary with response, sources, and metadata
        """
        try:
            logger.info(f"Generating RAG response for: '{query}'")

            # Step 1: Retrieve relevant context
            search_results, context = self.retrieve_context(
                db=db,
                query=query,
                top_k=top_k,
                document_id=document_id,
                use_hybrid=True
            )

            # Step 1.5: Check if any documents exist
            if not search_results or len(search_results) == 0:
                logger.warning("No documents found for RAG query")
                return {
                    "answer": "I don't have any documents to answer your question. Please upload documents first using the /api/v1/documents/upload endpoint.",
                    "sources": [],
                    "context_used": 0,
                    "model": "N/A",
                    "tokens_used": 0
                }

            # Step 2: Build prompt with context
            system_prompt = self._build_system_prompt(context)
            
            # Step 3: Build messages list
            messages = [{"role": "system", "content": system_prompt}]
            
            # Add conversation history if provided
            if conversation_history:
                for msg in conversation_history[-5:]:  # Last 5 messages
                    messages.append({
                        "role": msg.get("role", "user"),
                        "content": msg.get("content", "")
                    })
            
            # Add current query
            messages.append({"role": "user", "content": query})
            
            # Step 4: Generate response
            completion = self.openai_service.chat_completion(
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            # Step 5: Extract sources
            sources = self._extract_sources(search_results)
            
            # Step 6: Build response
            response = {
                "answer": completion["response"],
                "sources": sources,
                "context_used": len(search_results),
                "model": completion["model"],
                "tokens_used": completion["tokens_used"]
            }
            
            logger.info("RAG response generated successfully")
            return response
            
        except Exception as e:
            logger.error(f"RAG generation failed: {str(e)}")
            raise
    
    
    def _build_system_prompt(self, context: str) -> str:
        """
        Build system prompt with context

        Args:
            context: Retrieved context string

        Returns:
            System prompt string
        """
        return f"""You are a helpful AI assistant that answers questions based STRICTLY on provided document context.

        CRITICAL RULES - DO NOT VIOLATE:
        1. Answer ONLY using information from the CONTEXT below - DO NOT use your general knowledge
        2. If the context doesn't contain the answer, respond: "I don't have enough information in the available documents to answer that question."
        3. ALWAYS cite your sources using the format: "According to Source 1..." or "Source 2 states..."
        4. If asked to list or summarize multiple documents, identify each source separately
        5. DO NOT make up document names, content, or information that isn't in the CONTEXT
        6. If the CONTEXT is empty or insufficient, say so - never fabricate an answer

        CONTEXT FROM UPLOADED DOCUMENTS:
        {context}

        Remember: If it's not in the CONTEXT above, you cannot answer it. Be honest about limitations.
        """
    
    
    def _extract_sources(self, search_results: List[Dict]) -> List[Dict]:
        """
        Extract source information from search results

        Args:
            search_results: List of search result dictionaries

        Returns:
            List of source dictionaries
        """
        sources = []

        # Include all chunks, but group by document for better representation
        for i, result in enumerate(search_results[:self.max_sources]):
            document_id = result.get('document_id')

            source = {
                "source_number": i + 1,
                "document_name": result.get('document_name', 'Unknown'),
                "document_id": document_id,
                "chunk_index": result.get('chunk_index', 0),
                "relevance_score": result.get('combined_score') or result.get('similarity_score', 0),
                "text_preview": result.get('text', '')[:200] + "..."
            }
            sources.append(source)

        return sources
    
    
    def generate_rag_response_with_citations(
        self,
        db: Session,
        query: str,
        conversation_history: Optional[List[Dict]] = None,
        document_id: Optional[str] = None,
        top_k: int = 5,
        temperature: float = 0.7,
        max_tokens: int = 500
    ) -> Dict:
        """
        Generate RAG response with inline citations
        
        Args:
            db: Database session
            query: User query
            conversation_history: Previous conversation messages
            document_id: Optional filter by document
            top_k: Number of chunks to retrieve
            temperature: LLM temperature
            max_tokens: Maximum response tokens
            
        Returns:
            Dictionary with response, sources, and metadata
        """
        try:
            # Get base RAG response
            rag_response = self.generate_rag_response(
                db=db,
                query=query,
                conversation_history=conversation_history,
                document_id=document_id,
                top_k=top_k,
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            # Add instruction for citations in system prompt
            # This is a placeholder - full citation parsing would require
            # more sophisticated NLP or a citation-aware model
            
            return rag_response
            
        except Exception as e:
            logger.error(f"RAG with citations failed: {str(e)}")
            raise
    
    
    def evaluate_response_quality(
        self,
        query: str,
        response: str,
        sources: List[Dict]
    ) -> Dict:
        """
        Evaluate the quality of a RAG response
        
        Args:
            query: Original query
            response: Generated response
            sources: Retrieved sources
            
        Returns:
            Dictionary with quality metrics
        """
        metrics = {
            "has_sources": len(sources) > 0,
            "source_count": len(sources),
            "response_length": len(response),
            "avg_source_relevance": sum(s.get('relevance_score', 0) for s in sources) / len(sources) if sources else 0,
            "contains_source_reference": any(f"Source {i+1}" in response for i in range(len(sources)))
        }
        
        # Simple quality score (0-1)
        quality_score = 0.0
        if metrics["has_sources"]:
            quality_score += 0.3
        if metrics["source_count"] >= 3:
            quality_score += 0.2
        if metrics["avg_source_relevance"] > 0.5:
            quality_score += 0.3
        if metrics["contains_source_reference"]:
            quality_score += 0.2
        
        metrics["quality_score"] = round(quality_score, 2)
        
        return metrics


# Create singleton instance
rag_service = RAGService()