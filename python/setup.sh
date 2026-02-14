#!/bin/bash
# Quick setup script for Epstein Files RAG system

set -e

echo "🔧 Setting up Epstein Files RAG system..."

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Check for OpenAI API key
if [ ! -f ../.env.local ]; then
    echo "⚠️  No .env.local file found"
    echo "Please create ../.env.local with your OpenAI API key:"
    echo "  OPENAI_API_KEY=sk-..."
    exit 1
fi

echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "  1. Download PDFs:          python download_pdfs.py"
echo "  2. Process documents:      python process_documents.py"
echo "  3. Start RAG API:          python rag_api.py"
echo ""
echo "Then visit http://localhost:8000/docs for API documentation"
