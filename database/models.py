from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Index
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.sql import func
from pgvector.sqlalchemy import Vector
from datetime import datetime

Base = declarative_base()


class Document(Base):
    """
    SQLAlchemy model for documents table
    """
    __tablename__ = "documents"
    
    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(String(50), unique=True, nullable=False, index=True)
    filename = Column(String(255), nullable=False)
    file_type = Column(String(10), nullable=False)
    file_size = Column(Integer, nullable=False)
    file_hash = Column(String(64), unique=True, nullable=False, index=True)
    file_path = Column(Text, nullable=False)
    
    # Content metadata
    character_count = Column(Integer)
    word_count = Column(Integer)
    page_count = Column(Integer)
    chunk_count = Column(Integer, default=0)
    
    # Processing status
    processing_status = Column(String(20), default='pending', index=True)
    error_message = Column(Text)
    
    # Timestamps
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())
    processed_at = Column(DateTime(timezone=True))
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    chunks = relationship("DocumentChunk", back_populates="document", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Document(document_id='{self.document_id}', filename='{self.filename}', status='{self.processing_status}')>"
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            "id": self.id,
            "document_id": self.document_id,
            "filename": self.filename,
            "file_type": self.file_type,
            "file_size": self.file_size,
            "file_hash": self.file_hash,
            "file_path": self.file_path,
            "character_count": self.character_count,
            "word_count": self.word_count,
            "page_count": self.page_count,
            "chunk_count": self.chunk_count,
            "processing_status": self.processing_status,
            "error_message": self.error_message,
            "uploaded_at": self.uploaded_at.isoformat() if self.uploaded_at else None,
            "processed_at": self.processed_at.isoformat() if self.processed_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }


class DocumentChunk(Base):
    """
    SQLAlchemy model for document_chunks table
    """
    __tablename__ = "document_chunks"
    
    id = Column(Integer, primary_key=True, index=True)
    chunk_id = Column(String(50), unique=True, nullable=False, index=True)
    document_id = Column(String(50), ForeignKey('documents.document_id', ondelete='CASCADE'), nullable=False, index=True)
    
    # Chunk content
    chunk_text = Column(Text, nullable=False)
    chunk_index = Column(Integer, nullable=False)
    
    # Chunk metadata
    chunk_size = Column(Integer, nullable=False)
    
    # Vector embedding (1536 dimensions for OpenAI text-embedding-3-small)
    embedding = Column(Vector(1536))
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    document = relationship("Document", back_populates="chunks")
    
    # Unique constraint for document_id + chunk_index
    __table_args__ = (
        Index('idx_document_chunk_unique', 'document_id', 'chunk_index', unique=True),
    )
    
    def __repr__(self):
        return f"<DocumentChunk(chunk_id='{self.chunk_id}', document_id='{self.document_id}', index={self.chunk_index})>"
    
    def to_dict(self, include_embedding=False):
        """Convert model to dictionary"""
        result = {
            "id": self.id,
            "chunk_id": self.chunk_id,
            "document_id": self.document_id,
            "chunk_text": self.chunk_text,
            "chunk_index": self.chunk_index,
            "chunk_size": self.chunk_size,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
        
        if include_embedding and self.embedding:
            result["embedding"] = self.embedding
        
        return result