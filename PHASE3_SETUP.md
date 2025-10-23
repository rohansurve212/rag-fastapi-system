# Phase 3: Document Upload & Storage

## Overview

Phase 3 adds document ingestion capabilities to the RAG System. Users can now upload text and PDF documents, which are parsed, chunked, and prepared for semantic search in future phases.

## What's New in Phase 3

### New Files Created

1. **utils/file_handler.py** - File handling and validation utilities
2. **utils/text_chunker.py** - Document chunking with overlap strategy
3. **utils/__init__.py** - Utils package initialization
4. **parsers/text_parser.py** - Plain text file parser
5. **parsers/pdf_parser.py** - PDF parser with OCR support
6. **parsers/__init__.py** - Parsers package initialization
7. **routers/documents.py** - Document upload and management endpoints
8. **test_documents.py** - Comprehensive test script for Phase 3
9. **PHASE3_SETUP.md** - This file

### Updated Files

1. **models.py** - Added document-related Pydantic models
2. **routers/__init__.py** - Added documents router
3. **main.py** - Included documents router and updated endpoints
4. **Makefile** - Added `test-documents` and `test-all` commands

## File Structure After Phase 3

```
rag-fastapi-system/
├── main.py                      # Updated with documents router
├── config.py                    # Configuration (unchanged)
├── models.py                    # Updated with document models
├── requirements.txt             # Dependencies (unchanged)
├── Dockerfile                   # Container config (unchanged)
├── docker-compose.yml           # Docker Compose (unchanged)
├── init.sql                     # Database init (unchanged)
├── .env                         # Environment variables
├── .env.example                 # Env template (unchanged)
├── .gitignore                   # Git ignore (unchanged)
├── README.md                    # Main documentation
├── PHASE2_SETUP.md              # Phase 2 docs
├── PHASE3_SETUP.md              # NEW: This file
├── test_api.sh                  # Phase 1 tests
├── test_chat.py                 # Phase 2 tests
├── test_documents.py            # NEW: Phase 3 tests
├── Makefile                     # Updated with new commands
├── services/                    # Services (from Phase 2)
│   ├── __init__.py
│   └── openai_service.py
├── routers/                     # Routers (updated)
│   ├── __init__.py             # Updated
│   ├── chat.py
│   └── documents.py            # NEW
├── utils/                       # NEW: Utilities directory
│   ├── __init__.py
│   ├── file_handler.py         # NEW
│   └── text_chunker.py         # NEW
├── parsers/                     # NEW: Parsers directory
│   ├── __init__.py
│   ├── text_parser.py          # NEW
│   └── pdf_parser.py           # NEW
└── uploads/                     # Upload directory (auto-created)
```

## Installation Steps

### Step 1: Create New Directories

```bash
# Create new directories
mkdir -p utils parsers

# Create __init__.py files
touch utils/__init__.py
touch parsers/__init__.py
```

### Step 2: Create New Files

Copy content from the artifacts into these files:

1. `utils/__init__.py` ← "utils/__init__.py - Utils Package"
2. `utils/file_handler.py` ← "utils/file_handler.py - File Handling Utilities"
3. `utils/text_chunker.py` ← "utils/text_chunker.py - Document Chunking"
4. `parsers/__init__.py` ← "parsers/__init__.py - Parsers Package"
5. `parsers/text_parser.py` ← "parsers/text_parser.py - Text File Parser"
6. `parsers/pdf_parser.py` ← "parsers/pdf_parser.py - PDF Parser with OCR"
7. `routers/documents.py` ← "routers/documents.py - Document Upload Router"
8. `test_documents.py` ← "test_documents.py - Document Upload Test Script"
9. `PHASE3_SETUP.md` ← This file

### Step 3: Update Existing Files

Replace content in these files with updated versions:

1. `models.py` ← Replace with updated "models.py - Pydantic Models"
2. `routers/__init__.py` ← Replace with updated "routers/__init__.py - Routers Package"
3. `main.py` ← Replace with updated "main.py - FastAPI Application"
4. `Makefile` ← Replace with updated "Makefile - Development Commands"

### Step 4: Rebuild and Restart

```bash
# Stop containers
make down

# Rebuild with new code
make build

# Start services
make up

# Check logs
make logs-api
```

## Testing Phase 3

### Method 1: Using the Test Script (Recommended)

```bash
# Make test script executable
chmod +x test_documents.py

# Run comprehensive test suite
make test-documents
```

The test script runs 5 tests:
1. ✅ Text Parser Test
2. ✅ Text Chunking Test
3. ✅ Upload Text File
4. ✅ Upload Validation
5. ✅ Large File Validation

### Method 2: Using cURL

```bash
# Test text parser
curl http://localhost:8000/api/v1/documents/test/parse-text

# Test chunking
curl http://localhost:8000/api/v1/documents/test/chunking

# Upload a text file
curl -X POST http://localhost:8000/api/v1/documents/upload \
  -F "file=@/path/to/your/document.txt"

# Upload a PDF file
curl -X POST http://localhost:8000/api/v1/documents/upload \
  -F "file=@/path/to/your/document.pdf"
```

