import * as fs from 'fs';
import * as path from 'path';

// Dynamic import for pdf-parse
async function loadPdfParse() {
  const pdfParse = await import('pdf-parse');
  return pdfParse.default || pdfParse;
}

interface ProcessedDocument {
  id: string;
  filename: string;
  dataset: number;
  text: string;
  pages: number;
  metadata: any;
  processed_at: string;
}

async function processPDF(filePath: string, pdfParse: any): Promise<ProcessedDocument | null> {
  try {
    const dataBuffer = fs.readFileSync(filePath);
    const data = await pdfParse(dataBuffer);
    
    const filename = path.basename(filePath);
    const id = filename.replace('.pdf', '');
    const datasetMatch = filePath.match(/dataset-(\d+)/);
    const dataset = datasetMatch ? parseInt(datasetMatch[1]) : 0;
    
    return {
      id,
      filename,
      dataset,
      text: data.text,
      pages: data.numpages,
      metadata: data.metadata,
      processed_at: new Date().toISOString()
    };
  } catch (error) {
    console.error(`Error processing ${filePath}:`, error);
    return null;
  }
}

async function findAllPDFs(dir: string): Promise<string[]> {
  const files: string[] = [];
  
  function traverse(currentPath: string) {
    const items = fs.readdirSync(currentPath);
    
    for (const item of items) {
      const fullPath = path.join(currentPath, item);
      const stat = fs.statSync(fullPath);
      
      if (stat.isDirectory()) {
        traverse(fullPath);
      } else if (item.endsWith('.pdf')) {
        files.push(fullPath);
      }
    }
  }
  
  traverse(dir);
  return files;
}

async function processAllPDFs() {
  const pdfsDir = path.join(process.cwd(), 'data', 'pdfs');
  const outputDir = path.join(process.cwd(), 'data', 'processed');
  
  if (!fs.existsSync(pdfsDir)) {
    console.error('PDFs directory not found. Run download-pdfs.ts first.');
    process.exit(1);
  }
  
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }
  
  console.log('Loading PDF parser...');
  const pdfParse = await loadPdfParse();
  
  console.log('Finding all PDFs...');
  const pdfFiles = await findAllPDFs(pdfsDir);
  console.log(`Found ${pdfFiles.length} PDFs to process`);
  
  const processed: ProcessedDocument[] = [];
  let successCount = 0;
  let failCount = 0;
  
  for (const pdfPath of pdfFiles) {
    console.log(`Processing ${path.basename(pdfPath)}...`);
    const result = await processPDF(pdfPath, pdfParse);
    
    if (result) {
      processed.push(result);
      successCount++;
      console.log(`✓ Processed (${result.pages} pages, ${result.text.length} chars)`);
    } else {
      failCount++;
      console.log(`✗ Failed`);
    }
  }
  
  // Save all processed documents to a single JSON file
  fs.writeFileSync(
    path.join(outputDir, 'documents.json'),
    JSON.stringify(processed, null, 2)
  );
  
  console.log(`\nProcessing complete:`);
  console.log(`✓ Success: ${successCount}`);
  console.log(`✗ Failed: ${failCount}`);
  console.log(`Saved to data/processed/documents.json`);
}

processAllPDFs();
