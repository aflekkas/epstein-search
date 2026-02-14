import axios from 'axios';
import * as cheerio from 'cheerio';
import * as fs from 'fs';
import * as path from 'path';

interface DocumentLink {
  id: string;
  url: string;
  dataset: number;
  filename: string;
}

async function scrapeDataset(datasetNum: number): Promise<DocumentLink[]> {
  const url = `https://www.justice.gov/epstein/doj-disclosures/data-set-${datasetNum}-files`;
  console.log(`Scraping dataset ${datasetNum}...`);
  
  try {
    const response = await axios.get(url);
    const $ = cheerio.load(response.data);
    const links: DocumentLink[] = [];
    
    // Find all PDF links
    $('a[href*=".pdf"]').each((_, element) => {
      const href = $(element).attr('href');
      if (href) {
        const fullUrl = href.startsWith('http') ? href : `https://www.justice.gov${href}`;
        const filename = path.basename(href);
        const id = filename.replace('.pdf', '');
        
        links.push({
          id,
          url: fullUrl,
          dataset: datasetNum,
          filename
        });
      }
    });
    
    console.log(`Found ${links.length} documents in dataset ${datasetNum}`);
    return links;
  } catch (error) {
    console.error(`Error scraping dataset ${datasetNum}:`, error);
    return [];
  }
}

async function scrapeAllDatasets() {
  const allLinks: DocumentLink[] = [];
  
  // Start with datasets 1-12 (as shown on the site)
  for (let i = 1; i <= 12; i++) {
    const links = await scrapeDataset(i);
    allLinks.push(...links);
    
    // Be nice to the server
    await new Promise(resolve => setTimeout(resolve, 1000));
  }
  
  // Save to file
  const dataDir = path.join(process.cwd(), 'data');
  if (!fs.existsSync(dataDir)) {
    fs.mkdirSync(dataDir, { recursive: true });
  }
  
  fs.writeFileSync(
    path.join(dataDir, 'document-links.json'),
    JSON.stringify(allLinks, null, 2)
  );
  
  console.log(`\nTotal documents found: ${allLinks.length}`);
  console.log(`Saved to data/document-links.json`);
}

scrapeAllDatasets();
