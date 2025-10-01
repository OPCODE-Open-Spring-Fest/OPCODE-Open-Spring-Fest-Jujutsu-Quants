# letsstock-with-ai

Lightweight market + news analysis pipeline with pluggable agents. Fetch live quotes, pull article text from URLs, and generate a combined report with anomalies, summaries, diversity, breaking alerts, bias, sentiment, and optional Q&A.

## Features
- Live quotes via Alpha Vantage / FMP (with env keys), Yahoo Finance scrape fallback
- Article fetching from URLs (server-side parsing)
- Agents: anomalies, summaries, diversity, breaking alerts, bias, sentiment, Q&A
- REST API (FastAPI) + React frontend

## Quickstart

### Backend
1) Install
```bash
pip install -r tradesage-mvp/requirements.txt
```

2) (Optional) API keys
```powershell
$env:ALPHA_VANTAGE_API_KEY = "YOUR_KEY"
$env:FMP_API_KEY = "YOUR_KEY"
```

3) Run
```bash
uvicorn tradesage-mvp.app.adk.main:app --host 0.0.0.0 --port 8000 --reload
```
Open docs: http://localhost:8000/docs

Endpoints:
- Simple (no JSON):
```
GET /api/v2/report/simple?symbols=AAPL,TSLA&urls=<url1>,<url2>&question=...
```
- JSON body:
```
POST /api/v2/report
{
  "symbols": ["AAPL", "TSLA"],
  "market_data": [],
  "news_articles": [],
  "news_urls": ["https://...", "https://..."],
  "question": "Any notable moves?"
}
```

### Frontend
```bash
cd tradesage-mvp/frontend
npm install
npm start
```
Frontend: http://localhost:3000 (configure API base as http://localhost:8000)

## Project layout
- `tradesage-mvp/app/adk/agents/` – small agents
- `tradesage-mvp/app/adk/orchestrator.py` – runs the workflow
- `tradesage-mvp/app/services/` – market data + article fetch
- `tradesage-mvp/frontend/` – React app

## Notes
- Set `PROJECT_ID=letsstock-with-ai` if needed by any service/tooling.
- Works offline with manual `market_data`/`news_articles`, or online with `symbols` and `news_urls`.
