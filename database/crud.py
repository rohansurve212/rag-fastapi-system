from sqlalchemy.orm import Session
from sqlalchemy import desc, and_, func
from typing import List, Optional, Dict
from datetime import datetime
import logging

from database.models import Document, DocumentChunk

logger = logging.getLogger(__name__)


class DocumentCRUD:
    """
    CRUD operations for documents
    """
    
    @staticmethod
    def create_document(
        db: Session,
        document_id: str,
        filename: str,
        file_type: str,
        file_size: int,
        file_hash: str,
        file_path: str,
        **kwargs
    ) -> Document:
        """
        Create a new document record
        
        Args:
            db: Database session
            document_id: Unique document identifier
            filename: Original filename
            file_type: File extension
            file_size: File size in bytes
            file_hash: SHA-256 hash
            file_path: Path to saved file
            **kwargs: Additional fields (character_count, word_count, etc.)
            
        Returns:
            Created Document object
        """
        try:
            document = Document(
                document_id=document_id,
                filename=filename,
                file_type=file_type,
                file_size=file_size,
                file_hash=file_hash,
                file_path=file_path,
                **kwargs
            )
            
            db.add(document)
            db.commit()
            db.refresh(document)
            
            logger.info(f"Document created: {document_id}")
            return document
            
        except Exception as e:
            db.rollback()
            logger.error(f"Failed to create document: {str(e)}")
            raise
    
    @staticmethod
    def get_document_by_id(db: Session, document_id: str) -> Optional[Document]:
        """
        Get document by document_id
        
        Args:
            db: Database session
            document_id: Document identifier
            
        Returns:
            Document object or None
        """
        return db.query(Document).filter(Document.document_id == document_id).first()
    
    @staticmethod
    def get_document_by_hash(db: Session, file_hash: str) -> Optional[Document]:
        """
        Get document by file hash (for deduplication)
        
        Args:
            db: Database session
            file_hash: File SHA-256 hash
            
        Returns:
            Document object or None
        """
        return db.query(Document).filter(Document.file_hash == file_hash).first()
    
    @staticmethod
    def get_all_documents(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        status: Optional[str] = None
    ) -> List[Document]:
        """
        Get all documents with optional filtering
        
        Args:
            db: Database session
            skip: Number of records to skip
            limit: Maximum records to return
            status: Filter by processing status
            
        Returns:
            List of Document objects
        """
        query = db.query(Document)
        
        if status:
            query = query.filter(Document.processing_status == status)
        
        return query.order_by(desc(Document.uploaded_at)).offset(skip).limit(limit).all()
    
    @staticmethod
    def update_document_status(
        db: Session,
        document_id: str,
        status: str,
        error_message: Optional[str] = None,
        processed_at: Optional[datetime] = None
    ) -> Optional[Document]:
        """
        Update document processing status
        
        Args:
            db: Database session
            document_id: Document identifier
            status: New status (pending, processing, completed, failed)
            error_message: Error message if status is 'failed'
            processed_at: Processing completion time
            
        Returns:
            Updated Document object or None
        """
        try:
            document = DocumentCRUD.get_document_by_id(db, document_id)
            if not document:
                return None
            
            document.processing_status = status
            if error_message:
                document.error_message = error_message
            if processed_at:
                document.processed_at = processed_at
            
            db.commit()
            db.refresh(document)
            
            logger.info(f"Document status updated: {document_id} -> {status}")
            return document
            
        except Exception as e:
            db.rollback()
            logger.error(f"Failed to update document status: {str(e)}")
            raise
    
    @staticmethod
    def update_document_chunk_count(
        db: Session,
        document_id: str,
        chunk_count: int
    ) -> Optional[Document]:
        """
        Update document chunk count
        
        Args:
            db: Database session
            document_id: Document identifier
            chunk_count: Number of chunks
            
        Returns:
            Updated Document object or None
        """
        try:
            document = DocumentCRUD.get_document_by_id(db, document_id)
            if not document:
                return None
            
            document.chunk_count = chunk_count
            db.commit()
            db.refresh(document)
            
            return document
            
        except Exception as e:
            db.rollback()
            logger.error(f"Failed to update chunk count: {str(e)}")
            raise
    
    @staticmethod
    def delete_document(db: Session, document_id: str) -> bool:
        """
        Delete document and all its chunks (cascade)
        
        Args:
            db: Database session
            document_id: Document identifier
            
        Returns:
            True if deleted, False if not found
        """
        try:
            document = DocumentCRUD.get_document_by_id(db, document_id)
            if not document:
                return False
            
            db.delete(document)
            db.commit()
            
            logger.info(f"Document deleted: {document_id}")
            return True
            
        except Exception as e:
            db.rollback()
            logger.error(f"Failed to delete document: {str(e)}")
            raise
    
    @staticmethod
    def count_documents(db: Session, status: Optional[str] = None) -> int:
        """
        Count total documents
        
        Args:
            db: Database session
            status: Filter by status (optional)
            
        Returns:
            Count of documents
        """
        query = db.query(Document)
        if status:
            query = query.filter(Document.processing_status == status)
        return query.count()


