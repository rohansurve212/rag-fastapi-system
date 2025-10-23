from fastapi import APIRouter, UploadFile, File, HTTPException, status, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List
from pathlib import Path
import uuid
from datetime import datetime

from models import (
    DocumentUploadResponse,
    DocumentMetadata,
    ErrorResponse,
    ChunkData,
    DocumentListResponse
)
from utils import file_handler, text_chunker
from parsers import text_parser, pdf_parser
from database import get_db
from database.crud import DocumentCRUD, ChunkCRUD
from services import background_task_service
import logging

logger = logging.getLogger(__name__)

# Create router
router = APIRouter(
    prefix="/api/v1/documents",
    tags=["Documents"],
    responses={
        500: {"model": ErrorResponse, "description": "Internal server error"},
        400: {"model": ErrorResponse, "description": "Bad request"}
    }
)


@router.post("/upload", response_model=DocumentUploadResponse, status_code=status.HTTP_201_CREATED)
async def upload_document(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(..., description="Document file to upload (PDF or TXT)"),
    db: Session = Depends(get_db)
):
    """
    Upload and process a document
    
    This endpoint accepts text and PDF files, saves them, and processes them
    in the background to extract content, create chunks, and generate embeddings.
    
    **Supported formats:**
    - Text files (.txt)
    - PDF files (.pdf) - with OCR support for scanned documents
    
    **Processing steps:**
    1. Validate file type and size
    2. Check for duplicate (by hash)
    3. Save file to disk
    4. Create database record
    5. Process in background:
       - Extract text content
       - Split into chunks
       - Generate embeddings
       - Store chunks in database
    
    **Returns:**
    - Document ID
    - File metadata
    - Processing status
    """
    try:
        logger.info(f"Received upload request for file: {file.filename}")
        
        # Step 1: Validate file
        is_valid, error_message = file_handler.validate_file(file)
        if not is_valid:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error_message
            )
        
        # Step 2: Save file to disk
        file_path, file_hash, file_size = await file_handler.save_file(file)
        
        # Step 3: Check for duplicate
        existing_doc = DocumentCRUD.get_document_by_hash(db, file_hash)
        if existing_doc:
            logger.info(f"Duplicate document found: {existing_doc.document_id}")
            return DocumentUploadResponse(
                success=True,
                message="Document already exists (duplicate detected)",
                document_id=existing_doc.document_id,
                filename=existing_doc.filename,
                file_size=existing_doc.file_size,
                file_hash=existing_doc.file_hash,
                chunks_created=existing_doc.chunk_count or 0,
                metadata=DocumentMetadata(
                    filename=existing_doc.filename,
                    file_type=existing_doc.file_type,
                    file_size=existing_doc.file_size,
                    file_hash=existing_doc.file_hash,
                    character_count=existing_doc.character_count,
                    word_count=existing_doc.word_count,
                    page_count=existing_doc.page_count,
                    chunk_count=existing_doc.chunk_count,
                    uploaded_at=existing_doc.uploaded_at
                )
            )
        
        # Step 4: Parse document to get metadata
        file_ext = Path(file.filename).suffix.lower()
        file_type = file_ext[1:]  # Remove the dot
        
        if file_ext == '.txt':
            parse_result = await text_parser.parse(file_path)
        elif file_ext == '.pdf':
            parse_result = await pdf_parser.parse(file_path, use_ocr=True)
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unsupported file type: {file_ext}"
            )
        
        if not parse_result["success"]:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to parse document: {parse_result['error']}"
            )
        
        # Generate document ID
        document_id = f"doc_{uuid.uuid4().hex[:12]}"
        
        # Step 5: Create database record
        document = DocumentCRUD.create_document(
            db=db,
            document_id=document_id,
            filename=file.filename,
            file_type=file_type,
            file_size=file_size,
            file_hash=file_hash,
            file_path=str(file_path),
            character_count=parse_result["metadata"].get("character_count", 0),
            word_count=parse_result["metadata"].get("word_count", 0),
            page_count=parse_result["metadata"].get("page_count"),
            processing_status='pending'
        )
        
        # Step 6: Add background task for processing
        background_tasks.add_task(
            background_task_service.process_document,
            document_id=document_id,
            file_path=file_path,
            filename=file.filename,
            file_type=file_type
        )
        
        # Step 7: Create metadata response
        doc_metadata = DocumentMetadata(
            filename=document.filename,
            file_type=document.file_type,
            file_size=document.file_size,
            file_hash=document.file_hash,
            character_count=document.character_count,
            word_count=document.word_count,
            page_count=document.page_count,
            chunk_count=0,  # Will be updated by background task
            uploaded_at=document.uploaded_at
        )
        
        # Step 8: Create response
        response = DocumentUploadResponse(
            success=True,
            message="Document uploaded successfully. Processing in background...",
            document_id=document_id,
            filename=file.filename,
            file_size=file_size,
            file_hash=file_hash,
            chunks_created=0,  # Will be updated by background task
            metadata=doc_metadata
        )
        
        logger.info(f"Upload completed successfully for document: {document_id}")
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in document upload: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        )


