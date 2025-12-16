from typing import Dict, Any
import pypdf
from docx import Document
import pandas as pd
from pathlib import Path


class DocumentParser:
    @staticmethod
    def parse_pdf(file_path: str) -> Dict[str, Any]:
        text = ""
        num_pages = 0
        
        with open(file_path, 'rb') as file:
            pdf_reader = pypdf.PdfReader(file)
            num_pages = len(pdf_reader.pages)
            
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
        
        return {
            "text": text,
            "num_pages": num_pages,
            "metadata": {}
        }
    
    @staticmethod
    def parse_docx(file_path: str) -> Dict[str, Any]:
        doc = Document(file_path)
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        
        return {
            "text": text,
            "num_pages": None,
            "metadata": {}
        }
    
    @staticmethod
    def parse_txt(file_path: str) -> Dict[str, Any]:
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
        
        return {
            "text": text,
            "num_pages": None,
            "metadata": {}
        }
    
    @staticmethod
    def parse_csv(file_path: str) -> Dict[str, Any]:
        df = pd.read_csv(file_path)
        text = df.to_string()
        
        return {
            "text": text,
            "num_pages": None,
            "metadata": {
                "rows": len(df),
                "columns": len(df.columns)
            }
        }
    
    @staticmethod
    def parse_file(file_path: str) -> Dict[str, Any]:
        extension = Path(file_path).suffix.lower()
        
        parsers = {
            '.pdf': DocumentParser.parse_pdf,
            '.docx': DocumentParser.parse_docx,
            '.txt': DocumentParser.parse_txt,
            '.md': DocumentParser.parse_txt,
            '.csv': DocumentParser.parse_csv,
        }
        
        parser = parsers.get(extension)
        if not parser:
            raise ValueError(f"Unsupported file type: {extension}")
        
        return parser(file_path)

