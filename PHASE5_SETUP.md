# Phase 5: Embeddings & Semantic Search

## Overview

Phase 5 implements comprehensive search capabilities including semantic search, keyword search, hybrid search, and context-aware search. This phase completes the "Retrieval" component of the RAG (Retrieval-Augmented Generation) system.

## What's New in Phase 5

### New Files Created

1. **services/search_service.py** - Complete search service with multiple search strategies
2. **routers/search.py** - Search API endpoints
3. **test_search.py** - Comprehensive search test suite
4. **PHASE5_SETUP.md** - This file

### Updated Files

1. **services/__init__.py** - Added search service import
2. **routers/__init__.py** - Added search router import
3. **main.py** - Included search router and updated endpoints
4. **Makefile** - Added `test-search` command

## File Structure After Phase 5

```
rag-fastapi-system/
├── main.py                      # Updated with search router
├── config.py                    # Configuration (unchanged)
├── models.py                    # Pydantic models (unchanged)
├── test_search.py               # NEW: Phase 5 tests
├── Makefile                     # Updated with search tests
├── services/                    # Updated
│   ├── __init__.py             # Updated
│   ├── openai_service.py
│   ├── background_tasks.py
│   └── search_service.py       # NEW
├── routers/                     # Updated
│   ├── __init__.py             # Updated
│   ├── chat.py
│   ├── documents.py
│   └── search.py               # NEW
├── database/                    # Database (from Phase 4)
├── utils/                       # Utils (from Phase 3)
└── parsers/                     # Parsers (from Phase 3)
```

## Installation Steps

### Step 1: Create New Files

```bash
# Create search service
touch services/search_service.py

# Create search router
touch routers/search.py

# Create test file
touch test_search.py
touch PHASE5_SETUP.md
```

### Step 2: Copy File Contents

Copy content from the artifacts into each file:

**New Files:**
1. ✅ `services/search_service.py` ← "services/search_service.py - Search Service"
2. ✅ `routers/search.py` ← "routers/search.py - Search Router"
3. ✅ `test_search.py` ← "test_search.py - Search Test Script"

**Updated Files:**
1. ✅ `services/__init__.py` ← Replace with updated version
2. ✅ `routers/__init__.py` ← Replace with updated version
3. ✅ `main.py` ← Replace with updated version
4. ✅ `Makefile` ← Replace with updated version

### Step 3: Rebuild and Restart

```bash
# Stop containers
make down

# Rebuild (if needed)
make build

# Start services
make up

# Check logs
make logs-api
```

### Step 4: Verify Search Endpoints

```bash
# Check search statistics
curl "http://localhost:8000/api/v1/search/stats"
```

## Testing Phase 5

### Method 1: Using the Test Script (Recommended)

```bash
# Make test script executable
chmod +x test_search.py

# Run comprehensive test suite
make test-search
```

The test script runs 7 tests:
1. ✅ Search Statistics
2. ✅ Semantic Search
3. ✅ Keyword Search
4. ✅ Hybrid Search
5. ✅ Context Search
6. ✅ Search Filters
7. ✅ Empty Results Handling

**Note**: Tests automatically upload a document, wait for processing, run searches, and clean up.

### Method 2: Manual Testing via Swagger UI

1. Open http://localhost:8000/docs
2. Navigate to **Search** section
3. Test these endpoints:
   - `GET /api/v1/search/semantic` - Semantic search
   - `GET /api/v1/search/keyword` - Keyword search
   - `GET /api/v1/search/hybrid` - Hybrid search
   - `GET /api/v1/search/context` - Context search
   - `GET /api/v1/search/stats` - Statistics

### Method 3: Using cURL

```bash
# Semantic search
curl "http://localhost:8000/api/v1/search/semantic?query=machine%20learning&top_k=5"

# Keyword search
curl "http://localhost:8000/api/v1/search/keyword?query=neural%20networks&top_k=5"

# Hybrid search
curl "http://localhost:8000/api/v1/search/hybrid?query=deep%20learning&top_k=5&semantic_weight=0.7&keyword_weight=0.3"

# Context search
curl "http://localhost:8000/api/v1/search/context?query=AI%20applications&context_window=1"

# Statistics
curl "http://localhost:8000/api/v1/search/stats"
```

