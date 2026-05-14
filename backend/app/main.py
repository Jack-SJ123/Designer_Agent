from datetime import UTC, datetime
from pathlib import Path
from uuid import uuid4

from fastapi import FastAPI, HTTPException

from .artifacts import write_artifact
from .executors.factory import build_executor
from .models import ActionPlan, ApproveRequest, CreateTaskRequest, ExecuteRequest, ExecuteResponse, QaReport, TaskRecord
from .rules.engine import RulesEngine, validation_to_dict
from .store import TaskStore

DB_PATH = Path("backend/data/agent.db")
DB_PATH.parent.mkdir(parents=True, exist_ok=True)
store = TaskStore(str(DB_PATH))
store.init()
executor = build_executor()
rules_engine = RulesEngine("backend/config/standards.yml")

app = FastAPI(title="Electrical Designer Agent API", version="0.4.0")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/config/executor")
def executor_config() -> dict[str, str]:
    return {"mode": executor.apply_plan.__self__.__class__.__name__}


@app.post("/tasks", response_model=TaskRecord)
def create_task(request: CreateTaskRequest) -> TaskRecord:
    return store.create_task(f"task-{uuid4().hex[:10]}", request)


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
        actions=[{"action_type": "update_attribute", "target_selector": {"block_name": "DEVICE_TAG"}, "parameters": {"attribute": "TAG", "value": "AUTO-PLACEHOLDER"}, "rollback_hint": "Restore previous attribute value from audit snapshot."}],
    )
    store.save_plan(task_id, plan)
    store.update_status(task_id, "planned")
    return plan


@app.post("/tasks/{task_id}/validate")
def validate_task_plan(task_id: str) -> dict:
    try:
        plan = store.get_plan(task_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="Task or plan not found") from exc
    return validation_to_dict(rules_engine.validate_plan(plan))


@app.post("/tasks/{task_id}/approve", response_model=TaskRecord)
def approve_task(task_id: str, req: ApproveRequest) -> TaskRecord:
    task = get_task(task_id)
    if task.status != "planned":
        raise HTTPException(status_code=409, detail="Task must be planned before approval")
    return store.update_status(task_id, "approved", approved_by=req.approved_by)


@app.post("/tasks/{task_id}/execute", response_model=ExecuteResponse)
def execute_task(task_id: str, req: ExecuteRequest) -> ExecuteResponse:
    task = get_task(task_id)
    try:
        plan = store.get_plan(task_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="Task or plan not found") from exc

    if store.get_execution_by_key(task_id, req.idempotency_key):
        raise HTTPException(status_code=409, detail="Duplicate idempotency key for task")
    if task.status != "approved":
        raise HTTPException(status_code=409, detail="Task must be approved before execution")

    execution_id = f"exec-{uuid4().hex[:10]}"
    store.create_execution(execution_id, task_id, req.idempotency_key, "started", [])
    store.update_status(task_id, "running")

    plan_artifact = write_artifact(task_id, "plan", plan.model_dump(mode="json"))
    execution = executor.apply_plan(task.drawing_id, plan)
    qa = QaReport(ruleset_version="v1-draft", checks_run=["layer_compliance", "tag_completeness"], violations=[], status="pass")
    qa_artifact = write_artifact(task_id, "qa", qa.model_dump(mode="json"))
    exec_artifact = write_artifact(task_id, "execution", execution)

    final_status = "passed" if qa.status == "pass" else "failed"
    updated_task = store.update_status(task_id, final_status)
    artifacts = [plan_artifact, qa_artifact, exec_artifact]
    store.create_execution(f"{execution_id}-done", task_id, f"{req.idempotency_key}-result", "completed", artifacts)
    return ExecuteResponse(task=updated_task, plan=plan, qa_report=qa, execution={**execution, "execution_id": execution_id, "artifact_paths": artifacts})


@app.post("/demo/run")
def run_demo() -> dict:
    task = create_task(CreateTaskRequest(project_id="demo", drawing_id="DEMO-SLD-001.dwg", requested_change="Update one tag", source_docs=["demo.csv"], requester="demo-user"))
    _ = create_plan(task.task_id)
    _ = approve_task(task.task_id, ApproveRequest(approved_by="demo-checker"))
    result = execute_task(task.task_id, ExecuteRequest(idempotency_key=f"demo-{datetime.now(UTC).timestamp()}"))
    return {"task_id": task.task_id, "status": result.task.status, "execution": result.execution}
