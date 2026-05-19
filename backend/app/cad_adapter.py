from typing import Protocol

from .models import ActionPlan


class CadExecutor(Protocol):
    def apply_plan(self, drawing_path: str, plan: ActionPlan) -> dict:
        """Apply an approved action plan to a drawing and return execution metadata."""


class DryRunCadExecutor:
    def apply_plan(self, drawing_path: str, plan: ActionPlan) -> dict:
        return {
            "drawing_path": drawing_path,
            "applied_actions": len(plan.actions),
            "status": "dry_run",
        }
