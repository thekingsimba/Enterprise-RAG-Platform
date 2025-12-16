from typing import List, Dict, Any
from langchain.text_splitter import RecursiveCharacterTextSplitter
from app.core.config import settings


class TextChunker:
    def __init__(
        self,
        chunk_size: int = settings.CHUNK_SIZE,
        chunk_overlap: int = settings.CHUNK_OVERLAP
    ):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", ". ", " ", ""]
        )
    
    def chunk_text(self, text: str, metadata: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        chunks = self.text_splitter.split_text(text)
        
        result = []
        for idx, chunk in enumerate(chunks):
            chunk_data = {
                "content": chunk,
                "chunk_index": idx,
                "metadata": metadata or {}
            }
            result.append(chunk_data)
        
        return result
    
    def chunk_documents(
        self,
        documents: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        all_chunks = []
        
        for doc in documents:
            text = doc.get("text", "")
            metadata = doc.get("metadata", {})
            
            chunks = self.chunk_text(text, metadata)
            all_chunks.extend(chunks)
        
        return all_chunks

