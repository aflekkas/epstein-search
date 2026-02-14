# Deployment Guide

## Railway Deployment (Easiest)

### Option 1: Railway Dashboard (Recommended)

1. Go to https://railway.app/dashboard
2. Click "New Project" → "Deploy from GitHub repo"
3. Select `aflekkas/epstein-search`
4. Railway will auto-detect the Dockerfile
5. Add environment variable:
   - `OPENAI_API_KEY`: Your OpenAI API key
6. Deploy!

Railway will:
- Build the Docker image
- Deploy the FastAPI server
- Give you a public URL like `https://epstein-search-production.up.railway.app`

### Option 2: Railway CLI

```bash
# Install CLI
npm install -g @railway/cli

# Login
railway login

# Link to project
railway link

# Add environment variables
railway variables set OPENAI_API_KEY=sk-...

# Deploy
railway up
```

## Manual VPS Deployment

If you want to run on your own VPS:

### Requirements
- Python 3.13+
- 2GB+ RAM
- Docker (recommended) OR Python virtual environment

### With Docker

```bash
# Build image
docker build -t epstein-rag .

# Run container
docker run -d \
  -p 8000:8000 \
  -e OPENAI_API_KEY=sk-... \
  --name epstein-rag \
  epstein-rag
```

### Without Docker

```bash
# Install system packages (Debian/Ubuntu)
sudo apt install python3-venv python3-pip

# Create virtual environment
cd python
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Download and process documents
python download_pdfs.py
python process_documents.py

# Run API server (with process manager)
pip install gunicorn
gunicorn rag_api:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
```

## Frontend Deployment (Vercel)

Once the backend is deployed:

1. Update `next.config.ts` with backend URL:
```typescript
env: {
  NEXT_PUBLIC_API_URL: 'https://your-railway-url.railway.app'
}
```

2. Deploy to Vercel:
```bash
npm install -g vercel
vercel --prod
```

## Environment Variables

Required for backend:
- `OPENAI_API_KEY`: OpenAI API key
- `PORT`: (Optional) Port to run on (default: 8000)

## Post-Deployment

1. Download PDFs: `curl -X POST https://your-api.railway.app/admin/download`
2. Process documents: `curl -X POST https://your-api.railway.app/admin/process`
3. Test query: `curl -X POST https://your-api.railway.app/query -d '{"question":"test"}'`

## Monitoring

Railway provides built-in:
- Logs
- Metrics
- Auto-scaling
- SSL certificates

Access at: https://railway.app/dashboard
