from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_task_lifecycle() -> None:
    create = client.post(
        "/tasks",
        json={
            "project_id": "p1",
            "drawing_id": "SLD-100.dwg",
            "requested_change": "Update feeder tags",
            "source_docs": ["loadlist.xlsx"],
            "requester": "eng1",
        },
    )
    assert create.status_code == 200
    task = create.json()
    assert task["status"] == "queued"
    task_id = task["task_id"]

    planned = client.post(f"/tasks/{task_id}/plan")
    assert planned.status_code == 200

    approved = client.post(f"/tasks/{task_id}/approve", json={"approved_by": "checker1"})
    assert approved.status_code == 200
    assert approved.json()["status"] == "approved"

    executed = client.post(f"/tasks/{task_id}/execute")
    assert executed.status_code == 200
    body = executed.json()
    assert body["task"]["status"] == "passed"
    assert body["execution"]["status"] == "dry_run"
