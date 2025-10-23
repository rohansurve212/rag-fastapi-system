# Phase 2: OpenAI Integration & Basic Chat Endpoint

## Overview

Phase 2 adds OpenAI integration to the RAG System, enabling AI-powered chat functionality. This phase builds the foundation for the Retrieval-Augmented Generation system by implementing basic chat capabilities that will later be enhanced with document retrieval.

## What's New in Phase 2

### New Files Created

1. **models.py** - Pydantic models for request/response validation
2. **services/openai_service.py** - OpenAI API integration service
3. **services/__init__.py** - Services package initialization
4. **routers/chat.py** - Chat endpoint router
5. **routers/__init__.py** - Routers package initialization
6. **test_chat.py** - Comprehensive test script for chat functionality
7. **PHASE2_SETUP.md** - This file

### Updated Files

1. **main.py** - Added chat router and enhanced status endpoints
2. **Makefile** - Added `test-chat` command

## File Structure After Phase 2

```
rag-fastapi-system/
├── main.py                    # Updated with chat router
├── config.py                  # Configuration (from Phase 1)
├── models.py                  # NEW: Pydantic models
├── requirements.txt           # Dependencies (from Phase 1)
├── Dockerfile                 # Container config (from Phase 1)
├── docker-compose.yml         # Docker Compose (from Phase 1)
├── init.sql                   # Database init (from Phase 1)
├── .env                       # Environment variables
├── .env.example               # Env template (from Phase 1)
├── .gitignore                 # Git ignore (from Phase 1)
├── README.md                  # Main documentation (from Phase 1)
├── PHASE2_SETUP.md            # NEW: This file
├── test_api.sh                # Phase 1 tests
├── test_chat.py               # NEW: Phase 2 tests
├── Makefile                   # Updated with new commands
├── services/                  # NEW: Services directory
│   ├── __init__.py           # Package initialization
│   └── openai_service.py     # OpenAI integration
├── routers/                   # NEW: Routers directory
│   ├── __init__.py           # Package initialization
│   └── chat.py               # Chat endpoints
└── uploads/                   # Upload directory
```

## Installation Steps

### Step 1: Create New Files

Create the following directory structure and files:

```bash
# Create directories
mkdir -p services
mkdir -p routers

# Create __init__.py files
touch services/__init__.py
touch routers/__init__.py
```

Then copy the content from the artifacts into these files:

1. `models.py` - Copy from "models.py - Pydantic Models" artifact
2. `services/__init__.py` - Copy from "services/__init__.py - Services Package" artifact
3. `services/openai_service.py` - Copy from "services/openai_service.py - OpenAI Integration" artifact
4. `routers/__init__.py` - Copy from "routers/__init__.py - Routers Package" artifact
5. `routers/chat.py` - Copy from "routers/chat.py - Chat Router" artifact
6. `test_chat.py` - Copy from "test_chat.py - Chat Endpoint Test Script" artifact
7. `PHASE2_SETUP.md` - Copy from this artifact

### Step 2: Update Existing Files

Replace the content of these files with the updated versions:

1. `main.py` - Replace with updated "main.py - FastAPI Application" artifact
2. `Makefile` - Replace with updated "Makefile - Development Commands" artifact

### Step 3: Configure Environment Variables

Make sure your `.env` file has a valid OpenAI API key:

```bash
# Edit .env file
nano .env

# Add or update:
OPENAI_API_KEY=sk-your-actual-openai-api-key-here
OPENAI_MODEL=gpt-4
OPENAI_EMBEDDING_MODEL=text-embedding-3-small
```

**Important:** You MUST have a valid OpenAI API key for Phase 2 to work!

### Step 4: Rebuild and Restart Containers

```bash
# Stop current containers
make down

# Rebuild with new code
make build

# Start services
make up

# Check logs to ensure no errors
make logs-api
```

## Testing Phase 2

### Method 1: Using the Test Script (Recommended)

```bash
# Make sure the test script is executable
chmod +x test_chat.py

# Run the comprehensive test suite
make test-chat
```

