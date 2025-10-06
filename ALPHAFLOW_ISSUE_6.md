# Mission: Forge the Domain Expansion (Hard • 8 pts)

Design a new summarizer agent that fuses retrieval-ranked passages, market movement signals, and bias flags into a structured, cited summary.

## Goals
- Build `hybrid_rag_summarizer` agent:
  - Ingest: `market_data[]`, `news_articles[]`
  - Retrieve and rank passages (reuse ranking from Issue 5 if available)
  - Compute price deltas per symbol and classify move regimes (flat/up/down)
  - Integrate bias flags as uncertainty sources
  - Output structured JSON: `{ summary, key_points[], uncertainty_factors[], citations[] }`

## Where
- New agent file: `Jujutsu-Quants/app/adk/agents/hybrid_rag_summarizer.py`
- Wire into orchestrator optional stage (behind a flag in `ADK_CONFIG`)

## Minimal Reproducible Example (MRE)
```bash
uvicorn Jujutsu-Quants.app.adk.main:app --reload
curl -s -X POST http://localhost:8000/api/v2/report -H "Content-Type: application/json" -d '{
  "symbols": ["AAPL"],
  "news_urls": ["https://example.com/news1"],
  "question": "What are key drivers today?"
}' | jq
```
Expected top-level include key `rag_summary`:
```json
{
  "rag_summary": {
    "summary": "Apple rose modestly; supply chain easing ...",
    "key_points": ["iPhone demand", "China recovery"],
    "uncertainty_factors": ["single-source report", "political risk"],
    "citations": [{"source": "https://example.com/news1", "start": 120, "end": 220}]
  }
}
```

## Acceptance Criteria
- New agent produces deterministic structure and integrates three signals (price regime, ranked passages, bias flags)
- Orchestrator can include/exclude via config
- Unit tests for passage fusion and regime classification
- Docs updated (README agents section) with a short usage note
