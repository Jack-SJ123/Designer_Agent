import json
import sqlite3
from contextlib import contextmanager
from datetime import UTC, datetime

from .models import ActionPlan, CreateTaskRequest, TaskRecord


class TaskStore:
    def __init__(self, db_path: str = "backend/data/agent.db") -> None:
        self.db_path = db_path

    @contextmanager
    def _conn(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        finally:
            conn.close()

    def init(self) -> None:
        with self._conn() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS tasks (
                    task_id TEXT PRIMARY KEY,
                    project_id TEXT NOT NULL,
                    drawing_id TEXT NOT NULL,
                    requested_change TEXT NOT NULL,
                    source_docs TEXT NOT NULL,
                    requester TEXT NOT NULL,
                    status TEXT NOT NULL,
                    approved_by TEXT,
                    approved_at TEXT,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS plans (
                    task_id TEXT PRIMARY KEY,
                    payload TEXT NOT NULL,
                    FOREIGN KEY(task_id) REFERENCES tasks(task_id)
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS executions (
                    execution_id TEXT PRIMARY KEY,
                    task_id TEXT NOT NULL,
                    idempotency_key TEXT NOT NULL,
                    status TEXT NOT NULL,
                    artifact_paths TEXT NOT NULL,
                    created_at TEXT NOT NULL
                )
                """
            )

    def create_task(self, task_id: str, req: CreateTaskRequest) -> TaskRecord:
        now = datetime.now(UTC).isoformat()
        with self._conn() as conn:
            conn.execute(
                """INSERT INTO tasks(task_id, project_id, drawing_id, requested_change, source_docs,
                   requester, status, approved_by, approved_at, created_at, updated_at)
                   VALUES (?, ?, ?, ?, ?, ?, 'queued', NULL, NULL, ?, ?)""",
                (task_id, req.project_id, req.drawing_id, req.requested_change, json.dumps(req.source_docs), req.requester, now, now),
            )
        return self.get_task(task_id)

    def get_task(self, task_id: str) -> TaskRecord:
        with self._conn() as conn:
            row = conn.execute("SELECT * FROM tasks WHERE task_id=?", (task_id,)).fetchone()
        if not row:
            raise KeyError(task_id)
        return TaskRecord(
            task_id=row["task_id"], project_id=row["project_id"], drawing_id=row["drawing_id"],
            requested_change=row["requested_change"], source_docs=json.loads(row["source_docs"]), requester=row["requester"],
            status=row["status"], approved_by=row["approved_by"],
            approved_at=datetime.fromisoformat(row["approved_at"]) if row["approved_at"] else None,
            created_at=datetime.fromisoformat(row["created_at"]), updated_at=datetime.fromisoformat(row["updated_at"]),
        )

    def update_status(self, task_id: str, status: str, approved_by: str | None = None) -> TaskRecord:
        now = datetime.now(UTC).isoformat()
        approved_at = now if approved_by else None
        with self._conn() as conn:
            conn.execute(
                "UPDATE tasks SET status=?, approved_by=COALESCE(?, approved_by), approved_at=COALESCE(?, approved_at), updated_at=? WHERE task_id=?",
                (status, approved_by, approved_at, now, task_id),
            )
        return self.get_task(task_id)

    def save_plan(self, task_id: str, plan: ActionPlan) -> None:
        with self._conn() as conn:
            conn.execute(
                "INSERT INTO plans(task_id, payload) VALUES(?, ?) ON CONFLICT(task_id) DO UPDATE SET payload=excluded.payload",
                (task_id, plan.model_dump_json()),
            )

    def get_plan(self, task_id: str) -> ActionPlan:
        with self._conn() as conn:
            row = conn.execute("SELECT payload FROM plans WHERE task_id=?", (task_id,)).fetchone()
        if not row:
            raise KeyError(task_id)
        return ActionPlan.model_validate_json(row["payload"])

    def get_execution_by_key(self, task_id: str, idempotency_key: str):
        with self._conn() as conn:
            return conn.execute("SELECT * FROM executions WHERE task_id=? AND idempotency_key=?", (task_id, idempotency_key)).fetchone()

    def create_execution(self, execution_id: str, task_id: str, idempotency_key: str, status: str, artifact_paths: list[str]) -> None:
        now = datetime.now(UTC).isoformat()
        with self._conn() as conn:
            conn.execute(
                "INSERT INTO executions(execution_id, task_id, idempotency_key, status, artifact_paths, created_at) VALUES (?, ?, ?, ?, ?, ?)",
                (execution_id, task_id, idempotency_key, status, json.dumps(artifact_paths), now),
            )
