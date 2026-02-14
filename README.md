# Epstein Files RAG Search

AI-powered search platform for the Epstein investigation documents released by the U.S. Department of Justice.

**Live Demo:** (Coming soon)  
**GitHub:** https://github.com/aflekkas/epstein-search

## 🎯 What is this?

The DOJ released 524 documents from the Epstein investigation, but their search tool is limited. This project provides:

- **Semantic search** across all documents (not just keyword matching)
- **AI-powered Q&A** - ask questions in natural language
- **Source citations** - see which documents support each answer
- **Better than the gov site** - handles handwritten docs, OCR issues, complex queries

## 🚀 Quick Start

### Backend (Python RAG System)

The core search functionality is built in Python:

```bash
cd python
pip install -r requirements.txt
python download_pdfs.py      # Download all PDFs
python process_documents.py  # Create embeddings
python rag_api.py           # Start API server
```

See `python/README.md` for detailed instructions.

### Frontend (Next.js)

Coming soon - simple search interface.

```bash
npm install
npm run dev
```

## 📊 Data

- **524 documents** from 12 data sets
- Released: February 13, 2026
- Source: https://www.justice.gov/...
- Includes: memos, correspondence, audio files, flight logs, etc.

## 🛠 Tech Stack

- **Backend**: Python, FastAPI, LangChain, ChromaDB
- **Frontend**: Next.js 15, TypeScript, Tailwind CSS
- **AI**: OpenAI (embeddings + GPT-5.2)
- **Storage**: Local vector store (ChromaDB)

## 💡 Use Cases

1. **Research** - Journalists, investigators, researchers
2. **Content Creation** - YouTube videos, Twitter threads, articles
3. **Public Access** - Better search than government site
4. **API Access** - Programmatic queries for data analysis

## 📝 API Endpoints

```bash
POST /query       # Ask questions (RAG)
GET  /search      # Semantic search
GET  /stats       # System info
```

Full API docs at `http://localhost:8000/docs` when running.

## 🗺️ Roadmap

- [x] Document scraping
- [x] RAG system (Python)
- [x] API server
- [ ] Complete PDF downloads
- [ ] Frontend UI
- [ ] Authentication
- [ ] Advanced filters
- [ ] Deployment
- [ ] API rate limiting
- [ ] Premium features

## 📄 License

MIT - See LICENSE file

## 🙏 Contributing

Contributions welcome! Open an issue or PR.

## 🔗 Links

- [Project Plan](PROJECT_PLAN.md)
- [Python README](python/README.md)
- [DOJ Source](https://www.justice.gov/...)
