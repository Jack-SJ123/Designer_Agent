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
