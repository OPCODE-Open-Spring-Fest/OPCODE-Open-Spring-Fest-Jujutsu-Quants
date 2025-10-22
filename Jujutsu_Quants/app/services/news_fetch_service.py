import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from typing import List, Dict


def fetch_urls_to_articles(urls: List[str]) -> List[Dict]:
    articles: List[Dict] = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    for url in urls:
        try:
            resp = requests.get(url, headers=headers, timeout=15)
            resp.raise_for_status()
            soup = BeautifulSoup(resp.text, 'html.parser')

            title = None
            if soup.title and soup.title.string:
                title = soup.title.string.strip()
            if not title:
                og_title = soup.find('meta', property='og:title')
                if og_title and og_title.get('content'):
                    title = og_title['content'].strip()

            # Naive content extraction: concatenate paragraph texts
            paragraphs = [p.get_text(strip=True) for p in soup.find_all('p')]
            content = '\n'.join([p for p in paragraphs if p])

            netloc = urlparse(url).netloc
            source = netloc.replace('www.', '') if netloc else 'unknown'

            if content:
                articles.append({
                    'title': title or source,
                    'content': content[:5000],
                    'source': source,
                    'url': url
                })
        except Exception:
            # Skip URLs that fail to fetch/parse
            continue
    return articles
