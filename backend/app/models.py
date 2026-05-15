from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, Field


class TaskRequest(BaseModel):
    task_id: str = Field(..., description="Unique task identifier.")
    project_id: str
    drawing_id: str
    requested_change: str
    source_docs: list[str] = Field(default_factory=list)
    requester: str


class CreateTaskRequest(BaseModel):
    project_id: str
    drawing_id: str
    requested_change: str
    source_docs: list[str] = Field(default_factory=list)
    requester: str


class TaskRecord(BaseModel):
    task_id: str
    project_id: str
    drawing_id: str
    requested_change: str
    source_docs: list[str] = Field(default_factory=list)
    requester: str
    status: Literal["queued", "planned", "approved", "running", "passed", "failed"]
    approved_by: str | None = None
    approved_at: datetime | None = None
    created_at: datetime
    updated_at: datetime


class ApproveRequest(BaseModel):
    approved_by: str


class ExecuteRequest(BaseModel):
    idempotency_key: str


class CadAction(BaseModel):
    action_type: Literal[
        "locate_block",
        "replace_block_variant",
        "update_attribute",
        "insert_symbol",
        "add_leader_note",
        "revision_cloud",
    ]
    target_selector: dict[str, Any]
    parameters: dict[str, Any]
    tolerance: float | None = None
    rollback_hint: str


class ActionPlan(BaseModel):
    plan_id: str
    risk_level: Literal["low", "medium", "high"]
    assumptions: list[str] = Field(default_factory=list)
    required_approvals: list[str] = Field(default_factory=list)
    actions: list[CadAction]


class QaReport(BaseModel):
    ruleset_version: str
    checks_run: list[str]
    violations: list[str]
    status: Literal["pass", "fail"]


class ExecuteResponse(BaseModel):
    task: TaskRecord
    plan: ActionPlan
    qa_report: QaReport
    execution: dict[str, Any]
