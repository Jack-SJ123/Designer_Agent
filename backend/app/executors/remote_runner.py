import os
from typing import Any

import httpx

from ..models import ActionPlan


class RemoteRunnerExecutor:
    """Calls a locally hosted Windows AutoCAD runner service."""

    def __init__(self) -> None:
        self.base_url = os.getenv("EDA_RUNNER_URL", "http://127.0.0.1:8765")
        self.timeout = float(os.getenv("EDA_RUNNER_TIMEOUT_SEC", "30"))

    def apply_plan(self, drawing_path: str, plan: ActionPlan) -> dict[str, Any]:
        payload = {"drawing_path": drawing_path, "plan": plan.model_dump(mode="json")}
        with httpx.Client(timeout=self.timeout) as client:
            resp = client.post(f"{self.base_url}/apply-plan", json=payload)
            resp.raise_for_status()
            return resp.json()
