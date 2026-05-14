import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


def write_artifact(task_id: str, name: str, payload: dict[str, Any]) -> str:
    root = Path("backend/data/artifacts") / task_id
    root.mkdir(parents=True, exist_ok=True)
    stamped = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    path = root / f"{stamped}_{name}.json"
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return str(path)
