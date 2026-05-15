# Windows AutoCAD Runner (Phase 7)

This service runs on the engineer laptop (Windows + AutoCAD installed) and exposes:

- `POST /apply-plan`
- `GET /health`

## Run
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app:app --host 127.0.0.1 --port 8765
```

Set orchestrator mode:
```bash
set EDA_EXECUTOR_MODE=remote
set EDA_RUNNER_URL=http://127.0.0.1:8765
```

Enable real AutoCAD execution:
```bash
set EDA_AUTOCAD_REAL=1
```

## Real-mode behavior
- Uses `win32com.client.Dispatch("AutoCAD.Application")`
- Opens `drawing_path`
- Finds block references by `target_selector.block_name`
- Updates matching attribute tags from `parameters.attribute` to `parameters.value`
- Saves DWG and returns `updated_count`

## Notes
- Real mode requires AutoCAD COM and `pywin32`.
- Currently supports `update_attribute` action type.
