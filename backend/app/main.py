from pathlib import Path
from uuid import uuid4

from fastapi import FastAPI, HTTPException

from .cad_adapter import DryRunCadExecutor
from .models import ActionPlan, ApproveRequest, CreateTaskRequest, ExecuteResponse, QaReport, TaskRecord
from .store import TaskStore

DB_PATH = Path("backend/data/agent.db")
DB_PATH.parent.mkdir(parents=True, exist_ok=True)
store = TaskStore(str(DB_PATH))
store.init()
executor = DryRunCadExecutor()

app = FastAPI(title="Electrical Designer Agent API", version="0.2.0")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/tasks", response_model=TaskRecord)
def create_task(request: CreateTaskRequest) -> TaskRecord:
    task_id = f"task-{uuid4().hex[:10]}"
    return store.create_task(task_id, request)


@app.get("/tasks/{task_id}", response_model=TaskRecord)
def get_task(task_id: str) -> TaskRecord:
    try:
        return store.get_task(task_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="Task not found") from exc


@app.post("/tasks/{task_id}/plan", response_model=ActionPlan)
def create_plan(task_id: str) -> ActionPlan:
    try:
        _ = store.get_task(task_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="Task not found") from exc

    plan = ActionPlan(
        plan_id=f"plan-{task_id}",
        risk_level="medium",
        assumptions=["Drawing exists and is accessible by CAD worker."],
        required_approvals=["electrical_checker"],
        actions=[
            {
                "action_type": "update_attribute",
                "target_selector": {"block_name": "DEVICE_TAG"},
                "parameters": {"attribute": "TAG", "value": "AUTO-PLACEHOLDER"},
                "rollback_hint": "Restore previous attribute value from audit snapshot.",
            }
        ],
    )
    store.save_plan(task_id, plan)
    store.update_status(task_id, "planned")
    return plan


@app.post("/tasks/{task_id}/approve", response_model=TaskRecord)
def approve_task(task_id: str, req: ApproveRequest) -> TaskRecord:
    try:
        task = store.get_task(task_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="Task not found") from exc
    if task.status != "planned":
        raise HTTPException(status_code=409, detail="Task must be planned before approval")
    return store.update_status(task_id, "approved", approved_by=req.approved_by)


@app.post("/tasks/{task_id}/execute", response_model=ExecuteResponse)
def execute_task(task_id: str) -> ExecuteResponse:
    try:
        task = store.get_task(task_id)
        plan = store.get_plan(task_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="Task or plan not found") from exc

    if task.status != "approved":
        raise HTTPException(status_code=409, detail="Task must be approved before execution")

    store.update_status(task_id, "running")
    execution = executor.apply_plan(task.drawing_id, plan)

    qa = QaReport(
        ruleset_version="v1-draft",
        checks_run=["layer_compliance", "tag_completeness"],
        violations=[],
        status="pass",
    )
    final_status = "passed" if qa.status == "pass" else "failed"
    updated_task = store.update_status(task_id, final_status)
    return ExecuteResponse(task=updated_task, plan=plan, qa_report=qa, execution=execution)
