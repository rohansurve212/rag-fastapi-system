# RAG FastAPI System - Developer Guide

**Version:** 1.0.0
**Last Updated:** October 2025
**Status:** Production Ready

---

## Table of Contents

1. [Overview](#1-overview)
2. [System Architecture](#2-system-architecture)
3. [Technology Stack](#3-technology-stack)
4. [Codebase Structure](#4-codebase-structure)
5. [Core Components](#5-core-components)
6. [Process Workflows](#6-process-workflows)
7. [Database Schema](#7-database-schema)
8. [API Endpoints](#8-api-endpoints)
9. [Development Setup](#9-development-setup)
10. [Testing](#10-testing)
11. [Deployment](#11-deployment)
12. [Best Practices](#12-best-practices)
13. [Troubleshooting](#13-troubleshooting)

---

## 1. Overview

### What is This System?

This is a **Retrieval-Augmented Generation (RAG)** system that allows users to:
- Upload documents (PDF, TXT)
- Ask questions about uploaded documents
- Get AI-generated answers with source citations
- Search documents semantically (by meaning, not just keywords)

### Key Capabilities

- **Document Processing**: Automatic text extraction, chunking, and embedding generation
- **Semantic Search**: Vector similarity search using OpenAI embeddings
- **RAG Chat**: Context-aware AI responses using GPT-4
- **Source Attribution**: All answers cite their sources
- **Multi-Document Synthesis**: Combines information from multiple documents

---

## 2. System Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         Client (HTTP)                            │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                      FastAPI Application                         │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌───────────┐│
│  │  Routers   │  │  Services  │  │   Parsers  │  │   Utils   ││
│  └────────────┘  └────────────┘  └────────────┘  └───────────┘│
└────────────────────────────┬────────────────────────────────────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
        ▼                    ▼                    ▼
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│  PostgreSQL  │    │   OpenAI     │    │ File System  │
│  + pgvector  │    │     API      │    │  (uploads/)  │
└──────────────┘    └──────────────┘    └──────────────┘
```

### Component Layers

1. **Presentation Layer** (Routers): HTTP endpoints, request/response handling
2. **Business Logic Layer** (Services): Core application logic
3. **Data Access Layer** (Database CRUD): Database operations
4. **External Services Layer**: OpenAI API integration
5. **Storage Layer**: PostgreSQL + File System

### Design Patterns Used

- **Dependency Injection**: FastAPI's `Depends()` for database sessions
- **Service Layer Pattern**: Business logic separated from routes
- **Repository Pattern**: CRUD operations abstracted from business logic
- **Singleton Pattern**: Single instances of services (openai_service, search_service)
- **Background Tasks**: Async document processing using FastAPI BackgroundTasks

---

## 3. Technology Stack

### Core Technologies

| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| **Web Framework** | FastAPI | 0.104.1 | REST API framework |
| **Web Server** | Uvicorn | 0.24.0 | ASGI server |
| **Database** | PostgreSQL | 16 | Primary database |
| **Vector Extension** | pgvector | Latest | Vector similarity search |
| **ORM** | SQLAlchemy | 2.0.23 | Database ORM |
| **AI/ML** | OpenAI API | 2.5.0+ | GPT-4 & Embeddings |
| **PDF Processing** | PyPDF2 | 3.0.1 | PDF text extraction |
| **Containerization** | Docker | Latest | Application deployment |

### Key Libraries

- **pydantic**: Data validation and settings management
- **asyncpg**: Async PostgreSQL driver
- **python-multipart**: File upload handling
- **aiofiles**: Async file operations

---

## 4. Codebase Structure

### Directory Layout

```
rag-fastapi-system/
│
├── main.py                    # FastAPI application entry point
├── config.py                  # Configuration and environment variables
├── models.py                  # Pydantic models for API request/response
├── requirements.txt           # Python dependencies
├── Dockerfile                 # Docker container definition
├── docker-compose.yml         # Multi-container orchestration
├── Makefile                   # Common commands and shortcuts
├── init.sql                   # Database initialization SQL
│
├── routers/                   # API endpoint definitions
│   ├── __init__.py
│   ├── chat.py               # Basic chat endpoints (non-RAG)
│   ├── documents.py          # Document management endpoints
│   ├── rag.py                # RAG chat endpoints
│   └── search.py             # Search endpoints
│
├── services/                  # Business logic layer
│   ├── __init__.py
│   ├── openai_service.py     # OpenAI API integration
│   ├── search_service.py     # Search functionality
│   ├── rag_service.py        # RAG pipeline implementation
│   └── background_tasks.py   # Background processing
│
├── database/                  # Database layer
│   ├── __init__.py
│   ├── connection.py         # Database connection & session management
│   ├── models.py             # SQLAlchemy models
│   ├── crud.py               # CRUD operations
│   └── schema.sql            # Database schema definitions
│
├── parsers/                   # Document parsers
│   ├── __init__.py
│   ├── text_parser.py        # Plain text parsing
│   └── pdf_parser.py         # PDF parsing with OCR support
│
├── utils/                     # Utility functions
│   ├── __init__.py
│   ├── file_handler.py       # File upload/validation
│   └── text_chunker.py       # Text chunking logic
│
├── uploads/                   # Uploaded files storage
│
├── test_*.py                  # Test scripts
│
└── PHASE*_SETUP.md           # Phase-specific documentation
```

### File Responsibilities

#### Core Application Files

- **`main.py`**: Application initialization, middleware, startup/shutdown events
- **`config.py`**: Environment configuration using Pydantic Settings
- **`models.py`**: Request/response schemas for API endpoints

#### Routers (API Endpoints)

Each router handles a specific domain:

- **`chat.py`**: Standard GPT-4 chat without document context
- **`documents.py`**: Upload, list, retrieve, delete documents
- **`rag.py`**: RAG-powered chat with document retrieval
- **`search.py`**: Semantic, keyword, and hybrid search

#### Services (Business Logic)

- **`openai_service.py`**:
  - GPT-4 chat completions
  - Embedding generation (with batching)
  - API connection management

- **`search_service.py`**:
  - Semantic search (vector similarity)
  - Keyword search (text matching)
  - Hybrid search (combined scoring)

- **`rag_service.py`**:
  - Context retrieval
  - Prompt construction
  - Response generation
  - Source extraction

- **`background_tasks.py`**:
  - Document processing pipeline
  - Chunk generation
  - Embedding creation

#### Database Layer

- **`connection.py`**: Connection pooling, session management
- **`models.py`**: SQLAlchemy ORM models (Document, DocumentChunk)
- **`crud.py`**: Create, Read, Update, Delete operations

---

## 5. Core Components

### 5.1 Configuration Management (`config.py`)

**Purpose**: Centralized configuration using environment variables

**Key Features**:
- Pydantic Settings for validation
- `.env` file support
- Type-safe configuration
- Custom field validators

**Important Settings**:

```python
class Settings(BaseSettings):
    # OpenAI
    openai_api_key: str
    openai_model: str = "gpt-4"
    openai_embedding_model: str = "text-embedding-3-small"

    # Database
    database_url: str

    # File Upload
    max_upload_size: int = 10485760  # 10MB
    allowed_extensions: List[str] = [".txt", ".pdf"]

    # Vector Search
    embedding_dimension: int = 1536
    top_k_results: int = 5

    # Text Chunking
    chunk_size: int = 1000
    chunk_overlap: int = 200
```

### 5.2 Database Models (`database/models.py`)

#### Document Model

Stores document metadata:

```python
class Document(Base):
    __tablename__ = "documents"

    document_id: str (PK)
    filename: str
    file_type: str
    file_size: int
    file_hash: str (UNIQUE)
    file_path: str
    character_count: int
    word_count: int
    page_count: int
    chunk_count: int
    processing_status: str  # pending, processing, completed, failed
    uploaded_at: datetime
    updated_at: datetime
```

#### DocumentChunk Model

Stores text chunks with embeddings:

```python
class DocumentChunk(Base):
    __tablename__ = "document_chunks"

    chunk_id: str (PK)
    document_id: str (FK -> documents.document_id)
    chunk_index: int
    chunk_text: str
    chunk_size: int
    embedding: Vector(1536)  # pgvector type
    created_at: datetime
```

**Key Relationships**:
- One Document → Many DocumentChunks
- Cascade delete: Deleting a document deletes all its chunks

### 5.3 OpenAI Service (`services/openai_service.py`)

**Singleton Service**: `openai_service = OpenAIService()`

**Methods**:

1. **`chat_completion(messages, temperature, max_tokens)`**
   - Generates GPT-4 responses
   - Supports conversation history
   - Returns: response text, token count, model

2. **`create_embedding(text)`**
   - Creates single text embedding
   - Returns: 1536-dimensional vector

3. **`create_embeddings_batch(texts, batch_size=100)`**
   - Batch embedding generation
   - **Critical**: Automatically batches to avoid 300k token limit
   - Returns: List of embedding vectors

4. **`test_connection()`**
   - Validates API connectivity
   - Returns: boolean

**Important Implementation Details**:

```python
# Batching to avoid OpenAI API limits
def create_embeddings_batch(self, texts: List[str], batch_size: int = 100):
    all_embeddings = []
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]
        response = self.client.embeddings.create(
            model=self.embedding_model,
            input=batch
        )
        all_embeddings.extend([item.embedding for item in response.data])
    return all_embeddings
```

### 5.4 Search Service (`services/search_service.py`)

**Singleton Service**: `search_service = SearchService()`

**Search Types**:

1. **Semantic Search**:
   - Uses cosine similarity on embeddings
   - Finds conceptually similar content
   - Query → Embedding → Vector search in DB

2. **Keyword Search**:
   - SQL LIKE query (case-insensitive)
   - Finds exact text matches
   - Simple relevance scoring by frequency

3. **Hybrid Search** (Recommended):
   - Combines semantic (70%) + keyword (30%)
   - Best of both worlds
   - Normalized combined scoring

**Methods**:

```python
# Semantic search
semantic_search(db, query, top_k=5, document_id=None, min_similarity=0.0)

# Keyword search
keyword_search(db, query, top_k=5, document_id=None)

# Hybrid search (recommended)
hybrid_search(db, query, top_k=5, document_id=None,
              semantic_weight=0.7, keyword_weight=0.3)

# Search with context
search_with_context(db, query, top_k=5, context_window=1)

# Statistics
get_search_statistics(db)
```

### 5.5 RAG Service (`services/rag_service.py`)

**Singleton Service**: `rag_service = RAGService()`

**Purpose**: Implements the complete RAG pipeline

**Configuration**:
- `max_context_length = 6000` characters
- `max_sources = 10` chunks

**Core Method**: `generate_rag_response()`

**RAG Pipeline Steps**:

```python
def generate_rag_response(db, query, conversation_history=None,
                         document_id=None, top_k=8,
                         temperature=0.7, max_tokens=500):

    # Step 1: Retrieve relevant context
    search_results, context = retrieve_context(
        db, query, top_k, document_id
    )

    # Step 2: Check if documents exist
    if not search_results:
        return "No documents available" message

    # Step 3: Build system prompt with context
    system_prompt = build_system_prompt(context)

    # Step 4: Build messages with history
    messages = [system_prompt] + conversation_history + [query]

    # Step 5: Generate response with GPT-4
    completion = openai_service.chat_completion(messages)

    # Step 6: Extract and format sources
    sources = extract_sources(search_results)

    return {
        "answer": completion["response"],
        "sources": sources,
        "context_used": len(search_results),
        "model": completion["model"],
        "tokens_used": completion["tokens_used"]
    }
```

**Critical Features**:

1. **Context Assembly**:
   ```python
   def _assemble_context(search_results):
       context_parts = []
       for i, result in enumerate(search_results):
           context_part = f"[Source {i+1}: {document_name}]\n{text}\n"
           context_parts.append(context_part)
       return "\n".join(context_parts)
   ```

2. **Hallucination Prevention**:
   - Empty results check
   - Strict system prompt
   - Source citation requirements

3. **System Prompt**:
   ```
   CRITICAL RULES - DO NOT VIOLATE:
   1. Answer ONLY using information from the CONTEXT below
   2. If context doesn't contain answer, say so
   3. ALWAYS cite sources
   4. DO NOT make up document names or content
   5. If CONTEXT is empty, say so - never fabricate
   ```

### 5.6 Background Tasks (`services/background_tasks.py`)

**Purpose**: Async document processing after upload

**Process Flow**:

```python
async def process_document(document_id, file_path, filename, file_type):

    # Step 1: Update status to 'processing'
    update_document_status(document_id, 'processing')

    # Step 2: Parse document (extract text)
    if file_type == 'txt':
        result = text_parser.parse(file_path)
    elif file_type == 'pdf':
        result = pdf_parser.parse(file_path, use_ocr=True)

    # Step 3: Chunk text
    chunks = text_chunker.chunk_text(
        result['content'],
        preserve_paragraphs=True
    )

    # Step 4: Generate embeddings (batched!)
    embeddings = openai_service.create_embeddings_batch(chunks)

    # Step 5: Store chunks in database
    for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
        ChunkCRUD.create_chunk(
            db, document_id, i, chunk, embedding
        )

    # Step 6: Update document metadata
    DocumentCRUD.update_document(
        db, document_id,
        chunk_count=len(chunks),
        processing_status='completed'
    )
```

**Error Handling**:
- Failures set status to 'failed'
- Logs errors for debugging
- Document remains in database for retry

### 5.7 Text Chunker (`utils/text_chunker.py`)

**Purpose**: Split documents into searchable chunks

**Strategy**: Recursive Character Text Splitter

**Configuration**:
- `chunk_size = 1000` characters
- `chunk_overlap = 200` characters (for context continuity)

**Methods**:

```python
def chunk_text(text, preserve_paragraphs=True):
    # Split by paragraphs first
    paragraphs = text.split('\n\n')

    chunks = []
    for paragraph in paragraphs:
        if len(paragraph) <= chunk_size:
            chunks.append(paragraph)
        else:
            # Split large paragraphs with overlap
            sub_chunks = split_with_overlap(paragraph)
            chunks.extend(sub_chunks)

    return chunks
```

**Why Chunking?**
- Embeddings work best on focused text
- Enables precise source attribution
- Optimizes retrieval relevance
- Manages token limits

---

## 6. Process Workflows

### 6.1 Document Upload & Processing Workflow

```
┌─────────────────────────────────────────────────────────────┐
│ 1. CLIENT: POST /api/v1/documents/upload (multipart/form)  │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. ROUTER (documents.py): upload_document()                │
│    - Validate file type (.txt, .pdf)                        │
│    - Validate file size (<= 10MB)                           │
│    - Save file to uploads/ directory                        │
│    - Calculate file hash (SHA-256)                          │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. CHECK DUPLICATE: DocumentCRUD.get_document_by_hash()    │
│    If exists → Return existing document                     │
│    If new → Continue to Step 4                              │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│ 4. PARSE DOCUMENT: Extract text + metadata                 │
│    - TXT: text_parser.parse()                              │
│    - PDF: pdf_parser.parse() (with OCR if needed)          │
│    Result: {content, character_count, word_count, ...}     │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│ 5. CREATE DB RECORD: DocumentCRUD.create_document()        │
│    - Generate document_id                                   │
│    - Store metadata                                         │
│    - Set processing_status = 'pending'                      │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│ 6. BACKGROUND TASK: BackgroundTasks.add_task()             │
│    - Return 201 response immediately to client              │
│    - Process document asynchronously                        │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│ 7. BACKGROUND PROCESSING:                                   │
│    a) Update status → 'processing'                          │
│    b) Chunk text (text_chunker.chunk_text())               │
│    c) Generate embeddings (batched, 100 per API call)       │
│    d) Store chunks with embeddings in DB                    │
│    e) Update document: chunk_count, status → 'completed'    │
└─────────────────────────────────────────────────────────────┘
```

**Timeline**:
- Immediate (Steps 1-6): ~1-2 seconds
- Background (Step 7):
  - Small files (< 5 pages): ~5-10 seconds
  - Large files (500+ pages): ~2-5 minutes

### 6.2 RAG Chat Query Workflow

```
┌─────────────────────────────────────────────────────────────┐
│ 1. CLIENT: POST /api/v1/rag/chat                           │
│    Body: {query, top_k, document_id?, temperature, ...}    │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. ROUTER (rag.py): rag_chat()                             │
│    - Validate request (Pydantic)                            │
│    - Get database session                                   │
│    - Call rag_service.generate_rag_response()              │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. RAG SERVICE: retrieve_context()                         │
│    a) Generate query embedding via OpenAI                   │
│    b) Perform hybrid search (semantic + keyword)            │
│    c) Retrieve top_k most relevant chunks                   │
│    d) Assemble context with source attribution             │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│ 4. CHECK RESULTS: if no chunks found                       │
│    → Return "No documents available" message                │
│    Otherwise → Continue                                     │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│ 5. BUILD PROMPT:                                            │
│    System: "Answer ONLY from CONTEXT below..."             │
│    Context: "[Source 1: doc.txt]\nText...\n[Source 2...]"  │
│    History: Previous conversation messages (optional)       │
│    User Query: Current question                             │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│ 6. OPENAI: Generate response with GPT-4                    │
│    - Send messages array to OpenAI                          │
│    - Receive: answer, token count, model                    │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│ 7. EXTRACT SOURCES: Format source information              │
│    For each chunk used:                                     │
│    - source_number, document_name, chunk_index              │
│    - relevance_score, text_preview                          │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│ 8. RETURN RESPONSE:                                         │
│    {                                                        │
│      answer: "GPT-4 response citing sources",              │
│      sources: [{doc_name, score, preview}, ...],           │
│      context_used: 5,                                       │
│      model: "gpt-4-0613",                                   │
│      tokens_used: 432                                       │
│    }                                                        │
└─────────────────────────────────────────────────────────────┘
```

**Performance**:
- Query embedding: ~200-500ms
- Vector search: ~100-300ms
- GPT-4 response: ~1-3 seconds
- **Total**: ~2-4 seconds

### 6.3 Semantic Search Workflow

```
Query → Embedding → Vector Search → Ranked Results

1. Convert query to embedding (OpenAI)
2. Execute pgvector similarity search:
   SELECT chunk_id, document_id, chunk_text,
          1 - (embedding <=> query_embedding) AS similarity
   FROM document_chunks
   WHERE similarity > min_threshold
   ORDER BY similarity DESC
   LIMIT top_k
3. Join with documents table for metadata
4. Format and return results with scores
```

**Vector Similarity**:
- Uses cosine similarity (via `<=>` operator)
- Scores: 0.0 (dissimilar) to 1.0 (identical)
- Typical good matches: 0.3+

---

## 7. Database Schema

### Tables

#### `documents`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| document_id | VARCHAR(50) | PRIMARY KEY | Unique identifier (doc_xxxxx) |
| filename | VARCHAR(255) | NOT NULL | Original filename |
| file_type | VARCHAR(10) | NOT NULL | 'txt' or 'pdf' |
| file_size | INTEGER | NOT NULL | Size in bytes |
| file_hash | VARCHAR(64) | UNIQUE, NOT NULL | SHA-256 hash for deduplication |
| file_path | TEXT | NOT NULL | Server file path |
| character_count | INTEGER | | Total characters |
| word_count | INTEGER | | Total words |
| page_count | INTEGER | | Pages (PDF only) |
| chunk_count | INTEGER | DEFAULT 0 | Number of chunks created |
| processing_status | VARCHAR(20) | DEFAULT 'pending' | pending/processing/completed/failed |
| uploaded_at | TIMESTAMP | DEFAULT NOW() | Upload timestamp |
| updated_at | TIMESTAMP | DEFAULT NOW() | Last update timestamp |

#### `document_chunks`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| chunk_id | VARCHAR(100) | PRIMARY KEY | chunk_doc_xxxxx_N |
| document_id | VARCHAR(50) | FOREIGN KEY, NOT NULL | References documents(document_id) |
| chunk_index | INTEGER | NOT NULL | Chunk number (0-based) |
| chunk_text | TEXT | NOT NULL | Text content |
| chunk_size | INTEGER | | Character count |
| embedding | VECTOR(1536) | | OpenAI embedding |
| created_at | TIMESTAMP | DEFAULT NOW() | Creation timestamp |

**Indexes**:
- `idx_document_chunks_document_id`: Fast lookup by document
- `idx_document_chunks_embedding`: Vector similarity search (HNSW)
- `idx_documents_hash`: Fast duplicate detection

**Foreign Key Behavior**:
- ON DELETE CASCADE: Deleting a document deletes all its chunks

### pgvector Extension

**Installation**:
```sql
CREATE EXTENSION IF NOT EXISTS vector;
```

**Vector Operations**:
- `<=>`: Cosine distance (used for similarity)
- `<->`: Euclidean distance
- `<#>`: Inner product

**Example Query**:
```sql
SELECT chunk_id,
       1 - (embedding <=> '[0.1, 0.2, ...]'::vector) AS similarity
FROM document_chunks
ORDER BY embedding <=> '[0.1, 0.2, ...]'::vector
LIMIT 5;
```

---

## 8. API Endpoints

### Complete Endpoint Reference

#### Health & Status

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Welcome message + endpoint list |
| GET | `/health` | Health check |
| GET | `/api/v1/status` | Detailed API status |
| GET | `/api/v1/rag/health` | RAG system health + statistics |

#### Document Management

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/documents/upload` | Upload document (multipart/form-data) |
| GET | `/api/v1/documents/` | List all documents (with pagination) |
| GET | `/api/v1/documents/{id}` | Get document details |
| GET | `/api/v1/documents/{id}/chunks` | Get document chunks |
| DELETE | `/api/v1/documents/{id}` | Delete document + chunks |

#### Search

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/search/semantic` | Semantic vector search |
| GET | `/api/v1/search/keyword` | Keyword text search |
| GET | `/api/v1/search/hybrid` | Combined search (recommended) |
| GET | `/api/v1/search/stats` | Search statistics |

#### Chat

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/chat` | Basic GPT-4 chat (no RAG) |
| POST | `/api/v1/rag/chat` | RAG-powered chat (with documents) |

#### Testing (Development)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/documents/test/parse-text` | Test text parser |
| GET | `/api/v1/documents/test/chunking` | Test text chunking |

### Interactive Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

---

## 9. Development Setup

### Prerequisites

- Docker & Docker Compose
- Git
- OpenAI API key

### Initial Setup

```bash
# 1. Clone repository
git clone <repo-url>
cd rag-fastapi-system

# 2. Create .env file
cp .env.example .env

# 3. Add your OpenAI API key to .env
# Edit .env and set:
OPENAI_API_KEY=your_api_key_here

# 4. Build and start containers
make build
make up

# Or combined:
docker-compose up --build -d

# 5. Verify services are running
make status
# or
docker-compose ps

# 6. Check logs
make logs-api
# or
docker logs rag-api -f
```

### Available Make Commands

```bash
make help          # Show all commands
make build         # Build Docker containers
make up            # Start services
make down          # Stop services
make restart       # Restart services
make logs          # View all logs
make logs-api      # View API logs only
make logs-db       # View database logs only
make test-chat     # Run chat tests
make test-database # Run database tests
make shell-api     # Open shell in API container
make shell-db      # Open PostgreSQL shell
make clean         # Remove everything (containers + volumes)
```

### Local Development (Without Docker)

```bash
# 1. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set environment variables
export DATABASE_URL="postgresql://raguser:ragpassword@localhost:5432/ragdb"
export OPENAI_API_KEY="your_key"

# 4. Start PostgreSQL (with pgvector)
# You'll need to install PostgreSQL 16 + pgvector extension

# 5. Run application
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Environment Variables

Create `.env` file with:

```env
# Required
OPENAI_API_KEY=sk-proj-xxxxx

# Optional (have defaults)
OPENAI_MODEL=gpt-4
OPENAI_EMBEDDING_MODEL=text-embedding-3-small
DATABASE_URL=postgresql://raguser:ragpassword@db:5432/ragdb
MAX_UPLOAD_SIZE=10485760
ALLOWED_EXTENSIONS=.txt,.pdf
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
TOP_K_RESULTS=5
```

---

## 10. Testing

### Test Files

| File | Purpose |
|------|---------|
| `test_chat.py` | Tests basic chat endpoint |
| `test_database.py` | Tests database operations + CRUD |
| `test_documents.py` | Tests document upload + processing |
| `test_rag.py` | Tests RAG chat functionality |
| `test_search.py` | Tests search endpoints |

### Running Tests

```bash
# Run all tests
make test-chat
make test-database
docker-compose exec api python test_rag.py
docker-compose exec api python test_search.py

# Or manually:
docker-compose exec api python test_chat.py
```

### Manual Testing with curl

```bash
# Health check
curl http://localhost:8000/health

# Upload document
curl -X POST http://localhost:8000/api/v1/documents/upload \
  -F "file=@test.txt"

# List documents
curl http://localhost:8000/api/v1/documents/

# RAG chat
curl -X POST http://localhost:8000/api/v1/rag/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "What is FastAPI?", "top_k": 5}'

# Semantic search
curl "http://localhost:8000/api/v1/search/semantic?query=python&top_k=3"
```

### Testing Checklist

- [ ] Health endpoints respond correctly
- [ ] Document upload (TXT and PDF)
- [ ] Document processing completes
- [ ] Semantic search returns relevant results
- [ ] RAG chat provides accurate answers with sources
- [ ] Document deletion cascades to chunks
- [ ] Error handling works (empty queries, invalid files)
- [ ] Large documents process successfully (batching)

---

## 11. Deployment

### Docker Deployment (Production)

```bash
# 1. Update .env for production
ENVIRONMENT=production
API_RELOAD=False

# 2. Use production docker-compose
docker-compose -f docker-compose.prod.yml up -d

# 3. Set up reverse proxy (nginx)
# Point to port 8000 with SSL

# 4. Set up monitoring
# - Application logs
# - Database backups
# - API usage metrics
```

### Environment Considerations

**Development**:
- API reload enabled
- Debug logging
- Localhost access

**Production**:
- API reload disabled
- Info/Warning logging only
- Proper CORS configuration
- Rate limiting (recommended)
- API key authentication (recommended)
- HTTPS only

### Scaling Considerations

**Horizontal Scaling**:
- Multiple API containers behind load balancer
- Shared PostgreSQL instance
- Shared file storage (NFS or S3)

**Vertical Scaling**:
- Database: Increase memory for vector search
- API: Increase CPU for concurrent requests

**Optimization**:
- Redis caching for embeddings
- Connection pooling (already configured)
- Async file operations (already implemented)

---

## 12. Best Practices

### Code Style

- **Python**: PEP 8
- **Type Hints**: Use throughout
- **Docstrings**: Google style
- **Imports**: Group by standard/third-party/local

### Error Handling

```python
# Always use specific exceptions
try:
    result = operation()
except OpenAIError as e:
    logger.error(f"OpenAI error: {e}")
    raise HTTPException(status_code=500, detail=str(e))
except ValueError as e:
    logger.error(f"Validation error: {e}")
    raise HTTPException(status_code=400, detail=str(e))
```

### Logging

```python
# Use appropriate log levels
logger.debug("Detailed debugging info")
logger.info("Important business logic events")
logger.warning("Recoverable issues")
logger.error("Errors requiring attention")
```

### Database Sessions

```python
# Always use dependency injection
@router.get("/items")
async def get_items(db: Session = Depends(get_db)):
    items = ItemCRUD.get_all(db)
    return items

# Sessions auto-close via finally block
```

### API Design

- Use appropriate HTTP methods (GET, POST, DELETE)
- Return correct status codes (200, 201, 404, 500)
- Include response models for validation
- Document with docstrings (auto-generates API docs)

### Security Best Practices

1. **Never commit** `.env` files
2. **Validate** all user inputs (Pydantic does this)
3. **Sanitize** file uploads (check extensions, size)
4. **Rate limit** endpoints (implement as middleware)
5. **Use HTTPS** in production
6. **Rotate** API keys regularly
7. **Hash** file contents for deduplication (already done)

---

## 13. Troubleshooting

### Common Issues

#### 1. Database Connection Failed

**Symptoms**: API logs show database connection errors

**Solutions**:
```bash
# Check database is running
docker-compose ps

# Check database logs
docker logs rag-database

# Verify connection string in .env
DATABASE_URL=postgresql://raguser:ragpassword@db:5432/ragdb

# Restart database
docker-compose restart db
```

#### 2. OpenAI API Errors

**Symptoms**: 401 Unauthorized, 429 Rate Limit

**Solutions**:
```bash
# Verify API key in .env
echo $OPENAI_API_KEY

# Check OpenAI dashboard for usage/limits
# https://platform.openai.com/usage

# For rate limits, implement exponential backoff
```

#### 3. Document Processing Stuck

**Symptoms**: Documents stay in 'processing' status

**Solutions**:
```bash
# Check API logs for errors
docker logs rag-api | grep -i error

# Check document status
curl http://localhost:8000/api/v1/documents/{document_id}

# Common causes:
# - Large PDF (2000+ chunks) → Increase timeout
# - OpenAI rate limit → Wait and retry
# - OCR failure → Check tesseract installation
```

#### 4. Empty Search Results

**Symptoms**: RAG chat says "no documents available"

**Solutions**:
```bash
# Check RAG health
curl http://localhost:8000/api/v1/rag/health

# Verify chunks exist
SELECT COUNT(*) FROM document_chunks;

# Check embeddings
SELECT COUNT(*) FROM document_chunks WHERE embedding IS NOT NULL;

# If chunks missing, reprocess documents
```

#### 5. Slow Performance

**Symptoms**: Queries take > 10 seconds

**Solutions**:
- Check database indexes exist
- Reduce `top_k` parameter
- Optimize chunk size (smaller = faster search)
- Add database connection pooling (already configured)
- Consider caching frequently searched embeddings

### Debug Mode

```python
# Enable debug logging in main.py
import logging
logging.basicConfig(level=logging.DEBUG)

# Or in .env
LOG_LEVEL=DEBUG
```

### Health Check Endpoints

```bash
# Overall API health
curl http://localhost:8000/health

# RAG system health (detailed)
curl http://localhost:8000/api/v1/rag/health

# Search statistics
curl http://localhost:8000/api/v1/search/stats
```

### Database Inspection

```bash
# Open PostgreSQL shell
make shell-db

# Useful queries
\dt                              # List tables
SELECT COUNT(*) FROM documents;  # Count documents
SELECT COUNT(*) FROM document_chunks;  # Count chunks

# Check document statuses
SELECT processing_status, COUNT(*)
FROM documents
GROUP BY processing_status;

# Find documents without chunks
SELECT document_id, filename, chunk_count
FROM documents
WHERE chunk_count = 0;
```

---

## Additional Resources

### Documentation Files

- `README.md`: Quick start guide
- `PHASE2_SETUP.md`: OpenAI integration details
- `PHASE3_SETUP.md`: Document upload implementation
- `PHASE4_SETUP.md`: Database & CRUD operations
- `PHASE5_SETUP.md`: Search functionality
- `PHASE6_SUMMARY.md`: Complete RAG implementation
- `QUICKSTART_PHASE*.md`: Phase-specific quick starts

### Key Concepts to Learn

1. **Vector Embeddings**: How text is converted to numbers for similarity search
2. **RAG Pattern**: Retrieval-Augmented Generation explained
3. **FastAPI**: Async Python web framework
4. **SQLAlchemy**: Python ORM
5. **pgvector**: PostgreSQL extension for vector operations
6. **OpenAI API**: GPT-4 and embeddings

### Helpful Commands Summary

```bash
# Development
make up            # Start everything
make logs-api      # Watch API logs
make restart       # Restart after code changes
make shell-api     # Debug in container

# Testing
make test-chat     # Test chat functionality
make test-database # Test DB operations

# Maintenance
make down          # Stop services
make clean         # Remove everything
docker system prune -a  # Clean Docker cache
```

---

## Contributing Guidelines

### Code Changes

1. Create feature branch: `git checkout -b feature/your-feature`
2. Make changes with clear commit messages
3. Test thoroughly (run all test scripts)
4. Update documentation if needed
5. Submit pull request with description

### Adding New Features

1. **New Endpoint**: Add to appropriate router
2. **New Service**: Create in `services/` directory
3. **New Model**: Add to `database/models.py` and `models.py`
4. **Migration**: Update `init.sql` or create migration script

### Testing New Features

- Write test script in `test_*.py`
- Test manually via API docs
- Verify logs for errors
- Check database state

---

## Glossary

- **RAG**: Retrieval-Augmented Generation - AI technique combining search + generation
- **Embedding**: Vector representation of text for similarity comparison
- **Chunk**: Segment of document text (typically 1000 characters)
- **Vector Similarity**: Measuring how similar two embeddings are
- **Cosine Similarity**: Specific similarity metric (0.0 = dissimilar, 1.0 = identical)
- **pgvector**: PostgreSQL extension for vector operations
- **CRUD**: Create, Read, Update, Delete operations
- **ORM**: Object-Relational Mapping (SQLAlchemy)
- **Singleton**: Design pattern ensuring single instance of a class

---

**Document Version**: 1.0.0
**Last Updated**: October 2025
**Maintained By**: Development Team
**Contact**: [Add contact info]

---
