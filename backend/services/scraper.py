import requests
from bs4 import BeautifulSoup
import re

def clean_text(text):
    # Remove references like [1], [2], etc.
    text = re.sub(r'\[\d+\]', '', text)
    # Remove [edit]
    text = re.sub(r'\[edit\]', '', text)
    # Remove multiple spaces and newlines
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def scrape_wikipedia(url: str):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Title
        title = soup.find(id="firstHeading").text
        
        # Content
        content_div = soup.find(id="bodyContent")
        
        # Extract Summary (paragraphs before the first heading)
        summary_paragraphs = []
        for element in content_div.find_all(['p', 'h2'], recursive=False):
            if element.name == 'h2':
                break
            if element.name == 'p':
                summary_paragraphs.append(element.text)
                
        summary = clean_text(" ".join(summary_paragraphs))
        
        # Extract Sections and Full Text
        sections = []
        full_text = ""
        current_section = "Summary"
        
        # Get all text for LLM processing
        # We'll simple extract all paragraphs and headings to form the full context
        for element in content_div.find_all(['p', 'h2', 'h3']):
            text = clean_text(element.text)
            if not text:
                continue
                
            if element.name in ['h2', 'h3']:
                # Skip Contents, References, External links, See also
                if text in ['Contents', 'References', 'External links', 'See also', 'Notes', 'Further reading']:
                    continue
                current_section = text
                sections.append(text)
                full_text += f"\n\n## {text}\n\n"
            else:
                full_text += f"{text} "
        
        # Limit full text length to avoid token limits (approx 20k chars)
        if len(full_text) > 6000:
             full_text = full_text[:6000] + "... (truncated)"
                
        # Limit summary length if too long
        if len(summary) > 1000:
            summary = summary[:1000] + "..."
            
        return {
            "title": title,
            "summary": summary,
            "sections": list(set(sections)), # Unique sections
            "text": full_text
        }
        
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        raise Exception(f"Failed to scrape URL: {str(e)}")
