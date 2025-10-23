# RAG System with FastAPI

A complete Retrieval-Augmented Generation (RAG) system built with FastAPI and OpenAI's API that allows users to upload documents and have natural conversations about their content using semantic search and AI-powered responses.

## 🚀 Features

- **Document Upload & Processing**: Upload text and PDF documents with OCR support
- **Semantic Search**: Find relevant information using vector embeddings
- **RAG-Powered Chat**: Chat with your documents using AI
- **Source Attribution**: Know where information comes from
- **Multi-turn Conversations**: Maintain context across conversation
- **RESTful API**: Well-structured FastAPI application
- **Database Integration**: PostgreSQL with pgvector for efficient vector storage
- **Containerized**: Fully containerized with Docker and Docker Compose

## 📋 Prerequisites

- Docker and Docker Compose installed
- OpenAI API key
- At least 4GB of free disk space

## 🛠️ Installation & Setup

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd rag-fastapi-system
```

### 2. Create Environment File

Copy the example environment file and update it with your settings:

```bash
cp .env.example .env
```

Edit `.env` and add your OpenAI API key:

```
OPENAI_API_KEY=your_openai_api_key_here
```

### 3. Build and Start the Application

```bash
docker-compose up --build
```

This will:
- Build the FastAPI application container
- Start PostgreSQL with pgvector extension
- Set up the network and volumes
- Initialize the database

### 4. Verify Installation

Once the containers are running, you can access:

- **API Documentation**: http://localhost:8000/docs
- **Alternative API Docs**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health
- **RAG Health**: http://localhost:8000/api/v1/rag/health

## 📁 Project Structure

```
rag-fastapi-system/
├── main.py                      # FastAPI application entry point
├── config.py                    # Configuration management
├── models.py                    # Pydantic models
├── requirements.txt             # Python dependencies
├── Dockerfile                   # Docker configuration
├── docker-compose.yml           # Docker Compose configuration
├── services/                    # Business logic services
│   ├── openai_service.py       # OpenAI integration
│   ├── search_service.py       # Search functionality
│   ├── rag_service.py          # RAG implementation
│   └── background_tasks.py     # Async processing
├── routers/                     # API endpoints
│   ├── chat.py                 # Simple chat
│   ├── documents.py            # Document management
│   ├── search.py               # Search endpoints
│   └── rag.py                  # RAG chat
├── database/                    # Database layer
│   ├── models.py               # SQLAlchemy models
│   ├── connection.py           # Connection management
│   └── crud.py                 # CRUD operations
├── utils/                       # Utility functions
│   ├── file_handler.py         # File operations
│   └── text_chunker.py         # Text chunking
└── parsers/                     # Document parsers
    ├── text_parser.py          # Text file parser
    └── pdf_parser.py           # PDF parser with OCR
```

## 🔌 API Endpoints

### Document Management
- `POST /api/v1/documents/upload` - Upload documents
- `GET /api/v1/documents/` - List documents
- `GET /api/v1/documents/{id}` - Get document details
- `DELETE /api/v1/documents/{id}` - Delete document

### Search
- `GET /api/v1/search/semantic` - Semantic search
- `GET /api/v1/search/keyword` - Keyword search
- `GET /api/v1/search/hybrid` - Hybrid search
- `GET /api/v1/search/context` - Context search
- `GET /api/v1/search/stats` - Search statistics

### RAG Chat
- `POST /api/v1/rag/chat` - RAG-powered chat
- `GET /api/v1/rag/health` - RAG system health

### Simple Chat
- `POST /api/v1/chat` - Simple chat (no RAG)
- `GET /api/v1/chat/test` - Test OpenAI connection

## 🧪 Testing

### Run All Tests
```bash
make test-all
```

### Run Individual Phase Tests
```bash
make test          # Phase 1: Basic API
make test-chat     # Phase 2: OpenAI integration
make test-documents # Phase 3: Document upload
make test-database # Phase 4: Database
make test-search   # Phase 5: Search
make test-rag      # Phase 6: RAG (Final)
```

## 💡 Usage Examples

### 1. Upload a Document

```bash
curl -X POST http://localhost:8000/api/v1/documents/upload \
  -F "file=@your_document.pdf"
```

### 2. Search Documents

```bash
curl "http://localhost:8000/api/v1/search/hybrid?query=machine%20learning&top_k=5"
```

### 3. RAG Chat

```bash
curl -X POST http://localhost:8000/api/v1/rag/chat \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is machine learning?",
    "top_k": 5,
    "temperature": 0.7
  }'
