# Electrical Designer Agent (Phase 1)

Phase 1 implements a persistent task lifecycle with approval gating and dry-run execution.

## Implemented
- Task creation and retrieval
- Plan generation and persistence
- Approval gate enforcement
- Execution endpoint with dry-run CAD executor
- Structured QA response and final task status update

## API endpoints
- `GET /health`
- `POST /tasks`
- `GET /tasks/{task_id}`
- `POST /tasks/{task_id}/plan`
- `POST /tasks/{task_id}/approve`
- `POST /tasks/{task_id}/execute`
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

## Test
```bash
pytest backend/tests -q
```
## Next steps
1. Implement task persistence and job queue.
2. Add AutoCAD executor integration (local laptop runner).
3. Add approval UI and auth.