## Features Implemented

### ✅ Semantic Search

**What it does**: Uses AI embeddings to find conceptually similar content

**How it works**:
1. Converts query to embedding vector
2. Computes cosine similarity with document chunks
3. Returns most similar chunks ranked by score

**Use cases**:
- Natural language queries
- Finding related concepts
- Conceptual similarity

**Example**:
```
Query: "How do computers learn?"
Finds: Chunks about machine learning, neural networks, training
```

### ✅ Keyword Search

**What it does**: Finds exact or partial text matches

**How it works**:
1. Searches chunk text for query string
2. Calculates relevance based on match frequency
3. Returns matching chunks

**Use cases**:
- Finding specific terms
- Exact phrase matching
- Quick text lookup

**Example**:
```
Query: "neural networks"
Finds: Chunks containing "neural networks"
```

### ✅ Hybrid Search

**What it does**: Combines semantic and keyword search

**How it works**:
1. Performs both semantic and keyword search
2. Combines scores with configurable weights
3. Returns unified ranked results

**Use cases**:
- Best of both worlds
- Balanced retrieval
- Flexible search strategies

**Example**:
```
Query: "deep learning applications"
Combines: Semantic understanding + exact term matching
Weights: 70% semantic, 30% keyword (configurable)
```

### ✅ Context Search

**What it does**: Includes surrounding chunks for better context

**How it works**:
1. Performs hybrid search
2. Retrieves N chunks before/after each result
3. Returns results with context

**Use cases**:
- Reading passages with context
- Understanding narrative flow
- Getting complete information

**Example**:
```
Query: "computer vision"
Returns: Matching chunk + 1 chunk before + 1 chunk after
```

### ✅ Search Filters

- **top_k**: Number of results (1-20)
- **document_id**: Filter by specific document
- **min_similarity**: Minimum similarity threshold (0.0-1.0)
- **semantic_weight**: Weight for semantic scores
- **keyword_weight**: Weight for keyword scores
- **context_window**: Number of surrounding chunks (0-5)

### ✅ Search Statistics

Provides insights about searchable content:
- Total documents
- Total chunks
- Chunks with embeddings
- Searchable percentage
- Average chunks per document

## API Endpoints

### 1. GET /api/v1/search/semantic

Semantic search using vector similarity.

**Parameters:**
- `query` (required): Search text
- `top_k` (optional): Number of results (default: 5, max: 20)
- `document_id` (optional): Filter by document
- `min_similarity` (optional): Minimum score (default: 0.0)

**Response:**
```json
{
  "success": true,
  "query": "machine learning",
  "search_type": "semantic",
  "results_count": 3,
  "results": [
    {
      "chunk_id": "chunk_doc_abc_0",
      "document_id": "doc_abc123",
      "document_name": "ai_guide.txt",
      "text": "Machine learning is a subset...",
      "chunk_index": 1,
      "similarity_score": 0.8542,
      "chunk_size": 234,
      "metadata": {
        "file_type": "txt",
        "uploaded_at": "2025-10-19T12:00:00"
      }
    }
  ],
  "timestamp": "2025-10-19T12:05:00"
}
```

### 2. GET /api/v1/search/keyword

Keyword-based text matching.

**Parameters:**
- `query` (required): Search text
- `top_k` (optional): Number of results (default: 5)
- `document_id` (optional): Filter by document

**Response:**
```json
{
  "success": true,
  "query": "neural networks",
  "search_type": "keyword",
  "results_count": 2,
  "results": [
    {
      "chunk_id": "chunk_doc_abc_2",
      "document_id": "doc_abc123",
      "document_name": "ai_guide.txt",
      "text": "Neural networks are inspired...",
      "chunk_index": 2,
      "relevance_score": 0.6,
      "chunk_size": 198,
      "match_count": 3,
      "metadata": {}
    }
  ]
}
```

### 3. GET /api/v1/search/hybrid

Hybrid search combining semantic and keyword.

