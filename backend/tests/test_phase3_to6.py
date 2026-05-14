from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_idempotency_and_artifacts() -> None:
    create = client.post("/tasks", json={"project_id": "p3", "drawing_id": "SLD-300.dwg", "requested_change": "Change attribute", "source_docs": [], "requester": "eng3"})
    task_id = create.json()["task_id"]
    client.post(f"/tasks/{task_id}/plan")
    client.post(f"/tasks/{task_id}/approve", json={"approved_by": "checker3"})

    first = client.post(f"/tasks/{task_id}/execute", json={"idempotency_key": "abc-1"})
    assert first.status_code == 200
    assert len(first.json()["execution"]["artifact_paths"]) == 3

    dup = client.post(f"/tasks/{task_id}/execute", json={"idempotency_key": "abc-1"})
    assert dup.status_code == 409


def test_demo_endpoint() -> None:
    response = client.post("/demo/run")
    assert response.status_code == 200
    assert response.json()["status"] in {"passed", "failed"}
