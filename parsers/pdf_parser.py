from pathlib import Path
from typing import Dict, List
import PyPDF2
from pdf2image import convert_from_path
import pytesseract
from PIL import Image
import logging

logger = logging.getLogger(__name__)


class PDFParser:
    """
    Parser for PDF files with OCR support
    """
    
    def __init__(self):
        """
        Initialize PDF parser
        """
        self.use_ocr = True
        logger.info("PDF Parser initialized with OCR support")
    
    
    async def parse(self, file_path: Path, use_ocr: bool = True) -> Dict:
        """
        Parse a PDF file and extract its content
        
        Args:
            file_path: Path to the PDF file
            use_ocr: Whether to use OCR for image-based PDFs
            
        Returns:
            Dictionary containing parsed text and metadata
        """
        try:
            logger.info(f"Parsing PDF file: {file_path}")
            
            # Try text extraction first
            content, metadata = self._extract_text(file_path)
            
            # If no text found and OCR is enabled, try OCR
            if use_ocr and (not content or len(content.strip()) < 100):
                logger.info("Text extraction yielded minimal content, attempting OCR...")
                ocr_content = self._extract_text_with_ocr(file_path)
                if len(ocr_content) > len(content):
                    content = ocr_content
                    metadata["extraction_method"] = "ocr"
                else:
                    metadata["extraction_method"] = "text"
            else:
                metadata["extraction_method"] = "text"
            
            result = {
                "content": content,
                "metadata": metadata,
                "success": True,
                "error": None
            }
            
            logger.info(f"PDF parsed successfully: {len(content)} characters, {metadata['page_count']} pages")
            return result
            
        except Exception as e:
            logger.error(f"Error parsing PDF: {str(e)}")
            return {
                "content": "",
                "metadata": {},
                "success": False,
                "error": str(e)
            }
    
    
    def _extract_text(self, file_path: Path) -> tuple:
        """
        Extract text from PDF using PyPDF2
        
        Args:
            file_path: Path to PDF file
            
        Returns:
            Tuple of (text_content, metadata)
        """
        text_content = []
        
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                page_count = len(pdf_reader.pages)
                
                # Extract text from each page
                for page_num, page in enumerate(pdf_reader.pages):
                    try:
                        text = page.extract_text()
                        if text:
                            text_content.append(text)
                    except Exception as e:
                        logger.warning(f"Error extracting text from page {page_num + 1}: {str(e)}")
                
                # Get metadata
                metadata = {
                    "filename": file_path.name,
                    "file_type": "pdf",
                    "extension": ".pdf",
                    "page_count": page_count,
                    "has_content": bool(text_content)
                }
                
                # Add PDF info if available
                if pdf_reader.metadata:
                    if pdf_reader.metadata.get('/Title'):
                        metadata["title"] = pdf_reader.metadata.get('/Title')
                    if pdf_reader.metadata.get('/Author'):
                        metadata["author"] = pdf_reader.metadata.get('/Author')
                    if pdf_reader.metadata.get('/Subject'):
                        metadata["subject"] = pdf_reader.metadata.get('/Subject')
                
                full_text = "\n\n".join(text_content)
                metadata["character_count"] = len(full_text)
                metadata["word_count"] = len(full_text.split())
                
                return full_text, metadata
                
        except Exception as e:
            logger.error(f"Error in text extraction: {str(e)}")
            return "", {"error": str(e)}
    
    
    def _extract_text_with_ocr(self, file_path: Path) -> str:
        """
        Extract text from PDF using OCR (for scanned PDFs)
        
        Args:
            file_path: Path to PDF file
            
        Returns:
            Extracted text content
        """
        try:
            logger.info("Starting OCR extraction...")
            
            # Convert PDF to images
            images = convert_from_path(str(file_path), dpi=300)
            
            # Perform OCR on each page
            text_content = []
            for i, image in enumerate(images):
                logger.info(f"Processing page {i + 1}/{len(images)} with OCR")
                text = pytesseract.image_to_string(image, lang='eng')
                if text:
                    text_content.append(text)
            
            full_text = "\n\n".join(text_content)
            logger.info(f"OCR extraction complete: {len(full_text)} characters")
            
            return full_text
            
        except Exception as e:
            logger.error(f"Error in OCR extraction: {str(e)}")
            return ""
    
    
    async def parse_multiple(self, file_paths: List[Path], use_ocr: bool = True) -> List[Dict]:
        """
        Parse multiple PDF files
        
        Args:
            file_paths: List of PDF file paths
            use_ocr: Whether to use OCR
            
        Returns:
            List of parsed results
        """
        results = []
        for file_path in file_paths:
            result = await self.parse(file_path, use_ocr)
            results.append(result)
        return results


# Create singleton instance
pdf_parser = PDFParser()