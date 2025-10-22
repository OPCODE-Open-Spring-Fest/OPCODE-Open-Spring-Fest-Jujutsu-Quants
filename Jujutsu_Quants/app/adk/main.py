
from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import os

from app.adk.orchestrator import Orchestrator
from app.services.market_data_service import MarketDataService
from app.services.news_fetch_service import fetch_urls_to_articles

app = FastAPI(title="OpenAI News Lab", version="2.0.0")
orchestrator = Orchestrator()
market_service = MarketDataService()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ReportRequest(BaseModel):
    symbols: Optional[List[str]] = None
    market_data: Optional[List[Dict[str, Any]]] = None
    news_articles: Optional[List[Dict[str, Any]]] = None
    news_urls: Optional[List[str]] = None
    question: Optional[str] = None

@app.get("/")
async def root():
    return {"message": "OpenAI News Lab - Agent Orchestrator"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "openai-news-lab", "version": "2.0.0"}

@app.get("/api/v2/report/simple")
async def get_simple_report(
    symbols: Optional[str] = Query(default=None, description="Comma-separated symbols, e.g., AAPL,TSLA"),
    urls: Optional[str] = Query(default=None, description="Comma-separated news URLs"),
    question: Optional[str] = Query(default=None, description="Optional question for QA")
):
    # Parse symbols and urls
    symbol_list: List[str] = []
    url_list: List[str] = []
    if symbols:
        symbol_list = [s.strip() for s in symbols.split(',') if s.strip()]
    if urls:
        url_list = [u.strip() for u in urls.split(',') if u.strip()]

    # Resolve market data
    resolved_market_data: List[Dict[str, Any]] = []
    if symbol_list:
        quotes = market_service.get_multiple_quotes(symbol_list)
        for sym, quote in quotes.items():
            if quote and quote.get('status') == 'success':
                info = quote['data']['info']
                price = info.get('currentPrice', 0)
                prev = info.get('previousClose', price)
                change = price - prev
                change_pct = (change / prev) if prev else 0
                resolved_market_data.append({
                    'symbol': sym,
                    'price_change': round(change_pct, 4)
                })
            else:
                resolved_market_data.append({
                    'symbol': sym,
                    'price_change': 0.0,
                    'error': quote.get('error', 'fetch_failed') if isinstance(quote, dict) else 'fetch_failed'
                })

    # Resolve articles
    resolved_articles: List[Dict[str, Any]] = []
    if url_list:
        resolved_articles = fetch_urls_to_articles(url_list)

    return await orchestrator.process_news_workflow(
        resolved_market_data,
        resolved_articles,
        question,
    )

@app.post("/api/v2/report")
async def get_advanced_report(payload: ReportRequest):
    """
    Run all advanced agents and return their results.
    - If symbols provided, fetch live market data using env API keys.
    - Else, use market_data passed in the request.
    - If news_urls provided, fetch and parse content to articles.
    """
    # Basic validation: require at least one input signal
    if not ((payload.symbols and len(payload.symbols) > 0) or
            (payload.market_data and len(payload.market_data) > 0) or
            (payload.news_articles and len(payload.news_articles) > 0) or
            (payload.news_urls and len(payload.news_urls) > 0) or
            (payload.question and payload.question.strip())):
        raise HTTPException(status_code=400, detail="Empty request: provide symbols, market_data, news_articles, news_urls, or question")

    # Resolve market data
    resolved_market_data: List[Dict[str, Any]] = []
    if payload.symbols and len(payload.symbols) > 0:
        quotes = market_service.get_multiple_quotes(payload.symbols)
        for sym, quote in quotes.items():
            if quote and quote.get('status') == 'success':
                info = quote['data']['info']
                price = info.get('currentPrice', 0)
                prev = info.get('previousClose', price)
                change = price - prev
                change_pct = (change / prev) if prev else 0
                resolved_market_data.append({
                    'symbol': sym,
                    'price_change': round(change_pct, 4)
                })
            else:
                resolved_market_data.append({
                    'symbol': sym,
                    'price_change': 0.0,
                    'error': quote.get('error', 'fetch_failed') if isinstance(quote, dict) else 'fetch_failed'
                })
    else:
        resolved_market_data = payload.market_data or []

    # Resolve news articles
    resolved_articles: List[Dict[str, Any]] = payload.news_articles or []
    if payload.news_urls and len(payload.news_urls) > 0:
        fetched = fetch_urls_to_articles(payload.news_urls)
        resolved_articles = fetched + resolved_articles

    return await orchestrator.process_news_workflow(
        resolved_market_data,
        resolved_articles,
        payload.question,
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
