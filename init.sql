-- Initialize PostgreSQL database with pgvector extension
-- This script runs automatically when the database container starts

-- Enable pgvector extension for vector similarity search
CREATE EXTENSION IF NOT EXISTS vector;

-- Note: The main schema (documents and document_chunks tables) 
-- will be created by SQLAlchemy on application startup

-- Create a simple test to verify pgvector is working
CREATE TABLE IF NOT EXISTS pgvector_test (
    id SERIAL PRIMARY KEY,
    content TEXT,
    embedding vector(1536),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert test vector
INSERT INTO pgvector_test (content, embedding) 
VALUES ('test', ARRAY(SELECT random() FROM generate_series(1, 1536))::vector(1536));

-- Grant necessary permissions
GRANT ALL PRIVILEGES ON DATABASE ragdb TO raguser;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO raguser;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO raguser;
GRANT ALL PRIVILEGES ON ALL FUNCTIONS IN SCHEMA public TO raguser;

-- Verify pgvector is installed
SELECT 'pgvector extension installed successfully' as status 
WHERE EXISTS (
    SELECT 1 FROM pg_extension WHERE extname = 'vector'
);