### Method 3: Using Swagger UI

1. Open http://localhost:8000/docs
2. Navigate to **Documents** section
3. Try these endpoints:
   - `GET /api/v1/documents/test/parse-text`
   - `GET /api/v1/documents/test/chunking`
   - `POST /api/v1/documents/upload`

## New API Endpoints

### 1. POST /api/v1/documents/upload

Upload and process a document (text or PDF).

**Request:**
- Content-Type: multipart/form-data
- Body: file (binary)

**Response:**
```json
{
  "success": true,
  "message": "Document uploaded and processed successfully",
  "document_id": "doc_abc123def456",
  "filename": "example.pdf",
  "file_size": 52428,
  "file_hash": "a1b2c3d4e5f6",
  "chunks_created": 5,
  "metadata": {
    "filename": "example.pdf",
    "file_type": "pdf",
    "file_size": 52428,
    "file_hash": "a1b2c3d4e5f6",
    "character_count": 5000,
    "word_count": 800,
    "page_count": 3,
    "chunk_count": 5,
    "uploaded_at": "2025-10-19T12:00:00"
  },
  "timestamp": "2025-10-19T12:00:00"
}
```

### 2. GET /api/v1/documents/test/parse-text

Test the text parsing functionality.

**Response:**
```json
{
  "success": true,
  "content_length": 245,
  "metadata": {
    "filename": "test.txt",
    "file_type": "text",
    "word_count": 42,
    "line_count": 8
  },
  "sample_content": "This is a test document..."
}
```

### 3. GET /api/v1/documents/test/chunking

Test the text chunking functionality.

**Response:**
```json
{
  "success": true,
  "original_length": 1500,
  "chunk_count": 2,
  "chunk_size": 1000,
  "chunk_overlap": 200,
  "chunks": [
    {
      "index": 0,
      "length": 987,
      "preview": "Artificial Intelligence (AI) is transforming..."
    },
    {
      "index": 1,
      "length": 713,
      "preview": "Deep learning, using neural networks..."
    }
  ]
}
```

## Features Implemented

### ✅ File Upload & Validation

- File type validation (`.txt`, `.pdf`)
- File size validation (default: 10MB max)
- File hash generation for deduplication
- Safe filename generation
- Async file operations

### ✅ Text File Parsing

- UTF-8 encoding with error handling
- Metadata extraction (word count, line count, etc.)
- Efficient async file reading
- Error handling and logging

### ✅ PDF Parsing with OCR

- Text extraction using PyPDF2
- OCR support for scanned PDFs using Tesseract
- Automatic fallback to OCR when text extraction fails
- Page count and metadata extraction
- PDF info extraction (title, author, subject)

### ✅ Intelligent Chunking

- Paragraph-aware chunking
- Sentence boundary detection
- Configurable chunk size and overlap
- Metadata attachment to chunks
- Preservation of document structure

### ✅ Error Handling

- Comprehensive error handling for all operations
- Detailed error messages
- HTTP status codes following REST conventions
- Logging for debugging

### ✅ Testing

- 5 comprehensive tests
- Text parser testing
- Chunking testing
- Upload validation
- File size validation

## Configuration Options

All configuration is in `.env`:

```bash
# Upload Configuration
MAX_UPLOAD_SIZE=10485760          # 10MB in bytes
ALLOWED_EXTENSIONS=.txt,.pdf
UPLOAD_DIR=/app/uploads

# Chunking Configuration
CHUNK_SIZE=1000                   # Characters per chunk
CHUNK_OVERLAP=200                 # Overlapping characters
```

### Customizing Chunk Settings

**For shorter chunks (better for specific queries):**
```bash
CHUNK_SIZE=500
CHUNK_OVERLAP=100
```

**For longer chunks (better for context):**
```bash
CHUNK_SIZE=2000
CHUNK_OVERLAP=400
```

**General Guidelines:**
- Smaller chunks (500-800): Better for precise retrieval
- Medium chunks (1000-1500): Balanced approach
- Larger chunks (2000+): More context, may lose precision

**Overlap recommendations:**
- Use 15-20% of chunk size for overlap
- Higher overlap = more context but more storage

## How It Works

### Document Upload Flow

```
1. User uploads file
   ↓
2. Validate file type and size
   ↓
3. Save file to disk with unique hash
   ↓
4. Parse document based on type:
   - Text files: Direct text extraction
   - PDF files: Text extraction with OCR fallback
   ↓
5. Chunk the extracted text
   ↓
6. Generate metadata
   ↓
7. Return document ID and metadata
   (Phase 4 will store in database)
```

### Text Chunking Strategy

The chunker uses a smart strategy to preserve document structure:

1. **Paragraph-aware**: Tries to split at paragraph boundaries
2. **Sentence-aware**: Falls back to sentence boundaries
3. **Overlap**: Maintains context between chunks
4. **Metadata**: Tracks chunk position and relationships