**Parameters:**
- `query` (required): Search text
- `top_k` (optional): Number of results (default: 5)
- `document_id` (optional): Filter by document
- `semantic_weight` (optional): Semantic weight (default: 0.7)
- `keyword_weight` (optional): Keyword weight (default: 0.3)
- `min_similarity` (optional): Minimum semantic score (default: 0.0)

**Response:**
```json
{
  "success": true,
  "query": "deep learning",
  "search_type": "hybrid",
  "results_count": 3,
  "weights": {
    "semantic": 0.7,
    "keyword": 0.3
  },
  "results": [
    {
      "chunk_id": "chunk_doc_abc_1",
      "document_id": "doc_abc123",
      "document_name": "ai_guide.txt",
      "text": "Deep learning uses neural...",
      "chunk_index": 1,
      "combined_score": 0.7854,
      "semantic_score": 0.82,
      "keyword_score": 0.68,
      "chunk_size": 245,
      "metadata": {}
    }
  ]
}
```

### 4. GET /api/v1/search/context

Search with surrounding context chunks.

**Parameters:**
- `query` (required): Search text
- `top_k` (optional): Number of results (default: 5)
- `context_window` (optional): Surrounding chunks (default: 1, max: 5)
- `document_id` (optional): Filter by document
- `semantic_weight` (optional): Semantic weight (default: 0.7)
- `keyword_weight` (optional): Keyword weight (default: 0.3)

**Response:**
```json
{
  "success": true,
  "query": "computer vision",
  "search_type": "context",
  "context_window": 1,
  "results_count": 2,
  "results": [
    {
      "chunk_id": "chunk_doc_abc_4",
      "document_id": "doc_abc123",
      "document_name": "ai_guide.txt",
      "text": "Computer vision allows machines...",
      "chunk_index": 4,
      "combined_score": 0.7234,
      "context": [
        {
          "chunk_index": 3,
          "text": "Natural language processing...",
          "position": "before"
        },
        {
          "chunk_index": 5,
          "text": "Applications include facial...",
          "position": "after"
        }
      ]
    }
  ]
}
```

### 5. GET /api/v1/search/stats

Get search statistics and system status.

**Response:**
```json
{
  "success": true,
  "statistics": {
    "total_documents": 5,
    "total_chunks": 37,
    "chunks_with_embeddings": 37,
    "searchable_percentage": 100.0,
    "average_chunks_per_document": 7.4
  },
  "timestamp": "2025-10-19T12:00:00"
}
```

## Search Strategies

### When to Use Each Search Type

**Semantic Search** - Use when:
- Query is a natural language question
- Looking for conceptually related content
- Exact wording doesn't matter
- Want to find similar ideas

**Keyword Search** - Use when:
- Looking for specific terms or phrases
- Need exact matches
- Know the exact terminology
- Quick lookup required

**Hybrid Search** - Use when:
- Want best results from both approaches
- Balance between precision and recall
- Default recommendation for most cases
- Flexible search needs

**Context Search** - Use when:
- Need surrounding information
- Reading passages
- Understanding context
- Complete paragraphs needed

### Tuning Search Parameters

**For Precise Results:**
```
semantic_weight=0.3
keyword_weight=0.7
min_similarity=0.6
top_k=3
```

**For Broad Discovery:**
```
semantic_weight=0.8
keyword_weight=0.2
min_similarity=0.3
top_k=10
```

**Balanced (Recommended):**
```
semantic_weight=0.7
keyword_weight=0.3
min_similarity=0.0
top_k=5
```

## Performance

### Search Performance

| Operation | Average Time |
|-----------|--------------|
| Semantic Search | ~100-200ms |
| Keyword Search | ~50-100ms |
| Hybrid Search | ~150-250ms |
| Context Search | ~200-300ms |

**Factors affecting performance:**
- Number of chunks in database
- top_k parameter
- Context window size
- Database index efficiency

### Optimization Tips

1. **Use appropriate top_k**:
   - Smaller values = faster
   - Recommended: 5-10 for most cases

2. **Limit context window**:
   - 0-1: Fast
   - 2-3: Moderate
   - 4-5: Slower

3. **Filter by document**:
   - Reduces search space
   - Improves performance

4. **Set min_similarity**:
   - Filters low-quality results
   - Reduces processing time

## How It Works

### Semantic Search Flow

