# Electrical Designer Agent (v1 Scaffold)

This repository contains a starter architecture for an AI-assisted Electrical Designer agent focused on AutoCAD drawing updates with human approval gates.

## Scope (v1)
- API-first orchestrator scaffold
- JSON schemas for action planning and QA
- Rule profile examples
- CAD adapter interface stubs

## Run (local)
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
uvicorn app.main:app --app-dir backend --reload
```

## Next steps
1. Implement task persistence and job queue.
2. Add AutoCAD executor integration (local laptop runner).
3. Add approval UI and auth.
