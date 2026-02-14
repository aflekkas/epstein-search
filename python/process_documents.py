#!/usr/bin/env python3
"""
Process PDFs and create vector embeddings for RAG
"""
import json
import os
from pathlib import Path
from typing import List, Dict
import pypdf
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.schema import Document
from tqdm import tqdm
from dotenv import load_dotenv

load_dotenv()

def extract_text_from_pdf(pdf_path: Path) -> tuple[str, dict]:
    """Extract text and metadata from a PDF"""
    try:
        reader = pypdf.PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        
        metadata = {
            'num_pages': len(reader.pages),
            'filename': pdf_path.name,
            'dataset': pdf_path.parent.name.replace('dataset-', ''),
        }
        
        return text, metadata
    except Exception as e:
        print(f"Error extracting {pdf_path}: {e}")
        return "", {}

def process_all_pdfs(pdfs_dir: Path, output_dir: Path):
    """Process all PDFs and save extracted text"""
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Find all PDFs
    pdf_files = list(pdfs_dir.rglob("*.pdf"))
    print(f"Found {len(pdf_files)} PDFs")
    
    documents = []
    
    for pdf_path in tqdm(pdf_files, desc="Extracting text"):
        text, metadata = extract_text_from_pdf(pdf_path)
        if text:
            doc_id = pdf_path.stem
            documents.append({
                'id': doc_id,
                'text': text,
                'metadata': metadata
            })
    
    # Save extracted documents
    output_file = output_dir / 'documents.json'
    with open(output_file, 'w') as f:
        json.dump(documents, f, indent=2)
    
    print(f"✅ Saved {len(documents)} documents to {output_file}")
    return documents

def create_vector_store(documents: List[dict], persist_dir: Path):
    """Create vector embeddings and store in ChromaDB"""
    print("Creating embeddings...")
    
    # Initialize text splitter
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
    )
    
    # Create LangChain documents
    langchain_docs = []
    for doc in tqdm(documents, desc="Chunking documents"):
        chunks = text_splitter.split_text(doc['text'])
        for i, chunk in enumerate(chunks):
            langchain_docs.append(Document(
                page_content=chunk,
                metadata={
                    **doc['metadata'],
                    'doc_id': doc['id'],
                    'chunk_index': i
                }
            ))
    
    print(f"Created {len(langchain_docs)} chunks from {len(documents)} documents")
    
    # Create embeddings and store
    embeddings = OpenAIEmbeddings()
    vectorstore = Chroma.from_documents(
        documents=langchain_docs,
        embedding=embeddings,
        persist_directory=str(persist_dir)
    )
    
    print(f"✅ Vector store created at {persist_dir}")
    return vectorstore

def main():
    base_dir = Path(__file__).parent.parent
    pdfs_dir = base_dir / 'data' / 'pdfs'
    processed_dir = base_dir / 'data' / 'processed'
    vector_dir = base_dir / 'data' / 'vectorstore'
    
    # Step 1: Extract text from PDFs
    documents = process_all_pdfs(pdfs_dir, processed_dir)
    
    # Step 2: Create vector store
    if documents:
        create_vector_store(documents, vector_dir)
    else:
        print("No documents to process!")

if __name__ == "__main__":
    main()
