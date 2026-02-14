#!/usr/bin/env python3
"""
FastAPI server for RAG queries over Epstein documents
"""
from pathlib import Path
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Epstein Files RAG API")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize vector store and RAG chain
vector_dir = Path(__file__).parent.parent / 'data' / 'vectorstore'
embeddings = OpenAIEmbeddings()
vectorstore = None
qa_chain = None

def init_rag():
    """Initialize the RAG system"""
    global vectorstore, qa_chain
    
    if not vector_dir.exists():
        raise RuntimeError("Vector store not found. Run process_documents.py first.")
    
    vectorstore = Chroma(
        persist_directory=str(vector_dir),
        embedding_function=embeddings
    )
    
    # Create QA prompt template
    template = """Use the following pieces of context from the Epstein investigation documents to answer the question.
If you don't know the answer, just say that you don't know, don't try to make up an answer.
Always cite which document(s) you're referencing.

Context: {context}

Question: {question}

Answer:"""
    
    QA_PROMPT = PromptTemplate(
        template=template, input_variables=["context", "question"]
    )
    
    # Initialize QA chain
    llm = ChatOpenAI(model="gpt-5.2", temperature=0)
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vectorstore.as_retriever(search_kwargs={"k": 5}),
        return_source_documents=True,
        chain_type_kwargs={"prompt": QA_PROMPT}
    )

@app.on_event("startup")
async def startup_event():
    """Initialize RAG on startup"""
    init_rag()

class QueryRequest(BaseModel):
    question: str
    num_results: int = 5

class QueryResponse(BaseModel):
    answer: str
    sources: List[dict]

@app.get("/")
async def root():
    return {"message": "Epstein Files RAG API", "status": "running"}

@app.post("/query", response_model=QueryResponse)
async def query(request: QueryRequest):
    """
    Query the Epstein documents using RAG
    """
    try:
        result = qa_chain({"query": request.question})
        
        sources = []
        for doc in result['source_documents']:
            sources.append({
                'doc_id': doc.metadata.get('doc_id', 'unknown'),
                'filename': doc.metadata.get('filename', 'unknown'),
                'dataset': doc.metadata.get('dataset', 'unknown'),
                'chunk_index': doc.metadata.get('chunk_index', 0),
                'text': doc.page_content[:200] + "..."  # Preview
            })
        
        return QueryResponse(
            answer=result['result'],
            sources=sources
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/search")
async def search(q: str, k: int = 5):
    """
    Simple semantic search (no LLM)
    """
    try:
        docs = vectorstore.similarity_search(q, k=k)
        results = []
        for doc in docs:
            results.append({
                'doc_id': doc.metadata.get('doc_id', 'unknown'),
                'filename': doc.metadata.get('filename', 'unknown'),
                'dataset': doc.metadata.get('dataset', 'unknown'),
                'text': doc.page_content[:300] + "..."
            })
        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/stats")
async def stats():
    """Get statistics about the document corpus"""
    try:
        # This is a simple implementation - ChromaDB doesn't expose all stats easily
        return {
            "vector_store_ready": vectorstore is not None,
            "message": "RAG system is operational"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
