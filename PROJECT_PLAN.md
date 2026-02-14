# Epstein Files Search Platform - Build Plan

## Goal
Build an AI-powered search platform for the Epstein files released by justice.gov

## Timeline
Overnight build (8 hours)

## Tech Stack
- **Frontend**: Next.js 15, TypeScript, Tailwind CSS
- **Backend**: Next.js API routes
- **Document Processing**: pdf-parse, cheerio, axios
- **AI/Search**: OpenAI API (embeddings + GPT for analysis)
- **Storage**: File system (JSON) for MVP, can upgrade later
- **Deployment**: Vercel

## Architecture

### Phase 1: Document Scraping (1-2 hours)
- Scrape PDF links from justice.gov/epstein
- Download PDFs to local storage
- Extract metadata (document ID, dataset, etc.)

### Phase 2: Text Extraction (1-2 hours)
- Parse PDFs and extract text
- Chunk text into manageable pieces
- Store in JSON format with metadata

### Phase 3: Search Implementation (2-3 hours)
- Create OpenAI embeddings for document chunks
- Implement semantic search API
- Add LLM-powered summarization

### Phase 4: Frontend (1-2 hours)
- Simple search interface
- Results display with highlights
- Document viewer/preview

### Phase 5: Deployment (30 min - 1 hour)
- Push to GitHub
- Deploy to Vercel
- Environment variables setup

## MVP Features
1. Search across all Epstein documents
2. Semantic search (not just keyword matching)
3. AI-powered summaries of relevant documents
4. Document preview/download links
5. Filter by dataset

## Future Enhancements (post-MVP)
- Proper vector database (Pinecone/Weaviate)
- Advanced filters (date, people, locations)
- Saved searches
- Email alerts for new documents
- API access for researchers
- Premium tier

## Progress Tracking
- [ ] Next.js project setup
- [ ] Document scraper implemented
- [ ] PDF parser working
- [ ] Embeddings generated
- [ ] Search API functional
- [ ] Frontend UI complete
- [ ] Deployed to Vercel
- [ ] Testing complete

## Notes
- Start with Data Set 1 (50 docs) for testing
- Expand to full dataset once working
- Use GPT-4o-mini for cost efficiency during development
- Switch to GPT-5 for production if needed
