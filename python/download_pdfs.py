#!/usr/bin/env python3
"""
Download all Epstein investigation PDFs from justice.gov
Handles the age verification and proper PDF downloads
"""
import json
import os
import time
from pathlib import Path
import requests
from urllib.parse import urljoin
import concurrent.futures
from tqdm import tqdm

# Base URL
BASE_URL = "https://www.justice.gov"

def download_pdf(url: str, output_path: Path, session: requests.Session) -> bool:
    """Download a single PDF with proper handling"""
    try:
        # Make request with proper headers to bypass age verification
        response = session.get(url, stream=True, timeout=30)
        response.raise_for_status()
        
        # Check if we actually got a PDF
        content_type = response.headers.get('content-type', '')
        if 'application/pdf' not in content_type:
            print(f"⚠️  Not a PDF: {url} (got {content_type})")
            return False
        
        # Save the PDF
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        return True
    except Exception as e:
        print(f"❌ Error downloading {url}: {e}")
        return False

def main():
    # Load the document links
    links_file = Path(__file__).parent.parent / 'data' / 'document-links.json'
    with open(links_file) as f:
        documents = json.load(f)
    
    print(f"📄 Found {len(documents)} documents to download")
    
    # Create session with proper headers
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
        'Accept': 'application/pdf',
    })
    
    # Set age verification cookie
    session.cookies.set('age_verified', '1', domain='.justice.gov')
    
    # Download PDFs
    output_dir = Path(__file__).parent.parent / 'data' / 'pdfs'
    
    success = 0
    failed = 0
    skipped = 0
    
    for doc in tqdm(documents, desc="Downloading PDFs"):
        url = doc['url']
        dataset = doc['dataset']
        filename = doc['filename']
        
        output_path = output_dir / f"dataset-{dataset}" / filename
        
        # Skip if already downloaded
        if output_path.exists() and output_path.stat().st_size > 1000:
            skipped += 1
            continue
        
        # Download
        if download_pdf(url, output_path, session):
            success += 1
        else:
            failed += 1
        
        # Rate limiting
        time.sleep(0.5)
    
    print(f"\n✅ Success: {success}")
    print(f"❌ Failed: {failed}")
    print(f"⏭️  Skipped: {skipped}")

if __name__ == "__main__":
    main()
