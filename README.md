# Electrical Designer Agent (Phase 3-6)

This build advances toward real AutoCAD demo readiness.

## Highlights
- Configurable execution backends: `dry_run`, `autocad`, `remote`
- Remote runner executor contract for local Windows AutoCAD service
- Artifact persistence for plan/QA/execution logs
- Idempotent execute requests via `idempotency_key`
- Demo endpoint to run an end-to-end scenario

## API endpoints
- `GET /health`
- `GET /config/executor`
- `POST /tasks`
- `GET /tasks/{task_id}`
- `POST /tasks/{task_id}/plan`
- `POST /tasks/{task_id}/validate`
- `POST /tasks/{task_id}/approve`
- `POST /tasks/{task_id}/execute` (requires `idempotency_key`)
- `POST /demo/run`

## Runner modes
- default: `dry_run`
- `EDA_EXECUTOR_MODE=autocad`
- `EDA_EXECUTOR_MODE=remote` with `EDA_RUNNER_URL` (default `http://127.0.0.1:8765`)

## Test
```bash
pytest backend/tests -q
```


## Windows runner
See `runner_autocad/` for the local AutoCAD runner service and startup instructions.