The test script will run 5 tests:
1. ✅ OpenAI Connection Test
2. ✅ Simple Chat Request
3. ✅ Chat with Conversation History
4. ✅ Temperature Variation
5. ✅ Error Handling

### Method 2: Using cURL

```bash
# Test OpenAI connection
curl http://localhost:8000/api/v1/chat/test

# Simple chat request
curl -X POST http://localhost:8000/api/v1/chat/ \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What is FastAPI?",
    "temperature": 0.7,
    "max_tokens": 500
  }'

# Chat with conversation history
curl -X POST http://localhost:8000/api/v1/chat/ \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What did I just ask about?",
    "conversation_history": [
      {"role": "user", "content": "Tell me about Python"},
      {"role": "assistant", "content": "Python is a programming language."}
    ],
    "temperature": 0.7,
    "max_tokens": 500
  }'
```

### Method 3: Using Swagger UI

1. Open your browser and go to: http://localhost:8000/docs
2. Navigate to the **Chat** section
3. Click on `POST /api/v1/chat/`
4. Click "Try it out"
5. Enter your request in the request body
6. Click "Execute"

Example request body:
```json
{
  "message": "Explain what a REST API is",
  "temperature": 0.7,
  "max_tokens": 500
}
```

## New API Endpoints

### 1. POST /api/v1/chat/

Send a message to the AI assistant.

**Request Body:**
```json
{
  "message": "Your question here",
  "conversation_history": [  // Optional
    {
      "role": "user",
      "content": "Previous message"
    },
    {
      "role": "assistant",
      "content": "Previous response"
    }
  ],
  "temperature": 0.7,  // Optional: 0.0 to 2.0
  "max_tokens": 500    // Optional: 1 to 4000
}
```

**Response:**
```json
{
  "response": "AI assistant's response",
  "message_count": 3,
  "tokens_used": 150,
  "model": "gpt-4",
  "timestamp": "2025-10-18T12:00:00"
}
```

### 2. GET /api/v1/chat/test

Test OpenAI API connection and configuration.

**Response:**
```json
{
  "status": "success",
  "message": "OpenAI API is properly configured and accessible",
  "model": "gpt-4",
  "embedding_model": "text-embedding-3-small"
}
```

## Updated Endpoints

### GET /health

Now includes OpenAI configuration status:

```json
{
  "status": "healthy",
  "timestamp": "2025-10-18T12:00:00",
  "service": "RAG System API",
  "openai_configured": true
}
```

### GET /api/v1/status

Enhanced with OpenAI status information:

```json
{
  "api_version": "1.0.0",
  "status": "operational",
  "timestamp": "2025-10-18T12:00:00",
  "endpoints": {
    "root": "/",
    "health": "/health",
    "chat": "/api/v1/chat",
    "test_openai": "/api/v1/chat/test",
    "docs": "/docs",
    "openapi": "/openapi.json"
  },
  "openai_status": {
    "configured": true,
    "model": "gpt-4",
    "embedding_model": "text-embedding-3-small"
  }
}
```

## Features Implemented

### ✅ OpenAI Service Layer

- Singleton service instance for efficient API usage
- Chat completion with customizable parameters
- Embedding generation (single and batch)
- Connection testing
- Comprehensive error handling
- Detailed logging

### ✅ Request/Response Models

- Type-safe Pydantic models
- Automatic validation
- Clear documentation in API docs
- Example schemas for easy testing

### ✅ Chat Router

- RESTful endpoint design
- Conversation history support
- Configurable temperature and max_tokens
- Proper error handling and status codes
- Detailed endpoint documentation

### ✅ Error Handling

- Graceful handling of OpenAI API errors
- Validation errors with clear messages
- HTTP status codes following REST conventions
- Structured error responses

### ✅ Testing

- Comprehensive test script
- Multiple test scenarios
- Clear pass/fail indicators
- Integration testing

## Configuration Options

All configuration is in `.env`:

