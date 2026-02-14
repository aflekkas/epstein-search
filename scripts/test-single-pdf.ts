import * as fs from 'fs';
import * as path from 'path';
import * as pdfjsLib from 'pdfjs-dist/legacy/build/pdf.mjs';

async function testSinglePDF() {
  const pdfPath = '/data/.openclaw/workspace/epstein-search/data/pdfs/dataset-1/EFTA00000001.pdf';
  
  try {
    console.log('Reading PDF...');
    const dataBuffer = fs.readFileSync(pdfPath);
    const uint8Array = new Uint8Array(dataBuffer);
    
    console.log('Loading PDF document...');
    const loadingTask = pdfjsLib.getDocument({ data: uint8Array });
    const pdf = await loadingTask.promise;
    
    console.log(`PDF loaded. Pages: ${pdf.numPages}`);
    
    let fullText = '';
    
    for (let i = 1; i <= pdf.numPages; i++) {
      console.log(`Processing page ${i}...`);
      const page = await pdf.getPage(i);
      const textContent = await page.getTextContent();
      const pageText = textContent.items.map((item: any) => item.str).join(' ');
      fullText += pageText + '\n\n';
    }
    
    console.log(`\nExtracted text length: ${fullText.length} chars`);
    console.log('\nFirst 500 characters:');
    console.log(fullText.substring(0, 500));
    
  } catch (error) {
    console.error('Error:', error);
  }
}

testSinglePDF();
