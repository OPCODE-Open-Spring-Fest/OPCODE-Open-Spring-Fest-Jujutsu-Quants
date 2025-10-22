# OpenAI News Lab (Python-based Agentic AI)

A small, modular agent pipeline for market/news analysis. It fetches quotes (Alpha Vantage/FMP), scrapes articles from URLs, and runs simple agents for anomalies, summaries, diversity, breaking alerts, bias, sentiment, plus optional Q&A.

## Features
- Anomalies from price changes
- Summaries of articles
- Source diversity counts
- Breaking-news flagging
- Simple bias flags
- Heuristic sentiment
- Optional news Q&A

## Backend (FastAPI, Python)

### 1) Install
```bash
pip install -r requirements.txt
```

Set environment variables (PowerShell):
```powershell
$env:ALPHA_VANTAGE_API_KEY = "YOUR_KEY"   # optional, for live quotes
$env:FMP_API_KEY = "YOUR_KEY"             # optional
```

### 2) Run
```bash
uvicorn app.adk.main:app --host 0.0.0.0 --port 8000 --reload
```

Open docs: http://localhost:8000/docs

### 3) Endpoints

- Simple (no JSON body):
```
GET /api/v2/report/simple?symbols=AAPL,TSLA&urls=<url1>,<url2>&question=...
```

- JSON body:
```
POST /api/v2/report
Content-Type: application/json
{
  "symbols": ["AAPL", "TSLA"],          // optional; fetches live data if provided
  "market_data": [],                      // optional; manual data instead of symbols
  "news_articles": [],                    // optional; manual articles
  "news_urls": ["https://...", "https://..."],
  "question": "Any notable moves?"      // optional
}
```

### Response (shape)
```json
{
  "anomalies": [...],
  "summaries": [...],
  "diversity": {...},
  "breaking_alerts": [...],
  "bias": [...],
  "sentiment": [...],
  "qa": {...}
}
```

## Frontend (React)

```bash
cd frontend
npm install
set "REACT_APP_API_URL=http://localhost:8000" && npm start
```
The dev server runs at http://localhost:3000. If you need API calls, point them to http://localhost:8000.

### Troubleshooting
- Agentic AI note: The system orchestrates multiple Python agents (sentiment, anomaly, bias, QA). You may optionally use frameworks like LangChain/LlamaIndex/Google ADK behind config flags; default path remains dependency-light.
- API calls 404: ensure backend is running at http://localhost:8000.
- CORS errors: backend enables permissive CORS; restart if you changed config.
- Empty submission: backend returns 400 unless you provide at least one of `symbols`, `market_data`, `news_articles`, `news_urls`, or a `question`.

## Project Structure
- `app/adk/agents/*`: small, focused agents (low-comment, easy to scan)
- `app/adk/orchestrator.py`: runs the agent workflow
- `app/services/market_data_service.py`: quotes via Alpha Vantage / FMP / Yahoo scrape
- `app/services/news_fetch_service.py`: fetches article text from URLs
- `frontend/`: React app

## Notes
- If you pass `symbols`, live data is fetched using your env keys.
- If you pass `news_urls`, article HTML is fetched and parsed server-side.
- You can also pass manual `market_data` or `news_articles`.

## Contributing
- Add new agents in `app/adk/agents/`
- Export factories in `app/adk/agents/__init__.py`
- Wire into `process_news_workflow` in `app/adk/orchestrator.py`