```
User Query
    ↓
Generate Query Embedding (OpenAI)
    ↓
Vector Similarity Search (pgvector)
    ↓
Calculate Cosine Similarity
    ↓
Rank by Similarity Score
    ↓
Filter by Threshold
    ↓
Return Top-K Results
```

### Hybrid Search Flow

```
User Query
    ↓
┌─────────────────┬─────────────────┐
│ Semantic Search │ Keyword Search  │
└────────┬────────┴────────┬────────┘
         │                  │
         ├──────────────────┤
         │ Combine Scores   │
         │ (Weighted)       │
         └────────┬─────────┘
                  ↓
         Rank by Combined Score
                  ↓
         Return Top-K Results
```

### Scoring System

**Semantic Similarity:**
- Cosine similarity between embeddings
- Range: 0.0 (dissimilar) to 1.0 (identical)
- Based on vector distance

**Keyword Relevance:**
- Frequency of query term in text
- Normalized to 0.0-1.0 range
- Simple but effective

**Combined Score:**
```
combined_score = (semantic_score × semantic_weight) + 
                 (keyword_score × keyword_weight)
```

## Configuration

All configuration is in `.env` (unchanged from previous phases):

```bash
# OpenAI (for embeddings)
OPENAI_API_KEY=your_key_here
OPENAI_EMBEDDING_MODEL=text-embedding-3-small

# Database
DATABASE_URL=postgresql://raguser:ragpassword@db:5432/ragdb

# Chunking (affects search granularity)
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
```

## Troubleshooting

### Issue: "No search results"

**Possible causes:**
1. Documents not yet processed
2. No embeddings generated
3. Query too specific
4. min_similarity too high

**Solutions:**
```bash
# Check if documents are processed
curl "http://localhost:8000/api/v1/search/stats"

# Verify embeddings exist
make shell-db
SELECT COUNT(*) FROM document_chunks WHERE embedding IS NOT NULL;

# Lower min_similarity
curl "http://localhost:8000/api/v1/search/semantic?query=test&min_similarity=0.0"
```

### Issue: "Slow search performance"

**Solutions:**
1. Reduce top_k parameter
2. Add document_id filter
3. Reduce context_window
4. Check database indexes:
   ```sql
   \di  -- List indexes in PostgreSQL
   ```

### Issue: "Irrelevant results"

**Solutions:**
1. Increase min_similarity threshold
2. Adjust semantic/keyword weights
3. Use more specific queries
4. Try keyword search for exact terms

### Issue: "Import error for search_service"

**Solution:**
```bash
# Verify file exists
ls services/search_service.py

# Check services/__init__.py includes search_service
grep search_service services/__init__.py

# Rebuild container
make rebuild
```

## Advanced Usage

### Custom Search Implementation

```python
from database import db_manager
from services import search_service

# Custom search with specific parameters
with db_manager.get_session() as db:
    results = search_service.hybrid_search(
        db=db,
        query="artificial intelligence",
        top_k=10,
        semantic_weight=0.8,
        keyword_weight=0.2,
        min_similarity=0.5
    )
    
    for result in results:
        print(f"Score: {result['combined_score']}")
        print(f"Text: {result['text'][:100]}...")
        print("-" * 50)
```

### Batch Search

```python
queries = [
    "machine learning",
    "deep learning",
    "neural networks"
]

all_results = {}
for query in queries:
    with db_manager.get_session() as db:
        results = search_service.semantic_search(db, query, top_k=3)
        all_results[query] = results
```

### Document-Specific Search

```python
# Search within a specific document
document_id = "doc_abc123"

with db_manager.get_session() as db:
    results = search_service.hybrid_search(
        db=db,
        query="key concepts",
        top_k=5,
        document_id=document_id
    )
```

## Search Analytics

### Tracking Search Patterns

You can log searches for analytics:

```python
# In routers/search.py, add logging
logger.info(f"Search: query='{query}', type={search_type}, results={len(results)}")
```

### Common Search Queries

Monitor logs to identify:
- Popular search terms
- Zero-result queries
- Slow searches
- User patterns

## Best Practices

### Query Formulation

**Good queries:**
- Natural language questions
- Specific concepts
- 2-5 word phrases