Example:
```
Original text: 5000 characters
Chunk size: 1000 characters
Overlap: 200 characters

Chunk 1: chars 0-1000
Chunk 2: chars 800-1800 (200 char overlap)
Chunk 3: chars 1600-2600 (200 char overlap)
...
```

## Supported File Formats

### Text Files (.txt)
- ✅ Plain text
- ✅ UTF-8 encoding
- ✅ Any text-based content

### PDF Files (.pdf)
- ✅ Text-based PDFs
- ✅ Scanned PDFs (via OCR)
- ✅ Mixed text/image PDFs
- ✅ Multi-page documents

### OCR Support

OCR is powered by Tesseract and handles:
- Scanned documents
- Image-based PDFs
- Low-quality scans
- Multiple languages (default: English)

**Note:** OCR is slower than text extraction but provides fallback for scanned documents.

## Troubleshooting

### Issue: "File type not allowed"

**Solution:**
```bash
# Check allowed extensions in .env
ALLOWED_EXTENSIONS=.txt,.pdf

# Restart after changes
make restart
```

### Issue: "File too large"

**Solution:**
```bash
# Increase max file size in .env (in bytes)
MAX_UPLOAD_SIZE=52428800  # 50MB

# Restart
make restart
```

### Issue: "OCR not working"

**Solution:**
```bash
# Verify Tesseract is installed in container
make shell-api
tesseract --version

# If missing, rebuild container
make rebuild
```

### Issue: "Empty content from PDF"

**Possible causes:**
1. PDF is image-based (OCR should handle this)
2. PDF is encrypted
3. PDF is corrupted

**Solution:**
```bash
# Check logs for detailed error
make logs-api | grep -i pdf

# Try with a different PDF
```

### Issue: Import errors

**Solution:**
```bash
# Ensure all directories and __init__.py files exist
mkdir -p utils parsers
touch utils/__init__.py parsers/__init__.py

# Rebuild
make rebuild
```

## Development Tips

### Testing with Sample Files

Create test files easily:

```bash
# Create a test text file
echo "This is a test document with multiple paragraphs.

Second paragraph here.

Third paragraph with more content." > test.txt

# Upload it
curl -X POST http://localhost:8000/api/v1/documents/upload \
  -F "file=@test.txt"
```

### Monitoring Uploads

```bash
# Watch upload directory
watch -n 1 ls -lh uploads/

# View logs during upload
make logs-api -f
```

### Testing Different Chunk Sizes

Modify `test_documents.py` to experiment:

```python
from utils import TextChunker

# Test with different sizes
chunker_small = TextChunker(chunk_size=500, chunk_overlap=100)
chunker_large = TextChunker(chunk_size=2000, chunk_overlap=400)
```

## Performance Considerations

### Upload Performance

- **Text files**: Very fast (~100ms for typical documents)
- **PDF text extraction**: Fast (~500ms for 10-page PDF)
- **PDF with OCR**: Slower (~5-10s for 10-page PDF at 300 DPI)

### Optimization Tips

1. **OCR Performance**:
   - Lower DPI for faster processing (trade-off: accuracy)
   - Process large PDFs in background (Phase 4)

2. **Chunking Performance**:
   - Larger chunks = fewer chunks = faster processing
   - Balance with retrieval quality

3. **Storage**:
   - Files are stored with hash-based names
   - Automatic deduplication by hash

## What's Not Implemented (Yet)

These features will come in later phases:

- ⏳ Database storage for documents (Phase 4)
- ⏳ Embedding generation (Phase 5)
- ⏳ Document listing and management (Phase 4)
- ⏳ Document deletion (Phase 4)
- ⏳ Background processing (Phase 4)
- ⏳ Full RAG with retrieval (Phase 6)

## Next Steps

Phase 3 is complete! You now have:
- ✅ Document upload functionality
- ✅ Text and PDF parsing
- ✅ OCR support for scanned documents
- ✅ Intelligent chunking
- ✅ Comprehensive testing

**Ready for Phase 4?**

Phase 4 will add:
- PostgreSQL database integration
- Document and chunk storage
- Vector embeddings storage
- Background task processing
- Document management endpoints
- Database migrations

---

## Quick Reference

### Common Commands

```bash
# Start services
make up

# Run Phase 3 tests
make test-documents

# Run all tests
make test-all

# View logs
make logs-api

# Test upload
curl -X POST http://localhost:8000/api/v1/documents/upload \
  -F "file=@document.pdf"
```

### Important URLs

- API Docs: http://localhost:8000/docs
- Upload Endpoint: http://localhost:8000/api/v1/documents/upload
- Test Parser: http://localhost:8000/api/v1/documents/test/parse-text
- Test Chunking: http://localhost:8000/api/v1/documents/test/chunking

---

**Phase 3 Complete! 🎉**

Proceed to Phase 4 when ready.