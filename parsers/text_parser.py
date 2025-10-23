from pathlib import Path
from typing import Dict, List
import aiofiles
import logging

logger = logging.getLogger(__name__)


class TextParser:
    """
    Parser for plain text files
    """
    
    async def parse(self, file_path: Path) -> Dict:
        """
        Parse a text file and extract its content
        
        Args:
            file_path: Path to the text file
            
        Returns:
            Dictionary containing parsed text and metadata
        """
        try:
            logger.info(f"Parsing text file: {file_path}")
            
            # Read file content
            async with aiofiles.open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = await f.read()
            
            # Extract basic metadata
            metadata = self._extract_metadata(content, file_path)
            
            result = {
                "content": content,
                "metadata": metadata,
                "success": True,
                "error": None
            }
            
            logger.info(f"Text file parsed successfully: {len(content)} characters")
            return result
            
        except Exception as e:
            logger.error(f"Error parsing text file: {str(e)}")
            return {
                "content": "",
                "metadata": {},
                "success": False,
                "error": str(e)
            }
    
    
    def _extract_metadata(self, content: str, file_path: Path) -> Dict:
        """
        Extract metadata from text content
        
        Args:
            content: Text content
            file_path: Path to the file
            
        Returns:
            Dictionary with metadata
        """
        lines = content.split('\n')
        words = content.split()
        
        return {
            "filename": file_path.name,
            "file_type": "text",
            "extension": file_path.suffix.lower(),
            "character_count": len(content),
            "word_count": len(words),
            "line_count": len(lines),
            "has_content": bool(content.strip())
        }
    
    
    async def parse_multiple(self, file_paths: List[Path]) -> List[Dict]:
        """
        Parse multiple text files
        
        Args:
            file_paths: List of file paths
            
        Returns:
            List of parsed results
        """
        results = []
        for file_path in file_paths:
            result = await self.parse(file_path)
            results.append(result)
        return results


# Create singleton instance
text_parser = TextParser()