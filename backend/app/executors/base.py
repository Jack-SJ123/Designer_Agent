from typing import Protocol

from ..models import ActionPlan


class Executor(Protocol):
    def apply_plan(self, drawing_path: str, plan: ActionPlan) -> dict:
        ...
