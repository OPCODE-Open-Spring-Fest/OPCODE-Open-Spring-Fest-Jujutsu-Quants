# Jujutsu-Quants: Safe Folder Rename Plan

Goal: Rebrand repository folder and references from current name to `jujutsu-quants` without breaking imports.

## Option A (recommended): Keep code imports stable, rename only the top-level folder

This keeps Python import roots the same (e.g., `app.*`) and avoids mass refactors.

1) Close running dev servers.
2) From the parent directory of the repo, rename the folder:
```bash
# PowerShell
Rename-Item -Path .\ml_opensource -NewName jujutsu-quants

# or Git (preserves history better when moving contents into a new folder):
# cd ..
# git mv ml_opensource jujutsu-quants
```
3) Update docs/badges/links that reference the old folder name (done in contributor guide).
4) Verify dev:
```bash
cd jujutsu-quants\tradesage-mvp
uvicorn app.adk.main:app --reload
```

## Option B: Rename inner app root and refactor imports (advanced)

Only do this if you want code-level package rename. This requires large import changes.

High-level steps:
- Decide new Python package root (e.g., `jq_app` instead of `app`).
- Move directory `tradesage-mvp/app` -> `tradesage-mvp/jq_app`.
- Replace imports: `from app.` -> `from jq_app.` across backend code.
- Update ASGI entry: `uvicorn jq_app.adk.main:app`.
- Run test suite and fix remaining import errors.

Suggested scripted refactor (preview first):
```bash
# Example (run from repo root). Review diffs before committing.
Get-ChildItem -Recurse -Include *.py | ForEach-Object {
  (Get-Content $_.FullName) -replace '\bfrom app\.', 'from jq_app.' -replace '\bimport app\.', 'import jq_app.' | Set-Content $_.FullName
}
```

## Post-rename checks

- Start backend: `uvicorn app.adk.main:app --reload` (Option A) or `uvicorn jq_app.adk.main:app --reload` (Option B)
- Open API docs: http://localhost:8000/docs
- Run basic smoke call:
```bash
curl "http://localhost:8000/api/v2/report/simple?symbols=AAPL&urls=https://example.com"
```
- Frontend still builds and points to backend (if used).

## Notes
- We already rebranded docs to Jujutsu-Quants and simplified beginner issues (#1, #3).
- Prefer Option A for the event to reduce risk; Option B can be a later tracked task.