class ChunkCRUD:
    """
    CRUD operations for document chunks
    """
    
    @staticmethod
    def create_chunk(
        db: Session,
        chunk_id: str,
        document_id: str,
        chunk_text: str,
        chunk_index: int,
        embedding: Optional[List[float]] = None
    ) -> DocumentChunk:
        """
        Create a new document chunk
        
        Args:
            db: Database session
            chunk_id: Unique chunk identifier
            document_id: Parent document ID
            chunk_text: Text content of chunk
            chunk_index: Position in document
            embedding: Vector embedding (optional)
            
        Returns:
            Created DocumentChunk object
        """
        try:
            chunk = DocumentChunk(
                chunk_id=chunk_id,
                document_id=document_id,
                chunk_text=chunk_text,
                chunk_index=chunk_index,
                chunk_size=len(chunk_text),
                embedding=embedding
            )
            
            db.add(chunk)
            db.commit()
            db.refresh(chunk)
            
            logger.info(f"Chunk created: {chunk_id}")
            return chunk
            
        except Exception as e:
            db.rollback()
            logger.error(f"Failed to create chunk: {str(e)}")
            raise
    
    @staticmethod
    def create_chunks_batch(
        db: Session,
        chunks_data: List[Dict]
    ) -> List[DocumentChunk]:
        """
        Create multiple chunks in a batch
        
        Args:
            db: Database session
            chunks_data: List of chunk dictionaries
            
        Returns:
            List of created DocumentChunk objects
        """
        try:
            chunks = []
            for data in chunks_data:
                chunk = DocumentChunk(**data)
                chunks.append(chunk)
            
            db.add_all(chunks)
            db.commit()
            
            for chunk in chunks:
                db.refresh(chunk)
            
            logger.info(f"Batch created {len(chunks)} chunks")
            return chunks
            
        except Exception as e:
            db.rollback()
            logger.error(f"Failed to create chunks batch: {str(e)}")
            raise
    
    @staticmethod
    def get_chunk_by_id(db: Session, chunk_id: str) -> Optional[DocumentChunk]:
        """
        Get chunk by chunk_id
        
        Args:
            db: Database session
            chunk_id: Chunk identifier
            
        Returns:
            DocumentChunk object or None
        """
        return db.query(DocumentChunk).filter(DocumentChunk.chunk_id == chunk_id).first()
    
    @staticmethod
    def get_chunks_by_document(
        db: Session,
        document_id: str
    ) -> List[DocumentChunk]:
        """
        Get all chunks for a document
        
        Args:
            db: Database session
            document_id: Document identifier
            
        Returns:
            List of DocumentChunk objects ordered by chunk_index
        """
        return db.query(DocumentChunk).filter(
            DocumentChunk.document_id == document_id
        ).order_by(DocumentChunk.chunk_index).all()
    
    @staticmethod
    def update_chunk_embedding(
        db: Session,
        chunk_id: str,
        embedding: List[float]
    ) -> Optional[DocumentChunk]:
        """
        Update chunk embedding
        
        Args:
            db: Database session
            chunk_id: Chunk identifier
            embedding: Vector embedding
            
        Returns:
            Updated DocumentChunk object or None
        """
        try:
            chunk = ChunkCRUD.get_chunk_by_id(db, chunk_id)
            if not chunk:
                return None
            
            chunk.embedding = embedding
            db.commit()
            db.refresh(chunk)
            
            logger.info(f"Chunk embedding updated: {chunk_id}")
            return chunk
            
        except Exception as e:
            db.rollback()
            logger.error(f"Failed to update chunk embedding: {str(e)}")
            raise
    
    @staticmethod
    def search_similar_chunks(
        db: Session,
        query_embedding: List[float],
        limit: int = 5,
        document_id: Optional[str] = None
    ) -> List[tuple]:
        """
        Search for similar chunks using vector similarity
        
        Args:
            db: Database session
            query_embedding: Query vector
            limit: Maximum results to return
            document_id: Filter by document (optional)
            
        Returns:
            List of tuples (DocumentChunk, similarity_score)
        """
        try:
            # Calculate cosine distance (1 - cosine similarity)
            # Lower distance = more similar
            distance = DocumentChunk.embedding.cosine_distance(query_embedding)
            
            query = db.query(
                DocumentChunk,
                distance.label('distance')
            ).filter(
                DocumentChunk.embedding.isnot(None)
            )
            
            if document_id:
                query = query.filter(DocumentChunk.document_id == document_id)
            
            results = query.order_by(distance).limit(limit).all()
            
            # Convert distance to similarity score (1 - distance)
            results_with_score = [
                (chunk, 1 - dist) for chunk, dist in results
            ]
            
            return results_with_score
            
        except Exception as e:
            logger.error(f"Failed to search similar chunks: {str(e)}")
            raise
    
    @staticmethod
    def delete_chunks_by_document(db: Session, document_id: str) -> int:
        """
        Delete all chunks for a document
        
        Args:
            db: Database session
            document_id: Document identifier
            
        Returns:
            Number of chunks deleted
        """
        try:
            count = db.query(DocumentChunk).filter(
                DocumentChunk.document_id == document_id
            ).delete()
            
            db.commit()
            logger.info(f"Deleted {count} chunks for document: {document_id}")
            return count
            
        except Exception as e:
            db.rollback()
            logger.error(f"Failed to delete chunks: {str(e)}")
            raise
    
    @staticmethod
    def count_chunks(db: Session, document_id: Optional[str] = None) -> int:
        """
        Count total chunks
        
        Args:
            db: Database session
            document_id: Filter by document (optional)
            
        Returns:
            Count of chunks
        """
        query = db.query(DocumentChunk)
        if document_id:
            query = query.filter(DocumentChunk.document_id == document_id)
        return query.count()
    
    @staticmethod
    def get_chunks_without_embeddings(
        db: Session,
        limit: int = 100
    ) -> List[DocumentChunk]:
        """
        Get chunks that don't have embeddings yet
        
        Args:
            db: Database session
            limit: Maximum number of chunks to return
            
        Returns:
            List of DocumentChunk objects without embeddings
        """
        return db.query(DocumentChunk).filter(
            DocumentChunk.embedding.is_(None)
        ).limit(limit).all()
    
    @staticmethod
    def count_chunks_with_embeddings(db: Session) -> int:
        """
        Count chunks that have embeddings
        
        Args:
            db: Database session
            
        Returns:
            Count of chunks with embeddings
        """
        return db.query(DocumentChunk).filter(
            DocumentChunk.embedding.isnot(None)
        ).count()
    
    @staticmethod
    def get_all_chunks(
        db: Session,
        skip: int = 0,
        limit: int = 100
    ) -> List[DocumentChunk]:
        """
        Get all chunks with pagination
        
        Args:
            db: Database session
            skip: Number of records to skip
            limit: Maximum records to return
            
        Returns:
            List of DocumentChunk objects
        """
        return db.query(DocumentChunk).order_by(
            DocumentChunk.created_at.desc()
        ).offset(skip).limit(limit).all()