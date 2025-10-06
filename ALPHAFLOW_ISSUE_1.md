# Mission: Unmask the Cursed Bias (Easy • 2 pts)

## Minimal Reproducible Example (MRE)

1) Backend running:
```bash
uvicorn Jujutsu-Quants.app.adk.main:app --reload
```
2) Send sample request:
```bash
curl -s -X POST http://localhost:8000/api/v2/report -H "Content-Type: application/json" -d '{"question":"Test Tesla hypothesis"}' | jq
```
3) Expected: response JSON contains `bias` list. Current bug: entities are hardcoded; update detector to accept list via config or request.

## Acceptance Criteria
- Add config-driven or request-driven entity list.
- Update tests and README with configuration example.

## Task
Make `BiasDetector` usable by removing hardcoded `TARGET_ENTITIES` and allowing entities from:
- config (`AGENT_CONFIGS['bias_detector']['entities']`, optional)
- request-time input (method argument)
- fallback to simple title keywords

## What to Implement (small scope)
- Add optional parameter `entities: List[str] | None` to `detect(articles, entities=None)`.
- If `entities` is None, read from config; if still empty, derive from titles by picking capitalized tokens.
- Keep existing proximity logic unchanged.

## I/O
- Input: `articles: List[Dict{title:str, content:str}]`, optional `entities: List[str]`.
- Output: existing bias result list (unchanged schema).

## Example
```python
articles = [{
  'title': 'Apple beats expectations',
  'content': 'Analysts say Apple showed unprecedented growth.'
}]

det = create_bias_detector()
out = det.detect(articles, entities=['Apple'])
# out[0]['entity_focus'] == 'apple'
```

## Acceptance Criteria
- Hardcoded list removed; method accepts optional `entities`.
- If no entities provided, detector derives at least one from titles.
- Existing output shape unchanged; tests pass on simple sample above.

## Hints
- To derive entities quickly: `re.findall(r"\b[A-Z][a-zA-Z]{2,}\b", title)` and lowercase them.

## Labels
`good first issue`, `agents`, `bias`
