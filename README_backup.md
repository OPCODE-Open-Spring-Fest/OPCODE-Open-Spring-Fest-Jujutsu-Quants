# Jujutsu-Quants: Exorcising Cursed Markets (with Python)

Imagine the market as a city full of cursed spirits: sudden price spikes, rumor chains, biased headlines, and noisy signals. Jujutsu-Quants is your dojo. Each agent is a sorcerer with a specialty — one senses anomalies, another reads the news, another questions the sources, another checks bias, and so on. The orchestrator leads the squad so your hypothesis doesn’t walk in alone.

You bring a trading hypothesis. The squad brings evidence, contradictions, and confidence. Together, you exorcise bad ideas — and level up the good ones.

## What you get (Python-based)
- Live quotes via Alpha Vantage / FMP (with env keys), Yahoo Finance scrape fallback
- Article fetching from URLs (server-side parsing)
- Agents: anomalies, summaries, diversity, breaking alerts, bias, sentiment, Q&A
- REST API (FastAPI) + React frontend

## Quickstart: train, then fight

### Backend
1) Install
```bash
pip install -r Jujutsu-Quants/requirements.txt
```

2) (Optional) API keys
```powershell
$env:ALPHA_VANTAGE_API_KEY = "YOUR_KEY"
$env:FMP_API_KEY = "YOUR_KEY"
```

3) Run
```bash
uvicorn Jujutsu-Quants.app.adk.main:app --host 0.0.0.0 --port 8000 --reload
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
cd Jujutsu-Quants/frontend
npm install
set "REACT_APP_API_URL=http://localhost:8000" && npm start
```
Frontend: http://localhost:3000 (ensure `REACT_APP_API_URL` is set to http://localhost:8000)

## Dojo layout
- `Jujutsu-Quants/app/adk/agents/` – small agents
- `Jujutsu-Quants/app/adk/orchestrator.py` – runs the workflow
- `Jujutsu-Quants/app/services/` – market data + article fetch
- `Jujutsu-Quants/frontend/` – React app

## Notes
- Set `PROJECT_ID=letsstock-with-ai` if needed by any service/tooling.
- Works offline with manual `market_data`/`news_articles`, or online with `symbols` and `news_urls`.

## When a curse fights back (troubleshooting)

- Backend responds but dashboard is empty: confirm frontend uses `REACT_APP_API_URL=http://localhost:8000`.
- CORS issues: backend enables `allow_origins=["*"]`; restart backend if changed.
- Empty submission rejected: backend returns 400 if you send no `symbols`, `market_data`, `news_articles`, `news_urls`, or `question`.

## Minimal Reproducible Example (MRE)
## Optional techniques (use when needed)

- **LangChain**: add retrievers/tools within agents without changing the public API.
- **LlamaIndex**: build indexes/graphs for news corpora; call from agents.
- **Google ADK**: enable cloud agent runtime by setting `ADK_MODE=1` and installing ADK deps; the orchestrator auto-switches.

These are optional; default code runs with plain Python for easy local development.

Provide in issues:
- Exact backend request (curl) to `/api/v2/report` or `/api/v2/report/simple`
- Backend logs snippet
- Frontend console error
- Expected vs actual result