```

### 4. Multi-turn Conversation

```bash
curl -X POST http://localhost:8000/api/v1/rag/chat \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What are its applications?",
    "conversation_history": [
      {"role": "user", "content": "What is deep learning?"},
      {"role": "assistant", "content": "Deep learning is..."}
    ],
    "top_k": 5
  }'
```

## 🔧 Configuration

All configuration is managed through environment variables in the `.env` file:

### Key Variables

```bash
# OpenAI
OPENAI_API_KEY=your_key_here
OPENAI_MODEL=gpt-4
OPENAI_EMBEDDING_MODEL=text-embedding-3-small

# Database
DATABASE_URL=postgresql://raguser:ragpassword@db:5432/ragdb

# Upload Settings
MAX_UPLOAD_SIZE=10485760  # 10MB
ALLOWED_EXTENSIONS=.txt,.pdf

# Chunking
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
```

## 🐳 Docker Commands

```bash
# Start services
make up

# Stop services
make down

# Restart services
make restart

# View logs
make logs-api
make logs-db

# Rebuild containers
make rebuild

# Open API container shell
make shell-api

# Open database shell
make shell-db

# Check database status
make db-status
```

## 🚧 Development Phases

This project was built in 6 phases:

- ✅ **Phase 1**: Project Setup & Basic FastAPI Application
- ✅ **Phase 2**: OpenAI Integration & Basic Chat Endpoint
- ✅ **Phase 3**: Document Upload & Storage
- ✅ **Phase 4**: Database Integration & Management
- ✅ **Phase 5**: Embeddings & Semantic Search
- ✅ **Phase 6**: Complete RAG Implementation (**FINAL**)

## 🎓 How It Works

### RAG System Flow

```
1. User uploads documents
   ↓
2. Documents are parsed and chunked
   ↓
3. Chunks are embedded using OpenAI
   ↓
4. Embeddings stored in PostgreSQL with pgvector
   ↓
5. User asks a question
   ↓
6. Question is embedded
   ↓
7. Similar chunks retrieved via vector search
   ↓
8. Context assembled from relevant chunks
   ↓
9. AI generates answer using context
   ↓
10. Response with sources returned to user
```

### Key Technologies

- **FastAPI**: Modern Python web framework
- **PostgreSQL**: Relational database
- **pgvector**: Vector similarity search
- **OpenAI API**: Embeddings and chat completion
- **SQLAlchemy**: ORM for database
- **Docker**: Containerization

## 📊 Performance

- Document upload: <1 second
- Background processing: 5-15 seconds
- Semantic search: 100-200ms
- RAG response: 1-3 seconds

## 🔐 Security Notes

- Never commit your `.env` file to version control
- Keep your OpenAI API key secure
- In production, update CORS settings
- Use strong database passwords
- Implement rate limiting
- Add authentication (JWT/OAuth)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License.

## 🆘 Troubleshooting

### Common Issues

**Port Already in Use**
```bash
# Change ports in docker-compose.yml
ports:
  - "8001:8000"  # Use different port
```

**Database Connection Issues**
```bash
# Check database logs
make logs-db

# Restart database
docker-compose restart db
```

**OpenAI API Errors**
```bash
# Verify API key
grep OPENAI_API_KEY .env

# Test connection
curl http://localhost:8000/api/v1/chat/test
```

**No Search Results**
```bash
# Check embeddings
make shell-db
SELECT COUNT(*) FROM document_chunks WHERE embedding IS NOT NULL;
\q

# Upload documents and wait for processing
```

## 📚 Documentation

- Full API documentation: http://localhost:8000/docs
- Setup guides in phase-specific markdown files
- Inline code documentation

## 🎉 Success!

If you see this in your tests:
```
🎉 All tests passed!
🏆 CONGRATULATIONS! The complete RAG system is functional! 🏆
```

**You have a fully functional RAG system!** 🚀

## 📧 Support

For issues and questions, please open an issue on the GitHub repository.

---

Built with ❤️ using FastAPI, OpenAI, PostgreSQL, and pgvector

**Complete RAG System** - Upload documents, search semantically, chat naturally! 🤖✨
d AI-powered responses.

## 🚀 Features

- **Document Upload & Processing**: Upload text and PDF documents
- **Semantic Search**: Find relevant information using vector embeddings
- **AI-Powered Chat**: Chat with your documents using OpenAI's GPT models
- **RESTful API**: Well-structured FastAPI application
- **Database Integration**: PostgreSQL with pgvector for efficient vector storage
- **Containerized**: Fully containerized with Docker and Docker Compose

## 📋 Prerequisites

- Docker and Docker Compose installed
- OpenAI API key
- At least 2GB of free disk space

## 🛠️ Installation & Setup

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd rag-fastapi-system
```