```bash
# OpenAI Settings
OPENAI_API_KEY=your_key_here
OPENAI_MODEL=gpt-4                    # or gpt-3.5-turbo for lower cost
OPENAI_EMBEDDING_MODEL=text-embedding-3-small
```

### Model Options

**Chat Models:**
- `gpt-4` - Most capable, higher cost
- `gpt-4-turbo` - Faster, lower cost than GPT-4
- `gpt-3.5-turbo` - Fast, cost-effective

**Embedding Models:**
- `text-embedding-3-small` - Recommended, cost-effective
- `text-embedding-3-large` - Higher quality, higher cost

## Troubleshooting

### Issue: "OpenAI API key is not configured"

**Solution:**
```bash
# Check your .env file
cat .env | grep OPENAI_API_KEY

# Make sure it's set correctly
OPENAI_API_KEY=sk-your-actual-key-here

# Restart containers
make restart
```

### Issue: "Failed to connect to OpenAI API"

**Solutions:**
1. Verify your API key is valid at https://platform.openai.com/api-keys
2. Check if you have API credits/billing set up
3. Verify network connectivity from container:
   ```bash
   make shell-api
   curl https://api.openai.com/v1/models -H "Authorization: Bearer $OPENAI_API_KEY"
   ```

### Issue: "Rate limit exceeded"

**Solution:**
- You've hit OpenAI's rate limits
- Wait a few seconds and try again
- Consider upgrading your OpenAI plan
- Use gpt-3.5-turbo for higher rate limits

### Issue: Import errors when starting

**Solution:**
```bash
# Make sure all directories exist
mkdir -p services routers

# Make sure __init__.py files exist
touch services/__init__.py
touch routers/__init__.py

# Rebuild container
make rebuild
```

### Issue: Test script not running

**Solution:**
```bash
# Make it executable
chmod +x test_chat.py

# Run directly in container
docker-compose exec api python test_chat.py
```

## Development Tips

### Testing Chat Locally

Create a simple Python script to test the chat endpoint:

```python
import requests

response = requests.post(
    "http://localhost:8000/api/v1/chat/",
    json={
        "message": "Hello, how are you?",
        "temperature": 0.7,
        "max_tokens": 100
    }
)

print(response.json())
```

### Monitoring Token Usage

Check logs to see token consumption:
```bash
make logs-api | grep "tokens"
```

### Adjusting Response Length

Control response length with `max_tokens`:
- Short answers: 50-100 tokens
- Medium answers: 200-500 tokens
- Long answers: 500-2000 tokens

## Cost Considerations

OpenAI API pricing (approximate):

**GPT-4:**
- Input: $0.03 / 1K tokens
- Output: $0.06 / 1K tokens

**GPT-3.5-turbo:**
- Input: $0.0005 / 1K tokens
- Output: $0.0015 / 1K tokens

**Embeddings (text-embedding-3-small):**
- $0.00002 / 1K tokens

### Cost Saving Tips

1. Use `gpt-3.5-turbo` for testing and development
2. Set reasonable `max_tokens` limits
3. Cache responses when possible (future phase)
4. Use temperature=0 for deterministic responses (lower cost)

## Next Steps

Phase 2 is complete! You now have:
- ✅ Working OpenAI integration
- ✅ Functional chat endpoint
- ✅ Conversation history support
- ✅ Comprehensive testing

**Ready for Phase 3?**

Phase 3 will add:
- Document upload functionality
- Text and PDF parsing
- OCR for scanned PDFs
- Document chunking strategies
- File validation and storage

---

## Quick Reference

### Common Commands

```bash
# Start services
make up

# View logs
make logs-api

# Run tests
make test-chat

# Test OpenAI connection
curl http://localhost:8000/api/v1/chat/test

# Stop services
make down
```

### Important URLs

- API Docs: http://localhost:8000/docs
- Health Check: http://localhost:8000/health
- API Status: http://localhost:8000/api/v1/status
- Chat Endpoint: http://localhost:8000/api/v1/chat/

---

**Phase 2 Complete! 🎉**

Proceed to Phase 3 when ready.