@router.get("/", response_model=DocumentListResponse)
async def list_documents(
    skip: int = 0,
    limit: int = 100,
    status: str = None,
    db: Session = Depends(get_db)
):
    """
    List all uploaded documents
    
    **Query Parameters:**
    - skip: Number of records to skip (pagination)
    - limit: Maximum records to return (max 100)
    - status: Filter by processing status (pending, processing, completed, failed)
    
    **Returns:**
    - List of documents with metadata
    - Total count
    """
    try:
        documents = DocumentCRUD.get_all_documents(db, skip=skip, limit=limit, status=status)
        total_count = DocumentCRUD.count_documents(db, status=status)
        
        doc_list = []
        for doc in documents:
            doc_list.append(DocumentMetadata(
                filename=doc.filename,
                file_type=doc.file_type,
                file_size=doc.file_size,
                file_hash=doc.file_hash,
                character_count=doc.character_count,
                word_count=doc.word_count,
                page_count=doc.page_count,
                chunk_count=doc.chunk_count,
                uploaded_at=doc.uploaded_at
            ))
        
        return DocumentListResponse(
            documents=doc_list,
            total_count=total_count
        )
        
    except Exception as e:
        logger.error(f"Error listing documents: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list documents: {str(e)}"
        )


@router.get("/{document_id}", response_model=DocumentUploadResponse)
async def get_document(
    document_id: str,
    db: Session = Depends(get_db)
):
    """
    Get details of a specific document
    
    **Path Parameters:**
    - document_id: Document identifier
    
    **Returns:**
    - Document metadata
    - Processing status
    - Chunk information
    """
    try:
        document = DocumentCRUD.get_document_by_id(db, document_id)
        
        if not document:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Document not found: {document_id}"
            )
        
        doc_metadata = DocumentMetadata(
            filename=document.filename,
            file_type=document.file_type,
            file_size=document.file_size,
            file_hash=document.file_hash,
            character_count=document.character_count,
            word_count=document.word_count,
            page_count=document.page_count,
            chunk_count=document.chunk_count,
            uploaded_at=document.uploaded_at
        )
        
        return DocumentUploadResponse(
            success=document.processing_status == 'completed',
            message=f"Document status: {document.processing_status}",
            document_id=document.document_id,
            filename=document.filename,
            file_size=document.file_size,
            file_hash=document.file_hash,
            chunks_created=document.chunk_count or 0,
            metadata=doc_metadata
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting document: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get document: {str(e)}"
        )


