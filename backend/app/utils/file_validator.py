import magic
from pathlib import Path
from typing import Tuple
from app.core.config import settings


class FileValidator:
    ALLOWED_MIME_TYPES = {
        '.pdf': ['application/pdf'],
        '.docx': [
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            'application/msword'
        ],
        '.txt': ['text/plain'],
        '.csv': ['text/csv', 'text/plain'],
        '.md': ['text/plain', 'text/markdown']
    }
    
    @staticmethod
    def validate_file(
        file_content: bytes,
        filename: str,
        max_size: int = None
    ) -> Tuple[bool, str]:
        if max_size is None:
            max_size = settings.MAX_FILE_SIZE
        
        if len(file_content) > max_size:
            return False, f"File size exceeds maximum allowed size of {max_size} bytes"
        
        file_extension = Path(filename).suffix.lower()
        
        if file_extension not in settings.ALLOWED_EXTENSIONS:
            return False, f"File type {file_extension} not allowed"
        
        mime_type = magic.from_buffer(file_content, mime=True)
        
        allowed_mimes = FileValidator.ALLOWED_MIME_TYPES.get(file_extension, [])
        if mime_type not in allowed_mimes:
            return False, f"File content does not match expected type for {file_extension}"
        
        if FileValidator._contains_malicious_content(file_content):
            return False, "File contains potentially malicious content"
        
        return True, "File is valid"
    
    @staticmethod
    def _contains_malicious_content(content: bytes) -> bool:
        suspicious_patterns = [
            b'<script',
            b'javascript:',
            b'eval(',
            b'exec(',
            b'<?php',
        ]
        
        content_lower = content.lower()
        for pattern in suspicious_patterns:
            if pattern in content_lower:
                return True
        
        return False
    
    @staticmethod
    def get_file_info(file_content: bytes) -> dict:
        mime_type = magic.from_buffer(file_content, mime=True)
        file_type = magic.from_buffer(file_content)
        
        return {
            "mime_type": mime_type,
            "file_type": file_type,
            "size_bytes": len(file_content),
            "size_mb": round(len(file_content) / (1024 * 1024), 2)
        }

