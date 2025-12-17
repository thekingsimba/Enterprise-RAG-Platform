from typing import TypedDict, List, Dict, Any
from langgraph.graph import StateGraph, END
from app.services.embedding_service import EmbeddingService
from app.services.vector_store_service import VectorStoreService
from app.services.llm_service import LLMService
import logging

logger = logging.getLogger(__name__)


class RAGState(TypedDict):
    query: str
    organization_id: str
    chat_history: List[Dict[str, str]]
    rewritten_query: str
    context: str
    sources: List[Dict[str, Any]]
    answer: str
    error: str


class RAGWorkflow:
    def __init__(self):
        self.embedding_service = EmbeddingService()
        self.vector_store_service = VectorStoreService()
        self.llm_service = LLMService()
        self.workflow = self._build_workflow()
    
    def _build_workflow(self) -> StateGraph:
        workflow = StateGraph(RAGState)
        
        workflow.add_node("rewrite_query", self.rewrite_query)
        workflow.add_node("retrieve_context", self.retrieve_context)
        workflow.add_node("generate_answer", self.generate_answer)
        
        workflow.set_entry_point("rewrite_query")
        workflow.add_edge("rewrite_query", "retrieve_context")
        workflow.add_edge("retrieve_context", "generate_answer")
        workflow.add_edge("generate_answer", END)
        
        return workflow.compile()
    
    async def rewrite_query(self, state: RAGState) -> RAGState:
        try:
            query = state["query"]
            chat_history = state.get("chat_history", [])
            
            if not chat_history:
                state["rewritten_query"] = query
                return state
            
            rewrite_prompt = f"""Given the conversation history and the follow-up question, 
rephrase the follow-up question to be a standalone question.

Chat History:
{self._format_history(chat_history[-3:])}

Follow-up Question: {query}

Standalone Question:"""
            
            messages = [{"role": "user", "content": rewrite_prompt}]
            rewritten = await self.llm_service.generate_response(
                query=rewrite_prompt,
                context="",
                chat_history=[]
            )
            
            state["rewritten_query"] = rewritten.strip()
            logger.info(f"Rewritten query: {state['rewritten_query']}")
            
        except Exception as e:
            logger.error(f"Error rewriting query: {e}")
            state["rewritten_query"] = state["query"]
        
        return state
    
    async def retrieve_context(self, state: RAGState) -> RAGState:
        try:
            query = state["rewritten_query"]
            organization_id = state["organization_id"]
            
            query_embedding = self.embedding_service.create_embedding(query)
            
            namespace = f"org_{organization_id}"
            results = self.vector_store_service.query_vectors(
                query_vector=query_embedding,
                namespace=namespace,
                top_k=5
            )
            
            context_parts = []
            sources = []
            
            for idx, match in enumerate(results):
                metadata = match.metadata
                score = match.score
                
                context_parts.append(
                    f"[Document {idx + 1}]\n"
                    f"Source: {metadata.get('filename', 'Unknown')}\n"
                    f"Content: {metadata.get('content', match.id)}\n"
                    f"Relevance: {score:.2f}\n"
                )
                
                sources.append({
                    "chunk_id": match.id,
                    "document_id": metadata.get("document_id"),
                    "filename": metadata.get("filename"),
                    "score": score,
                    "content": metadata.get("content", "")[:200]
                })
            
            state["context"] = "\n\n".join(context_parts)
            state["sources"] = sources
            
        except Exception as e:
            logger.error(f"Error retrieving context: {e}")
            state["context"] = ""
            state["sources"] = []
            state["error"] = str(e)
        
        return state
    
    async def generate_answer(self, state: RAGState) -> RAGState:
        try:
            if not state["context"]:
                state["answer"] = "I couldn't find relevant information in the knowledge base to answer your question."
                return state
            
            answer = await self.llm_service.generate_response(
                query=state["query"],
                context=state["context"],
                chat_history=state.get("chat_history", [])
            )
            
            state["answer"] = answer
            
        except Exception as e:
            logger.error(f"Error generating answer: {e}")
            state["answer"] = "I encountered an error while generating the answer."
            state["error"] = str(e)
        
        return state
    
    def _format_history(self, history: List[Dict[str, str]]) -> str:
        formatted = []
        for msg in history:
            role = msg["role"].capitalize()
            content = msg["content"]
            formatted.append(f"{role}: {content}")
        return "\n".join(formatted)
    
    async def run(
        self,
        query: str,
        organization_id: str,
        chat_history: List[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        initial_state: RAGState = {
            "query": query,
            "organization_id": organization_id,
            "chat_history": chat_history or [],
            "rewritten_query": "",
            "context": "",
            "sources": [],
            "answer": "",
            "error": ""
        }
        
        final_state = await self.workflow.ainvoke(initial_state)
        
        return {
            "answer": final_state["answer"],
            "sources": final_state["sources"],
            "rewritten_query": final_state.get("rewritten_query", query)
        }


