import os
from datetime import UTC, datetime
from typing import Any

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


class CadAction(BaseModel):
    action_type: str
    target_selector: dict[str, Any]
    parameters: dict[str, Any]
    tolerance: float | None = None
    rollback_hint: str


class ActionPlan(BaseModel):
    plan_id: str
    risk_level: str
    assumptions: list[str] = []
    required_approvals: list[str] = []
    actions: list[CadAction]


class ApplyPlanRequest(BaseModel):
    drawing_path: str
    plan: ActionPlan


app = FastAPI(title="AutoCAD Runner", version="0.2.0")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


def _open_autocad_document(drawing_path: str):
    try:
        import win32com.client  # type: ignore
    except Exception as exc:  # pragma: no cover - Windows runtime dependency
        raise RuntimeError("pywin32 is required for real AutoCAD mode: pip install pywin32") from exc

    acad = win32com.client.Dispatch("AutoCAD.Application")
    acad.Visible = False
    doc = acad.Documents.Open(drawing_path)
    return acad, doc


def apply_update_attribute_real(drawing_path: str, action: CadAction) -> dict[str, Any]:
    block_name = str(action.target_selector.get("block_name", "")).upper()
    attr_name = str(action.parameters.get("attribute", "")).upper()
    new_value = str(action.parameters.get("value", ""))

    if not block_name or not attr_name:
        raise ValueError("target_selector.block_name and parameters.attribute are required")

    acad, doc = _open_autocad_document(drawing_path)
    touched = 0

    try:
        for entity in doc.ModelSpace:
            if getattr(entity, "ObjectName", "") != "AcDbBlockReference":
                continue
            if str(getattr(entity, "EffectiveName", "")).upper() != block_name:
                continue
            if not entity.HasAttributes:
                continue

            for att_ref in entity.GetAttributes():
                if str(att_ref.TagString).upper() == attr_name:
                    att_ref.TextString = new_value
                    touched += 1

        if touched == 0:
            raise RuntimeError(f"No matching attributes found for block='{block_name}' attribute='{attr_name}'")

        doc.Save()
        return {
            "mode": "real",
            "drawing_path": drawing_path,
            "block_name": block_name,
            "attribute": attr_name,
            "value": new_value,
            "updated_count": touched,
        }
    finally:
        try:
            doc.Close(True)
        finally:
            acad.Quit()


@app.post("/apply-plan")
def apply_plan(request: ApplyPlanRequest) -> dict[str, Any]:
    real_mode = os.getenv("EDA_AUTOCAD_REAL", "0") == "1"
    results: list[dict[str, Any]] = []

    for action in request.plan.actions:
        if action.action_type != "update_attribute":
            raise HTTPException(status_code=400, detail=f"Unsupported action_type: {action.action_type}")

        try:
            if real_mode:
                result = apply_update_attribute_real(request.drawing_path, action)
            else:
                result = {
                    "mode": "simulated",
                    "drawing_path": request.drawing_path,
                    "attribute": action.parameters.get("attribute"),
                    "value": action.parameters.get("value"),
                }
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc

        results.append(result)

    return {
        "status": "remote_runner_ok",
        "engine": "windows-autocad-runner",
        "applied_actions": len(results),
        "executed_at": datetime.now(UTC).isoformat(),
        "results": results,
    }
