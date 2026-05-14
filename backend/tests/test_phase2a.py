from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_validate_and_execute_simulated_autocad() -> None:
    created = client.post(
        "/tasks",
        json={
            "project_id": "p2",
            "drawing_id": "SLD-200.dwg",
            "requested_change": "Insert symbol",
            "source_docs": [],
            "requester": "eng2",
        },
    )
    task_id = created.json()["task_id"]

    client.post(f"/tasks/{task_id}/plan")
    validation = client.post(f"/tasks/{task_id}/validate")
    assert validation.status_code == 200
    assert validation.json()["status"] == "pass"

    client.post(f"/tasks/{task_id}/approve", json={"approved_by": "checker2"})
    executed = client.post(f"/tasks/{task_id}/execute")
    assert executed.status_code == 200
    assert executed.json()["execution"]["status"] == "dry_run"
