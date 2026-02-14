import axios from 'axios';
import * as fs from 'fs';
import * as path from 'path';

interface DocumentLink {
  id: string;
  url: string;
  dataset: number;
  filename: string;
}

async function downloadPDF(doc: DocumentLink, outputDir: string): Promise<boolean> {
  try {
    console.log(`Downloading ${doc.filename}...`);
    
    const response = await axios.get(doc.url, {
      responseType: 'arraybuffer',
      timeout: 30000,
      headers: {
        'User-Agent': 'Mozilla/5.0 (compatible; EpsteinSearchBot/1.0)'
      }
    });
    
    const datasetDir = path.join(outputDir, `dataset-${doc.dataset}`);
    if (!fs.existsSync(datasetDir)) {
      fs.mkdirSync(datasetDir, { recursive: true });
    }
    
    const filePath = path.join(datasetDir, doc.filename);
    fs.writeFileSync(filePath, response.data);
    
    console.log(`✓ Downloaded ${doc.filename}`);
    return true;
  } catch (error) {
    console.error(`✗ Failed to download ${doc.filename}:`, error);
    return false;
  }
}

async function downloadAllPDFs(limit: number = 100) {
  const linksPath = path.join(process.cwd(), 'data', 'document-links.json');
  
  if (!fs.existsSync(linksPath)) {
    console.error('document-links.json not found. Run scrape-links.ts first.');
    process.exit(1);
  }
  
  const allLinks: DocumentLink[] = JSON.parse(fs.readFileSync(linksPath, 'utf-8'));
  const linksToDownload = allLinks.slice(0, limit);
  
  console.log(`Downloading ${linksToDownload.length} PDFs...`);
  
  const outputDir = path.join(process.cwd(), 'data', 'pdfs');
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }
  
  let successCount = 0;
  let failCount = 0;
  
  for (const doc of linksToDownload) {
    const success = await downloadPDF(doc, outputDir);
    if (success) {
      successCount++;
    } else {
      failCount++;
    }
    
    // Be nice to the server - wait between downloads
    await new Promise(resolve => setTimeout(resolve, 2000));
  }
  
  console.log(`\nDownload complete:`);
  console.log(`✓ Success: ${successCount}`);
  console.log(`✗ Failed: ${failCount}`);
}

// Get limit from command line args or default to 100
const limit = parseInt(process.argv[2]) || 100;
downloadAllPDFs(limit);
