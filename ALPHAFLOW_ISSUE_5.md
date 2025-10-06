# Mission: Rank the Spirit Fragments (Medium • 4 pts)

The current `news_qa_agent.py` answers from raw concatenated text. Improve grounding by ranking passages and returning citations.

## Goals
- Chunk input articles into passages (e.g., 120–200 tokens)
- Rank passages by BM25+ or cosine similarity (tiny embeddings ok)
- Compose answer from top-K passages
- Return citations: article source + passage span indices

## Scope
- Pure-Python implementation; no heavy dependencies required
- Keep API: `answer(news_articles, question)` returning `{ answer, citations[] }`

## Where
- File: `Jujutsu-Quants/app/adk/agents/news_qa_agent.py`

## Minimal Reproducible Example (MRE)
```bash
uvicorn Jujutsu-Quants.app.adk.main:app --reload
curl -s "http://localhost:8000/api/v2/report/simple?question=What%20did%20TSLA%20announce%3F&urls=https://example.com/news1,https://example.com/news2" | jq
```
Expected: `qa.answer` summarizes from ranked passages and includes `qa.citations` like:
```json
{
  "qa": {
    "answer": "Tesla announced ...",
    "citations": [
      {"source": "https://example.com/news1", "start": 350, "end": 520},
      {"source": "https://example.com/news2", "start": 40, "end": 110}
    ]
  }
}
```

## Acceptance Criteria
- Deterministic chunking and ranking function with tests
- Answer includes at least one citation when sources exist
- Graceful fallback when no articles are provided
- README snippet added in agent section describing behavior
