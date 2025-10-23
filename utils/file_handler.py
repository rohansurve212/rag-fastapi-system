import os
import hashlib
import aiofiles
from pathlib import Path
from typing import Tuple, Optional
from fastapi import UploadFile, HTTPException
from config import settings
import logging

logger = logging.getLogger(__name__)


class FileHandler:
    """
    Utility class for handling file operations
    """
    
    def __init__(self):
        self.upload_dir = Path(settings.upload_dir)
        self.max_size = settings.max_upload_size
        self.allowed_extensions = settings.allowed_extensions
        
        # Ensure upload directory exists
        self.upload_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"Upload directory: {self.upload_dir}")
    
    
    def validate_file(self, file: UploadFile) -> Tuple[bool, Optional[str]]:
        """
        Validate uploaded file
        
        Args:
            file: Uploaded file object
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        # Check if file has a filename
        if not file.filename:
            return False, "No filename provided"
        
        # Check file extension
        file_ext = Path(file.filename).suffix.lower()
        if file_ext not in self.allowed_extensions:
            return False, f"File type {file_ext} not allowed. Allowed types: {', '.join(self.allowed_extensions)}"
        
        # Check file size (if content_type is available)
        # Note: We'll check actual size during reading
        
        return True, None
    
    
    def generate_file_hash(self, content: bytes) -> str:
        """
        Generate SHA-256 hash of file content
        
        Args:
            content: File content as bytes
            
        Returns:
            Hexadecimal hash string
        """
        return hashlib.sha256(content).hexdigest()
    
    
    def get_safe_filename(self, filename: str, file_hash: str) -> str:
        """
        Generate a safe filename using hash and original extension
        
        Args:
            filename: Original filename
            file_hash: Hash of file content
            
        Returns:
            Safe filename string
        """
        ext = Path(filename).suffix.lower()
        # Use first 16 characters of hash + extension
        return f"{file_hash[:16]}{ext}"
    
    
    async def save_file(self, file: UploadFile) -> Tuple[Path, str, int]:
        """
        Save uploaded file to disk
        
        Args:
            file: Uploaded file object
            
        Returns:
            Tuple of (file_path, file_hash, file_size)
            
        Raises:
            HTTPException: If file is too large or other errors occur
        """
        try:
            # Read file content
            content = await file.read()
            file_size = len(content)
            
            # Check file size
            if file_size > self.max_size:
                max_mb = self.max_size / (1024 * 1024)
                actual_mb = file_size / (1024 * 1024)
                raise HTTPException(
                    status_code=413,
                    detail=f"File too large. Max size: {max_mb:.2f}MB, Uploaded: {actual_mb:.2f}MB"
                )
            
            # Generate hash and safe filename
            file_hash = self.generate_file_hash(content)
            safe_filename = self.get_safe_filename(file.filename, file_hash)
            file_path = self.upload_dir / safe_filename
            
            # Save file
            async with aiofiles.open(file_path, 'wb') as f:
                await f.write(content)
            
            logger.info(f"File saved: {safe_filename} ({file_size} bytes)")
            
            return file_path, file_hash, file_size
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error saving file: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Error saving file: {str(e)}"
            )
        finally:
            # Reset file pointer
            await file.seek(0)
    
    
    async def delete_file(self, file_path: Path) -> bool:
        """
        Delete a file from disk
        
        Args:
            file_path: Path to the file
            
        Returns:
            True if deleted, False otherwise
        """
        try:
            if file_path.exists():
                file_path.unlink()
                logger.info(f"File deleted: {file_path}")
                return True
            return False
        except Exception as e:
            logger.error(f"Error deleting file: {str(e)}")
            return False
    
    
    def get_file_info(self, file_path: Path) -> dict:
        """
        Get information about a file
        
        Args:
            file_path: Path to the file
            
        Returns:
            Dictionary with file information
        """
        if not file_path.exists():
            return {}
        
        stat = file_path.stat()
        return {
            "filename": file_path.name,
            "size": stat.st_size,
            "created": stat.st_ctime,
            "modified": stat.st_mtime,
            "extension": file_path.suffix.lower()
        }


# Create singleton instance
file_handler = FileHandler()