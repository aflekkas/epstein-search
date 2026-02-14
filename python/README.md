# Epstein Files RAG System

AI-powered search and Q&A over Epstein investigation documents.

## Setup

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Set up OpenAI API key:
```bash
# Create .env file in project root
echo "OPENAI_API_KEY=your-key-here" > ../.env.local
```

## Usage

### Step 1: Download PDFs

Download all Epstein investigation documents:

```bash
python download_pdfs.py
```

This will download ~524 PDFs from justice.gov into `data/pdfs/`.

### Step 2: Process Documents

Extract text and create vector embeddings:

```bash
python process_documents.py
```

This will:
- Extract text from all PDFs
- Chunk documents into smaller pieces
- Create OpenAI embeddings
- Store in ChromaDB vector database

### Step 3: Run RAG API

Start the FastAPI server:

```bash
python rag_api.py
```

API will be available at http://localhost:8000

## API Endpoints

### POST /query
Ask questions about the documents using RAG:

```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"question": "What companies did Epstein invest in?"}'
```

Response includes:
- AI-generated answer
- Source documents cited
- Document metadata

### GET /search
Simple semantic search (no LLM):

```bash
curl "http://localhost:8000/search?q=flight%20logs&k=5"
```

Returns top K most relevant document chunks.

### GET /stats
System statistics and health check:

```bash
curl http://localhost:8000/stats
```

## Frontend Integration

The Next.js frontend in the parent directory can connect to this API.

Update `next.config.ts` to proxy API requests:

```typescript
module.exports = {
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: 'http://localhost:8000/:path*'
      }
    ]
  }
}
```

## Architecture

- **download_pdfs.py**: Scrapes and downloads PDFs from justice.gov
- **process_documents.py**: Extracts text, chunks, and creates embeddings
- **rag_api.py**: FastAPI server with RAG endpoints
- **Vector Store**: ChromaDB (local, persistent)
- **Embeddings**: OpenAI text-embedding-3-small
- **LLM**: OpenAI GPT-5.2 (configurable)

## Data Structure

```
data/
├── document-links.json          # Scraped links (524 docs)
├── pdfs/                        # Downloaded PDFs
│   ├── dataset-1/
│   ├── dataset-2/
│   └── ...
├── processed/
│   └── documents.json           # Extracted text
└── vectorstore/                 # ChromaDB vector store
```

## Monetization Ideas

1. **Public Search Interface**: Free basic searches, paid for advanced features
2. **API Access**: Charge researchers/journalists for API usage
3. **Premium Features**: 
   - Saved searches
   - Email alerts for new documents
   - Advanced filtering
   - Bulk document analysis
4. **Content Generation**: Extract insights for Twitter threads, YouTube videos
5. **White-label**: Sell to news organizations

## Performance

- ~524 documents from justice.gov
- Processing time: ~10-15 min for full corpus
- Query latency: ~2-3 seconds (including LLM)
- Vector search: <100ms

## Next Steps

- [ ] Complete PDF downloads (all 524 docs)
- [ ] Optimize chunking strategy
- [ ] Add caching for common queries
- [ ] Build frontend UI
- [ ] Add authentication
- [ ] Deploy to production
