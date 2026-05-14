from ..models import ActionPlan


class DryRunExecutor:
    def apply_plan(self, drawing_path: str, plan: ActionPlan) -> dict:
        return {
            "drawing_path": drawing_path,
            "applied_actions": len(plan.actions),
            "status": "dry_run",
            "engine": "dry-run",
        }
