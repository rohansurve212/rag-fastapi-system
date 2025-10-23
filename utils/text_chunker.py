from typing import List
from config import settings
import logging

logger = logging.getLogger(__name__)


class TextChunker:
    """
    Utility class for chunking text into smaller pieces
    for better embedding and retrieval
    """
    
    def __init__(
        self,
        chunk_size: int = None,
        chunk_overlap: int = None
    ):
        """
        Initialize text chunker
        
        Args:
            chunk_size: Maximum characters per chunk
            chunk_overlap: Number of overlapping characters between chunks
        """
        self.chunk_size = chunk_size or settings.chunk_size
        self.chunk_overlap = chunk_overlap or settings.chunk_overlap
        
        logger.info(f"TextChunker initialized: size={self.chunk_size}, overlap={self.chunk_overlap}")
    
    
    def chunk_text(self, text: str, preserve_paragraphs: bool = True) -> List[str]:
        """
        Split text into chunks with overlap
        
        Args:
            text: Text to chunk
            preserve_paragraphs: Try to split at paragraph boundaries
            
        Returns:
            List of text chunks
        """
        if not text or len(text) == 0:
            return []
        
        # If text is smaller than chunk size, return as single chunk
        if len(text) <= self.chunk_size:
            return [text.strip()]
        
        chunks = []
        
        if preserve_paragraphs:
            # Split by paragraphs first
            paragraphs = text.split('\n\n')
            current_chunk = ""
            
            for para in paragraphs:
                para = para.strip()
                if not para:
                    continue
                
                # If adding this paragraph exceeds chunk size
                if len(current_chunk) + len(para) + 2 > self.chunk_size:
                    if current_chunk:
                        chunks.append(current_chunk.strip())
                        # Add overlap from the end of current chunk
                        current_chunk = current_chunk[-self.chunk_overlap:] if len(current_chunk) > self.chunk_overlap else ""
                    
                    # If paragraph itself is larger than chunk size
                    if len(para) > self.chunk_size:
                        # Split the large paragraph
                        para_chunks = self._split_large_text(para)
                        chunks.extend(para_chunks[:-1])
                        current_chunk = para_chunks[-1] if para_chunks else ""
                    else:
                        current_chunk = para
                else:
                    # Add paragraph to current chunk
                    if current_chunk:
                        current_chunk += "\n\n" + para
                    else:
                        current_chunk = para
            
            # Add the last chunk
            if current_chunk:
                chunks.append(current_chunk.strip())
        else:
            # Simple character-based chunking
            chunks = self._split_large_text(text)
        
        logger.info(f"Text chunked into {len(chunks)} pieces")
        return chunks
    
    
    def _split_large_text(self, text: str) -> List[str]:
        """
        Split large text into chunks at sentence boundaries when possible
        
        Args:
            text: Text to split
            
        Returns:
            List of text chunks
        """
        chunks = []
        start = 0
        text_length = len(text)
        
        while start < text_length:
            # Calculate end position
            end = start + self.chunk_size
            
            # If this is the last chunk
            if end >= text_length:
                chunks.append(text[start:].strip())
                break
            
            # Try to find a sentence boundary (. ! ?) near the end
            chunk = text[start:end]
            
            # Look for sentence endings in the last 100 characters
            last_period = max(
                chunk.rfind('. '),
                chunk.rfind('! '),
                chunk.rfind('? ')
            )
            
            if last_period > self.chunk_size - 200:  # If found in reasonable range
                end = start + last_period + 1
            else:
                # Look for newline
                last_newline = chunk.rfind('\n')
                if last_newline > self.chunk_size - 200:
                    end = start + last_newline
                else:
                    # Look for space
                    last_space = chunk.rfind(' ')
                    if last_space > self.chunk_size - 100:
                        end = start + last_space
            
            chunks.append(text[start:end].strip())
            
            # Move start position with overlap
            start = end - self.chunk_overlap
        
        return chunks
    
    
    def chunk_with_metadata(self, text: str, metadata: dict = None) -> List[dict]:
        """
        Chunk text and attach metadata to each chunk
        
        Args:
            text: Text to chunk
            metadata: Metadata to attach to each chunk
            
        Returns:
            List of dictionaries with 'text' and 'metadata' keys
        """
        chunks = self.chunk_text(text)
        metadata = metadata or {}
        
        result = []
        for i, chunk in enumerate(chunks):
            result.append({
                "text": chunk,
                "metadata": {
                    **metadata,
                    "chunk_index": i,
                    "total_chunks": len(chunks),
                    "chunk_size": len(chunk)
                }
            })
        
        return result


# Create singleton instance
text_chunker = TextChunker()