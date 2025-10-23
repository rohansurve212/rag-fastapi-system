# Phase 3 - Quick Start Guide

## 🚀 5-Minute Setup

### Step 1: Create New Directories and Files

```bash
# Create directories
mkdir -p utils parsers

# Create package initialization files
touch utils/__init__.py
touch parsers/__init__.py

# Create new files
touch utils/file_handler.py
touch utils/text_chunker.py
touch parsers/text_parser.py
touch parsers/pdf_parser.py
touch routers/documents.py
touch test_documents.py
touch PHASE3_SETUP.md
```

### Step 2: Copy File Contents

Copy content from the artifacts into each file:

**New Files:**
1. ✅ `utils/__init__.py` ← "utils/__init__.py - Utils Package"
2. ✅ `utils/file_handler.py` ← "utils/file_handler.py - File Handling Utilities"
3. ✅ `utils/text_chunker.py` ← "utils/text_chunker.py - Document Chunking"
4. ✅ `parsers/__init__.py` ← "parsers/__init__.py - Parsers Package"
5. ✅ `parsers/text_parser.py` ← "parsers/text_parser.py - Text File Parser"
6. ✅ `parsers/pdf_parser.py` ← "parsers/pdf_parser.py - PDF Parser with OCR"
7. ✅ `routers/documents.py` ← "routers/documents.py - Document Upload Router"
8. ✅ `test_documents.py` ← "test_documents.py - Document Upload Test Script"

**Updated Files:**
1. ✅ `models.py` ← Replace with updated version
2. ✅ `routers/__init__.py` ← Replace with updated version
3. ✅ `main.py` ← Replace with updated version
4. ✅ `Makefile` ← Replace with updated version

### Step 3: Rebuild and Start

```bash
# Stop current containers
make down

# Rebuild
make build

# Start services
make up

# Check logs
make logs-api
```

### Step 4: Test Everything

```bash
# Run comprehensive tests
chmod +x test_documents.py
make test-documents
```

## ✅ Verification Checklist

- [ ] All new directories created (`utils/`, `parsers/`)
- [ ] All `__init__.py` files created
- [ ] All new files created and populated
- [ ] Updated files replaced
- [ ] Containers rebuilt and running
- [ ] No errors in logs
- [ ] Test script passes all 5 tests

## 🧪 Quick Tests

```bash
# Test text parser
curl http://localhost:8000/api/v1/documents/test/parse-text

# Test chunking
curl http://localhost:8000/api/v1/documents/test/chunking

# Create and upload a test file
echo "This is a test document" > test.txt
curl -X POST http://localhost:8000/api/v1/documents/upload \
  -F "file=@test.txt"
```

## 📋 New Files Summary

| File | Purpose |
|------|---------|
| `utils/file_handler.py` | File upload, validation, storage |
| `utils/text_chunker.py` | Document chunking strategy |
| `parsers/text_parser.py` | Text file parsing |
| `parsers/pdf_parser.py` | PDF parsing with OCR |
| `routers/documents.py` | Document upload endpoints |
| `test_documents.py` | Comprehensive test suite |

## 🎯 What Works Now

✅ Upload text files (.txt)  
✅ Upload PDF files (.pdf)  
✅ OCR for scanned PDFs  
✅ Intelligent text chunking  
✅ File validation (type & size)  
✅ Metadata extraction  
✅ Test endpoints  

## 🔗 Important URLs

- **API Docs**: http://localhost:8000/docs
- **Upload**: http://localhost:8000/api/v1/documents/upload
- **Test Parser**: http://localhost:8000/api/v1/documents/test/parse-text
- **Test Chunking**: http://localhost:8000/api/v1/documents/test/chunking

## ⚠️ Common Issues

**"Import Error" for utils or parsers**
→ Make sure `__init__.py` files exist in both directories

**"Tesseract not found"**
→ OCR requires Tesseract (already in Docker image)

**"File too large"**
→ Default limit is 10MB, adjust `MAX_UPLOAD_SIZE` in `.env`

**"File type not allowed"**
→ Only `.txt` and `.pdf` are supported

## 📊 Test Output

When successful, you should see:

```
✓ Text Parser test successful
✓ Chunking test successful  
✓ Text file upload successful
✓ Validation correctly rejected invalid file type
✓ Validation correctly rejected file exceeding size limit

🎉 All tests passed!
Phase 3 is complete and working correctly!
```

## 🎉 Success!

If all tests pass, you're ready for **Phase 4: Database Integration**!

---

**Need help?** Check `PHASE3_SETUP.md` for detailed documentation.