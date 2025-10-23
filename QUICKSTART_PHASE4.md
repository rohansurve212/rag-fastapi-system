# Phase 4 - Quick Start Guide

## 🚀 5-Minute Setup

### Step 1: Create New Directory and Files

```bash
# Create database directory
mkdir -p database

# Create __init__.py
touch database/__init__.py

# Create all database files
touch database/models.py
touch database/connection.py
touch database/crud.py
touch database/schema.sql

# Create background tasks file
touch services/background_tasks.py

# Create test file
touch test_database.py
```

### Step 2: Copy File Contents

Copy content from the artifacts into each file:

**New Files (7 files):**
1. ✅ `database/__init__.py` ← "database/__init__.py - Database Package"
2. ✅ `database/models.py` ← "database/models.py - SQLAlchemy Models"
3. ✅ `database/connection.py` ← "database/connection.py - Database Connection"
4. ✅ `database/crud.py` ← "database/crud.py - CRUD Operations"
5. ✅ `database/schema.sql` ← "database/schema.sql - Database Schema"
6. ✅ `services/background_tasks.py` ← "services/background_tasks.py"
7. ✅ `test_database.py` ← "test_database.py - Database Test Script"

**Updated Files (5 files):**
1. ✅ `routers/documents.py` ← Replace with updated version
2. ✅ `services/__init__.py` ← Replace with updated version
3. ✅ `main.py` ← Replace with updated version
4. ✅ `init.sql` ← Replace with updated version
5. ✅ `Makefile` ← Replace with updated version

### Step 3: Rebuild and Start

```bash
# Stop containers
make down

# Rebuild
make build

# Start services
make up

# Watch logs (wait for "Database tables verified/created")
make logs-api
```

### Step 4: Verify Database

```bash
# Check database status
make db-status

# Should show:
# Documents: 0 (or more)
# Chunks: 0 (or more)
```

### Step 5: Test Everything

```bash
# Make test script executable
chmod +x test_database.py

# Run tests (takes ~10-15 seconds due to background processing)
make test-database
```

## ✅ Verification Checklist

- [ ] All new directories created (`database/`)
- [ ] All `__init__.py` files exist
- [ ] All 7 new files created and populated
- [ ] All 5 files updated
- [ ] Containers rebuilt and running
- [ ] Database connection successful
- [ ] Tables created (documents, document_chunks)
- [ ] All 7 tests pass

## 🧪 Quick Tests

```bash
# Test 1: Check health (should show database connected)
curl http://localhost:8000/health

# Test 2: Upload a document
echo "Test document content" > test.txt
curl -X POST http://localhost:8000/api/v1/documents/upload \
  -F "file=@test.txt"

# Test 3: List documents
curl http://localhost:8000/api/v1/documents/

# Test 4: Check database directly
make shell-db
SELECT * FROM documents;
\q
```

## 📊 Expected Test Results

```
============================================================
  Test 1: Database Connection
============================================================

✓ Health check successful
  Status: healthy
  Service: RAG System API
  OpenAI Configured: True

============================================================
  Test 2: Document Upload with Database
============================================================

✓ Document upload successful

  Document ID: doc_abc123def456
  Filename: test.txt
  File Size: 345 bytes
  File Hash: a1b2c3d4e5f6
  Message: Document uploaded successfully. Processing in background...

============================================================
  Test 3: Document Retrieval
============================================================

ℹ Waiting 3 seconds for background processing...
✓ Document retrieval successful

  Document ID: doc_abc123def456
  Filename: test.txt
  Chunks Created: 3

============================================================
  Test 4: Document Chunks Retrieval
============================================================

ℹ Waiting 5 seconds for chunk processing...
✓ Chunks retrieval successful

  Document ID: doc_abc123def456
  Chunk Count: 3

  First Chunk:
    Chunk ID: chunk_doc_abc123def456_0
    Index: 0
    Text Preview: Test document content...
    Has Embedding: True

============================================================
  Test 5: List Documents
============================================================

✓ Document list retrieval successful

  Total Documents: 1
  Documents Retrieved: 1

============================================================
  Test 6: Document Deletion
============================================================

✓ Document deletion successful
✓ Deletion verified (document not found)

============================================================
  Test 7: Duplicate Detection
============================================================

✓ Duplicate detected correctly
  Message: Document already exists (duplicate detected)
  Same Document ID: doc_abc123def456

============================================================
  Test Summary
============================================================

Database Connection: PASSED
Document Upload: PASSED
Document Retrieval: PASSED
Document Chunks: PASSED
List Documents: PASSED
Document Deletion: PASSED
Duplicate Detection: PASSED

Total: 7 | Passed: 7 | Failed: 0

🎉 All tests passed!
Phase 4 is complete and working correctly!
```

## 📋 New Features Summary

| Feature | Description |
|---------|-------------|
| **Database Integration** | PostgreSQL with pgvector |
| **Document Storage** | Persistent document metadata |
| **Chunk Storage** | Text chunks with embeddings |
| **Vector Search** | Similarity search capability |
| **Background Processing** | Async document processing |
| **CRUD Operations** | Full create/read/update/delete |
| **Duplicate Detection** | Hash-based deduplication |

## 🎯 What Works Now

✅ Upload documents → Stored in database  
✅ Background processing → Chunks + embeddings created  
✅ List documents → Pagination supported  
✅ Get document details → With processing status  
✅ Get chunks → With embedding info  
✅ Delete documents → Cascades to chunks  
✅ Duplicate detection → Reuses existing docs  

## 🔗 Important URLs

- **API Docs**: http://localhost:8000/docs
- **Health**: http://localhost:8000/health
- **Upload**: http://localhost:8000/api/v1/documents/upload
- **List**: http://localhost:8000/api/v1/documents/

## ⚠️ Common Issues

**"Database connection failed"**
→ Check if PostgreSQL container is running: `docker-compose ps`

**"Tables not created"**
→ Run: `make migrate`

**"Import error for database"**
→ Ensure `database/__init__.py` exists

**"Background processing not working"**
→ Check OpenAI API key in `.env`

**"Tests take too long"**
→ Normal! Background processing needs 10-15 seconds

## 🎉 Success!

If all tests pass:
- ✅ Database fully integrated
- ✅ Documents persist across restarts
- ✅ Embeddings stored in vectors
- ✅ Background processing works
- ✅ CRUD operations functional

**Ready for Phase 5: Embeddings & Semantic Search!** 🚀

---

**Need help?** Check `PHASE4_SETUP.md` for detailed documentation.