from fastapi import FastAPI

from .models import ActionPlan, QaReport, TaskRequest

app = FastAPI(title="Electrical Designer Agent API", version="0.1.0")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/plan", response_model=ActionPlan)
def create_plan(task: TaskRequest) -> ActionPlan:
    # v1 placeholder: deterministic stub to demonstrate contract shape.
    return ActionPlan(
        plan_id=f"plan-{task.task_id}",
        risk_level="medium",
        assumptions=["Drawing exists and is accessible by CAD worker."],
        required_approvals=["electrical_checker"],
        actions=[
            {
                "action_type": "update_attribute",
                "target_selector": {"block_name": "DEVICE_TAG"},
                "parameters": {"attribute": "TAG", "value": "AUTO-PLACEHOLDER"},
                "tolerance": None,
                "rollback_hint": "Restore previous attribute value from audit snapshot.",
            }
        ],
    )


@app.post("/qa", response_model=QaReport)
def run_qa() -> QaReport:
    return QaReport(
        ruleset_version="v1-draft",
        checks_run=["layer_compliance", "tag_completeness"],
        violations=[],
        status="pass",
    )
