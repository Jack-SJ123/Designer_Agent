# Electrical Designer Agent (Phases 1–7)

This repository contains an AI-assisted Electrical Designer workflow that orchestrates plan/validate/approve/execute operations and can route execution to a local Windows AutoCAD runner.

## Phase Summary

### Phase 1 — Task lifecycle foundation
- Persistent task records in SQLite
- Core endpoints for create/get/plan/approve/execute
- Safe dry-run execution flow

### Phase 2A — Rules validation + executor structure
- Rules engine with YAML standards profile
- `POST /tasks/{task_id}/validate`
- Executor plugin structure introduced

### Phase 2B — Configurable execution mode
- Executor mode via `EDA_EXECUTOR_MODE`
- Stable dry-run default for safety
- Runtime executor introspection endpoint

### Phases 3–6 — Demo-readiness hardening
- Remote runner mode (`EDA_EXECUTOR_MODE=remote`)
- Idempotent execute requests (`idempotency_key`)
- Artifact persistence for plan/QA/execution
- Demo endpoint `POST /demo/run`

### Phase 7 — Windows AutoCAD real-mode runner
- `runner_autocad/` service with `/apply-plan`
- Real COM integration path using `pywin32`
- Real-mode toggle: `EDA_AUTOCAD_REAL=1`

---

## Repository Layout
- `backend/` — orchestrator API, models, store, rules, schemas, tests
- `runner_autocad/` — Windows-side runner service for real AutoCAD calls
- `docs/` — architecture notes

---

## API Endpoints (Orchestrator)
- `GET /health`
- `GET /config/executor`
- `POST /tasks`
- `GET /tasks/{task_id}`
- `POST /tasks/{task_id}/plan`
- `POST /tasks/{task_id}/validate`
- `POST /tasks/{task_id}/approve`
- `POST /tasks/{task_id}/execute` (requires JSON body with `idempotency_key`)
- `POST /demo/run`

---

## Environment Variables

### Orchestrator (`backend/app`)
- `EDA_EXECUTOR_MODE`:
  - `dry_run` (default)
  - `autocad` (placeholder local executor)
  - `remote` (calls Windows runner service)
- `EDA_RUNNER_URL` (used in `remote` mode)
  - default: `http://127.0.0.1:8765`

### Windows Runner (`runner_autocad`)
- `EDA_AUTOCAD_REAL=1` enables real COM execution
- unset or `0` uses simulated execution

---

## Setup

### 1) Start Windows AutoCAD Runner (on your laptop)
Open **Command Prompt** in `runner_autocad/`:

```bat
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
set EDA_AUTOCAD_REAL=1
uvicorn app:app --host 127.0.0.1 --port 8765
```

Health check:
```bat
curl http://127.0.0.1:8765/health
```

### 2) Start Orchestrator API
Open another terminal in repo root:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
export EDA_EXECUTOR_MODE=remote
export EDA_RUNNER_URL=http://127.0.0.1:8765
uvicorn app.main:app --app-dir backend --host 127.0.0.1 --port 8000
```

Health check:
```bash
curl http://127.0.0.1:8000/health
curl http://127.0.0.1:8000/config/executor
```

---

## Live Demo Runbook

### Option A — One-call demo
```bash
curl -X POST http://127.0.0.1:8000/demo/run
```

### Option B — Step-by-step (recommended for presentation)
1. Create task:
```bash
curl -X POST http://127.0.0.1:8000/tasks \
  -H 'Content-Type: application/json' \
  -d '{
    "project_id":"demo-project",
    "drawing_id":"C:/demo/SLD-001.dwg",
    "requested_change":"Update device tag",
    "source_docs":["demo.csv"],
    "requester":"demo-user"
  }'
```
2. Plan: `POST /tasks/{task_id}/plan`
3. Validate: `POST /tasks/{task_id}/validate`
4. Approve: `POST /tasks/{task_id}/approve` with `{"approved_by":"checker"}`
5. Execute: `POST /tasks/{task_id}/execute` with `{"idempotency_key":"demo-001"}`

---

## Tests
```bash
pytest backend/tests -q
```

---

## Notes
- The runner currently supports the `update_attribute` action type in real mode.
- Artifact files are written under `backend/data/artifacts/{task_id}`.