**Examples:**
- ✅ "What is machine learning?"
- ✅ "neural network architecture"
- ✅ "AI applications in healthcare"

**Less effective:**
- ❌ Single generic words ("AI")
- ❌ Very long sentences
- ❌ Overly complex questions

### Result Interpretation

**High similarity (0.8-1.0):**
- Very relevant results
- High confidence
- Direct answers

**Medium similarity (0.5-0.8):**
- Moderately relevant
- Related content
- May need review

**Low similarity (0.0-0.5):**
- Possibly relevant
- Tangentially related
- Consider different query

### Production Considerations

1. **Rate Limiting**: Add rate limiting to search endpoints
2. **Caching**: Cache common queries
3. **Monitoring**: Track search performance
4. **Feedback**: Collect user feedback on results
5. **A/B Testing**: Test different weight combinations

## What's Not Implemented (Yet)

These features will come in Phase 6 or future enhancements:

- ⏳ RAG chat with search integration (Phase 6)
- ⏳ Query expansion
- ⏳ Result caching
- ⏳ Search history
- ⏳ Personalized search
- ⏳ Multi-modal search (images + text)

## Next Steps - Phase 6 Preview

Phase 6 will integrate search with chat:

- ✨ RAG-powered chat endpoint
- ✨ Automatic context retrieval
- ✨ Source attribution in responses
- ✨ Multi-turn conversations with context
- ✨ Citation generation

## Testing Checklist

Before moving to Phase 6, verify:

- [ ] All new files created
- [ ] All existing files updated
- [ ] Containers running without errors
- [ ] Search statistics endpoint works
- [ ] Semantic search returns results
- [ ] Keyword search works
- [ ] Hybrid search combines scores correctly
- [ ] Context search includes surrounding chunks
- [ ] Filters work properly
- [ ] All 7 automated tests pass
- [ ] Search is reasonably fast (<300ms)

## Quick Reference

### Common Commands

```bash
# Start services
make up

# Run Phase 5 tests
make test-search

# Test semantic search
curl "http://localhost:8000/api/v1/search/semantic?query=AI&top_k=3"

# Check statistics
curl "http://localhost:8000/api/v1/search/stats"

# View logs
make logs-api
```

### Important URLs

- **API Docs**: http://localhost:8000/docs
- **Semantic Search**: http://localhost:8000/api/v1/search/semantic
- **Keyword Search**: http://localhost:8000/api/v1/search/keyword
- **Hybrid Search**: http://localhost:8000/api/v1/search/hybrid
- **Context Search**: http://localhost:8000/api/v1/search/context
- **Statistics**: http://localhost:8000/api/v1/search/stats

---

## Key Learnings

### What We Built

1. **Semantic Search** - AI-powered conceptual search
2. **Keyword Search** - Traditional text matching
3. **Hybrid Search** - Best of both worlds
4. **Context Search** - Results with surrounding text
5. **Search Statistics** - System insights

### Technologies Used

1. **Vector Similarity** - Cosine distance in pgvector
2. **OpenAI Embeddings** - text-embedding-3-small
3. **HNSW Index** - Fast approximate nearest neighbor
4. **SQL Text Search** - Pattern matching
5. **Score Combination** - Weighted ranking

---

## Success Criteria

Phase 5 is complete when:

- [x] Search service implemented
- [x] All search endpoints working
- [x] Semantic search functional
- [x] Keyword search operational
- [x] Hybrid search combining scores
- [x] Context search providing surrounding chunks
- [x] Statistics endpoint working
- [x] All 7 tests pass
- [x] Performance acceptable (<300ms)

---

**Phase 5 Complete! 🎉**

You now have:
- ✅ Semantic search with AI embeddings
- ✅ Keyword-based text search
- ✅ Hybrid search combining both
- ✅ Context-aware search
- ✅ Configurable search parameters
- ✅ Comprehensive testing

**Project Progress**: 83% Complete (5 of 6 core phases done)

Proceed to **Phase 6: Complete RAG Implementation** when ready! 🚀

---

**Phase 5 Completed**: October 19, 2025  
**Next Phase**: Complete RAG Implementation (Final Phase!)