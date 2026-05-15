from dataclasses import dataclass
from typing import Any

import yaml

from ..models import ActionPlan


@dataclass
class ValidationResult:
    status: str
    violations: list[str]
    checks_run: list[str]


class RulesEngine:
    def __init__(self, config_path: str) -> None:
        self.config_path = config_path
        with open(config_path, "r", encoding="utf-8") as f:
            self.profile = yaml.safe_load(f)

    def validate_plan(self, plan: ActionPlan) -> ValidationResult:
        checks = ["allowed_actions", "required_approvals"]
        violations: list[str] = []

        allowed = set(self.profile.get("allowed_actions", []))
        for action in plan.actions:
            if action.action_type not in allowed:
                violations.append(f"Action '{action.action_type}' is not allowed")

        required_approvals = set(self.profile.get("required_approvals", []))
        missing = required_approvals.difference(set(plan.required_approvals))
        if missing:
            violations.append(f"Missing required approvals in plan: {sorted(missing)}")

        return ValidationResult(
            status="pass" if not violations else "fail",
            violations=violations,
            checks_run=checks,
        )


def validation_to_dict(result: ValidationResult) -> dict[str, Any]:
    return {
        "status": result.status,
        "violations": result.violations,
        "checks_run": result.checks_run,
    }
