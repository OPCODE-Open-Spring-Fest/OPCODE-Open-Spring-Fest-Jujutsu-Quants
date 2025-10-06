---
name: MRE Bug Report
about: Create a minimal, reproducible example for a bug
title: "bug: <brief title>"
labels: bug, needs-triage
assignees: ''
---

### Summary
Describe the bug in one or two sentences.

### Minimal Reproducible Example

Backend request (curl):
```bash
curl -s -X POST http://localhost:8000/api/v2/report -H "Content-Type: application/json" -d '{
  "question": "<your question>",
  "symbols": [],
  "news_urls": []
}' | jq
```

Backend version and logs (tail):
```
<paste logs>
```

Frontend console/network error:
```
<paste snippet>
```

### Expected vs Actual
- Expected:
- Actual:

### Environment
- OS:
- Python/Node versions:
- Backend start command:

### Additional context
Any other details.


