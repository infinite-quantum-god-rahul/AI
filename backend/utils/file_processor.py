import os
import logging
from typing import Optional
from fastapi import UploadFile, HTTPException
import PyPDF2
from docx import Document
import io

from config import settings

logger = logging.getLogger(__name__)

class FileProcessor:
    def __init__(self):
        self.max_file_size = settings.max_file_size
        self.allowed_extensions = settings.allowed_file_types
        self.upload_directory = settings.upload_directory

    def is_valid_file(self, file: UploadFile) -> bool:
        """Validate uploaded file"""
        try:
            # Check file size
            if file.size and file.size > self.max_file_size:
                return False
            
            # Check file extension
            if not file.filename:
                return False
            
            file_extension = os.path.splitext(file.filename)[1].lower()
            if file_extension not in self.allowed_extensions:
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"File validation error: {str(e)}")
            return False

    async def process_file(self, file: UploadFile) -> str:
        """Process uploaded file and extract text content"""
        try:
            # Read file content
            content = await file.read()
            
            # Determine file type and extract text
            file_extension = os.path.splitext(file.filename)[1].lower()
            
            if file_extension == '.pdf':
                text_content = self._extract_pdf_text(content)
            elif file_extension in ['.docx', '.doc']:
                text_content = self._extract_docx_text(content)
            else:
                raise HTTPException(
                    status_code=400,
                    detail=f"Unsupported file type: {file_extension}"
                )
            
            if not text_content.strip():
                raise HTTPException(
                    status_code=400,
                    detail="No text content found in the uploaded file"
                )
            
            return text_content
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"File processing error: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Error processing file: {str(e)}"
            )

    def _extract_pdf_text(self, content: bytes) -> str:
        """Extract text from PDF file"""
        try:
            pdf_file = io.BytesIO(content)
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            
            return text.strip()
            
        except Exception as e:
            logger.error(f"PDF extraction error: {str(e)}")
            raise Exception(f"Failed to extract text from PDF: {str(e)}")

    def _extract_docx_text(self, content: bytes) -> str:
        """Extract text from DOCX file"""
        try:
            doc_file = io.BytesIO(content)
            doc = Document(doc_file)
            
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            
            return text.strip()
            
        except Exception as e:
            logger.error(f"DOCX extraction error: {str(e)}")
            raise Exception(f"Failed to extract text from DOCX: {str(e)}")

    def save_file(self, file: UploadFile, filename: str) -> str:
        """Save uploaded file to disk"""
        try:
            # Ensure upload directory exists
            os.makedirs(self.upload_directory, exist_ok=True)
            
            # Create file path
            file_path = os.path.join(self.upload_directory, filename)
            
            # Save file
            with open(file_path, "wb") as buffer:
                content = file.file.read()
                buffer.write(content)
            
            return file_path
            
        except Exception as e:
            logger.error(f"File save error: {str(e)}")
            raise Exception(f"Failed to save file: {str(e)}")

    def delete_file(self, file_path: str) -> bool:
        """Delete file from disk"""
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                return True
            return False
            
        except Exception as e:
            logger.error(f"File deletion error: {str(e)}")
            return False

    def get_file_info(self, file: UploadFile) -> dict:
        """Get file information"""
        return {
            "filename": file.filename,
            "content_type": file.content_type,
            "size": file.size,
            "extension": os.path.splitext(file.filename)[1].lower() if file.filename else None
        }
