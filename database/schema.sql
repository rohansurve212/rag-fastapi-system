-- Database Schema for RAG System
-- This creates the tables for documents, chunks, and embeddings

-- Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Drop existing tables if they exist (for development)
DROP TABLE IF EXISTS document_chunks CASCADE;
DROP TABLE IF EXISTS documents CASCADE;

-- Documents table: stores metadata about uploaded documents
CREATE TABLE documents (
    id SERIAL PRIMARY KEY,
    document_id VARCHAR(50) UNIQUE NOT NULL,
    filename VARCHAR(255) NOT NULL,
    file_type VARCHAR(10) NOT NULL,
    file_size INTEGER NOT NULL,
    file_hash VARCHAR(64) UNIQUE NOT NULL,
    file_path TEXT NOT NULL,
    
    -- Content metadata
    character_count INTEGER,
    word_count INTEGER,
    page_count INTEGER,
    chunk_count INTEGER DEFAULT 0,
    
    -- Processing status
    processing_status VARCHAR(20) DEFAULT 'pending',
    error_message TEXT,
    
    -- Timestamps
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    processed_at TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Indexes
    CONSTRAINT documents_status_check CHECK (
        processing_status IN ('pending', 'processing', 'completed', 'failed')
    )
);

-- Document chunks table: stores text chunks with embeddings
CREATE TABLE document_chunks (
    id SERIAL PRIMARY KEY,
    chunk_id VARCHAR(50) UNIQUE NOT NULL,
    document_id VARCHAR(50) NOT NULL,
    
    -- Chunk content
    chunk_text TEXT NOT NULL,
    chunk_index INTEGER NOT NULL,
    
    -- Chunk metadata
    chunk_size INTEGER NOT NULL,
    
    -- Vector embedding (1536 dimensions for OpenAI text-embedding-3-small)
    embedding vector(1536),
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Foreign key
    CONSTRAINT fk_document
        FOREIGN KEY (document_id)
        REFERENCES documents(document_id)
        ON DELETE CASCADE,
    
    -- Ensure unique chunks per document
    CONSTRAINT unique_document_chunk UNIQUE (document_id, chunk_index)
);

-- Create indexes for better query performance
CREATE INDEX idx_documents_document_id ON documents(document_id);
CREATE INDEX idx_documents_status ON documents(processing_status);
CREATE INDEX idx_documents_uploaded_at ON documents(uploaded_at);
CREATE INDEX idx_documents_file_hash ON documents(file_hash);

CREATE INDEX idx_chunks_document_id ON document_chunks(document_id);
CREATE INDEX idx_chunks_chunk_id ON document_chunks(chunk_id);

-- Create HNSW index for vector similarity search
-- This enables fast nearest neighbor search on embeddings
CREATE INDEX idx_chunks_embedding ON document_chunks 
USING hnsw (embedding vector_cosine_ops)
WITH (m = 16, ef_construction = 64);

-- Create function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create trigger for documents table
CREATE TRIGGER update_documents_updated_at
    BEFORE UPDATE ON documents
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Grant permissions
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO raguser;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO raguser;

-- Insert a test document to verify the schema
INSERT INTO documents (
    document_id, 
    filename, 
    file_type, 
    file_size, 
    file_hash, 
    file_path,
    processing_status
) VALUES (
    'doc_test123',
    'test_document.txt',
    'txt',
    1024,
    'test_hash_123',
    '/app/uploads/test_document.txt',
    'completed'
);

-- Verify the schema
SELECT 
    table_name, 
    column_name, 
    data_type 
FROM information_schema.columns 
WHERE table_schema = 'public' 
    AND table_name IN ('documents', 'document_chunks')
ORDER BY table_name, ordinal_position;