@router.delete("/{document_id}")
async def delete_document(
    document_id: str,
    db: Session = Depends(get_db)
):
    """
    Delete a document and all its chunks
    
    **Path Parameters:**
    - document_id: Document identifier
    
    **Returns:**
    - Success message
    """
    try:
        # Get document to get file path
        document = DocumentCRUD.get_document_by_id(db, document_id)
        
        if not document:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Document not found: {document_id}"
            )
        
        # Delete file from disk
        file_path = Path(document.file_path)
        if file_path.exists():
            await file_handler.delete_file(file_path)
        
        # Delete from database (cascades to chunks)
        DocumentCRUD.delete_document(db, document_id)
        
        return {
            "success": True,
            "message": f"Document deleted successfully: {document_id}",
            "document_id": document_id
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting document: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete document: {str(e)}"
        )


@router.get("/{document_id}/chunks")
async def get_document_chunks(
    document_id: str,
    db: Session = Depends(get_db)
):
    """
    Get all chunks for a document
    
    **Path Parameters:**
    - document_id: Document identifier
    
    **Returns:**
    - List of chunks with text and metadata
    """
    try:
        # Check if document exists
        document = DocumentCRUD.get_document_by_id(db, document_id)
        if not document:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Document not found: {document_id}"
            )
        
        # Get chunks
        chunks = ChunkCRUD.get_chunks_by_document(db, document_id)
        
        chunk_list = []
        for chunk in chunks:
            chunk_list.append(ChunkData(
                chunk_id=chunk.chunk_id,
                text=chunk.chunk_text,
                chunk_index=chunk.chunk_index,
                document_id=chunk.document_id,
                metadata={
                    "chunk_size": chunk.chunk_size,
                    "created_at": chunk.created_at.isoformat() if chunk.created_at else None,
                    "has_embedding": chunk.embedding is not None
                }
            ))
        
        return {
            "success": True,
            "document_id": document_id,
            "chunk_count": len(chunk_list),
            "chunks": chunk_list
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting chunks: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get chunks: {str(e)}"
        )


@router.get("/test/parse-text")
async def test_text_parser():
    """
    Test endpoint for text parser
    
    This endpoint tests the text parsing functionality with sample content.
    """
    try:
        # Create a temporary test file
        test_content = """This is a test document.
        
        It has multiple paragraphs to test the parsing functionality.

        This is the third paragraph with some more content to make it interesting.
        The parser should handle this correctly and extract all the text.
        """

        # Create temporary file
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write(test_content)
            temp_path = Path(f.name)
        
        # Parse the file
        result = await text_parser.parse(temp_path)
        
        # Clean up
        temp_path.unlink()
        
        return {
            "success": result["success"],
            "content_length": len(result["content"]),
            "metadata": result["metadata"],
            "sample_content": result["content"][:200]
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Test failed: {str(e)}"
        )


@router.get("/test/chunking")
async def test_chunking():
    """
    Test endpoint for text chunking
    
    This endpoint demonstrates how text is split into chunks.
    """
    try:
        # Sample text
        sample_text = """
        Artificial Intelligence (AI) is transforming how we live and work. 
        Machine learning, a subset of AI, enables computers to learn from data without explicit programming.
        
        Deep learning, using neural networks, has revolutionized fields like computer vision and natural language processing.
        These technologies power applications from voice assistants to autonomous vehicles.
        
        As AI continues to advance, it raises important questions about ethics, privacy, and the future of work.
        Responsible development and deployment of AI systems is crucial for ensuring beneficial outcomes for society.
        """ * 3  # Repeat to make it longer
        
        # Chunk the text
        chunks = text_chunker.chunk_text(sample_text, preserve_paragraphs=True)
        
        return {
            "success": True,
            "original_length": len(sample_text),
            "chunk_count": len(chunks),
            "chunk_size": text_chunker.chunk_size,
            "chunk_overlap": text_chunker.chunk_overlap,
            "chunks": [
                {
                    "index": i,
                    "length": len(chunk),
                    "preview": chunk[:100] + "..." if len(chunk) > 100 else chunk
                }
                for i, chunk in enumerate(chunks)
            ]
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Test failed: {str(e)}"
        )