### 2. Create Environment File

Copy the example environment file and update it with your settings:

```bash
cp .env.example .env
```

Edit `.env` and add your OpenAI API key:

```
OPENAI_API_KEY=your_openai_api_key_here
```

### 3. Build and Start the Application

```bash
docker-compose up --build
```

This will:
- Build the FastAPI application container
- Start PostgreSQL with pgvector extension
- Set up the network and volumes
- Initialize the database

### 4. Verify Installation

Once the containers are running, you can access:

- **API Documentation**: http://localhost:8000/docs
- **Alternative API Docs**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## 📁 Project Structure

```
rag-fastapi-system/
├── main.py                 # FastAPI application entry point
├── config.py              # Configuration management
├── requirements.txt       # Python dependencies
├── Dockerfile            # Docker configuration
├── docker-compose.yml    # Docker Compose configuration
├── init.sql              # Database initialization script
├── .env.example          # Environment variables template
├── .gitignore           # Git ignore file
├── README.md            # This file
└── uploads/             # Directory for uploaded files (created automatically)
```

## 🔌 API Endpoints

### Phase 1 Endpoints

- `GET /` - Welcome message
- `GET /health` - Health check endpoint
- `GET /api/v1/status` - Detailed API status

## 🐳 Docker Commands

### Start the application
```bash
docker-compose up
```

### Start in detached mode (background)
```bash
docker-compose up -d
```

### Stop the application
```bash
docker-compose down
```

### View logs
```bash
docker-compose logs -f
```

### View logs for specific service
```bash
docker-compose logs -f api
docker-compose logs -f db
```

### Rebuild containers
```bash
docker-compose up --build
```

### Remove all containers and volumes
```bash
docker-compose down -v
```

## 🧪 Testing

### Test Health Check
```bash
curl http://localhost:8000/health
```

### Test API Status
```bash
curl http://localhost:8000/api/v1/status
```

## 🔧 Configuration

All configuration is managed through environment variables in the `.env` file:

- **Application Settings**: App name, version, environment
- **OpenAI Settings**: API key, model selection
- **Database Settings**: Connection details
- **Upload Settings**: File size limits, allowed extensions
- **Vector Search Settings**: Embedding dimensions, top-K results
- **Chunking Settings**: Chunk size and overlap

## 📝 Environment Variables

Key environment variables (see `.env.example` for complete list):

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | Your OpenAI API key | Required |
| `OPENAI_MODEL` | GPT model to use | gpt-4 |
| `DATABASE_URL` | PostgreSQL connection string | Auto-configured |
| `MAX_UPLOAD_SIZE` | Max file upload size in bytes | 10485760 (10MB) |
| `CHUNK_SIZE` | Document chunk size | 1000 |

## 🔐 Security Notes

- Never commit your `.env` file to version control
- Keep your OpenAI API key secure
- In production, update CORS settings in `main.py`
- Use strong database passwords in production

## 🚧 Development Phases

This project is built in phases:

- ✅ **Phase 1**: Project Setup & Basic FastAPI Application (Current)
- ⏳ **Phase 2**: OpenAI Integration & Basic Chat Endpoint
- ⏳ **Phase 3**: Document Upload & Storage
- ⏳ **Phase 4**: Database Setup & Vector Storage
- ⏳ **Phase 5**: Embeddings & Semantic Search
- ⏳ **Phase 6**: Complete RAG Implementation
- ⏳ **Phase 7**: Testing, Optimization & Documentation

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License.

## 🆘 Troubleshooting

### Port Already in Use
If port 8000 or 5432 is already in use, update the ports in `docker-compose.yml`:

```yaml
ports:
  - "8001:8000"  # Change 8001 to any available port
```

### Database Connection Issues
Check database logs:
```bash
docker-compose logs db
```

Verify database is healthy:
```bash
docker-compose ps
```

### Container Build Failures
Clean rebuild:
```bash
docker-compose down -v
docker-compose build --no-cache
docker-compose up
```

## 📧 Support

For issues and questions, please open an issue on the GitHub repository.

---

Built with ❤️ using FastAPI, OpenAI, and PostgreSQL