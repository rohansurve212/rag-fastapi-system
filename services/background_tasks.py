import logging
from pathlib import Path
from typing import List
from datetime import datetime

from database import db_manager, Document, DocumentChunk
from database.crud import DocumentCRUD, ChunkCRUD
from utils import text_chunker
from parsers import text_parser, pdf_parser
from services import openai_service

logger = logging.getLogger(__name__)


class BackgroundTaskService:
    """
    Service for handling background tasks like document processing
    """
    
    @staticmethod
    async def process_document(
        document_id: str,
        file_path: Path,
        filename: str,
        file_type: str
    ):
        """
        Process a document in the background:
        1. Parse document
        2. Chunk text
        3. Generate embeddings
        4. Store in database
        
        Args:
            document_id: Document identifier
            file_path: Path to uploaded file
            filename: Original filename
            file_type: File extension
        """
        try:
            logger.info(f"Starting background processing for document: {document_id}")
            
            with db_manager.get_session() as db:
                # Update status to processing
                DocumentCRUD.update_document_status(
                    db, 
                    document_id, 
                    'processing'
                )
            
            # Step 1: Parse document
            if file_type == 'txt':
                parse_result = await text_parser.parse(file_path)
            elif file_type == 'pdf':
                parse_result = await pdf_parser.parse(file_path, use_ocr=True)
            else:
                raise ValueError(f"Unsupported file type: {file_type}")
            
            if not parse_result["success"]:
                raise Exception(f"Failed to parse document: {parse_result['error']}")
            
            content = parse_result["content"]
            
            # Step 2: Chunk text
            chunks = text_chunker.chunk_text(content, preserve_paragraphs=True)
            logger.info(f"Document chunked into {len(chunks)} pieces")
            
            # Step 3: Generate embeddings for all chunks
            logger.info(f"Generating embeddings for {len(chunks)} chunks")
            embeddings = openai_service.create_embeddings_batch(chunks)
            
            # Step 4: Store chunks in database
            with db_manager.get_session() as db:
                chunks_data = []
                for i, (chunk_text, embedding) in enumerate(zip(chunks, embeddings)):
                    chunk_id = f"chunk_{document_id}_{i}"
                    chunks_data.append({
                        "chunk_id": chunk_id,
                        "document_id": document_id,
                        "chunk_text": chunk_text,
                        "chunk_index": i,
                        "chunk_size": len(chunk_text),
                        "embedding": embedding
                    })
                
                # Batch insert chunks
                ChunkCRUD.create_chunks_batch(db, chunks_data)
                
                # Update document chunk count and status
                DocumentCRUD.update_document_chunk_count(db, document_id, len(chunks))
                DocumentCRUD.update_document_status(
                    db,
                    document_id,
                    'completed',
                    processed_at=datetime.utcnow()
                )
            
            logger.info(f"Document processing completed: {document_id}")
            
        except Exception as e:
            logger.error(f"Error processing document {document_id}: {str(e)}", exc_info=True)
            
            # Update document status to failed
            try:
                with db_manager.get_session() as db:
                    DocumentCRUD.update_document_status(
                        db,
                        document_id,
                        'failed',
                        error_message=str(e)
                    )
            except Exception as db_error:
                logger.error(f"Failed to update error status: {str(db_error)}")


background_task_service = BackgroundTaskService()