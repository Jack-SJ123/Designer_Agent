from ..models import ActionPlan


class AutoCADExecutor:
    """Phase 2A placeholder for local AutoCAD COM/.NET integration."""

    def apply_plan(self, drawing_path: str, plan: ActionPlan) -> dict:
        # TODO: Replace with real COM/.NET integration on engineer laptop.
        return {
            "drawing_path": drawing_path,
            "applied_actions": len(plan.actions),
            "status": "simulated_autocad",
            "engine": "autocad-placeholder",
        }
