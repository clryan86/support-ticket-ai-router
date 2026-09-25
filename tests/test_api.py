from pathlib import Path
from fastapi.testclient import TestClient

from app.config import Settings
from app.main import create_app

def test_route_batch_feedback_metrics(tmp_path: Path):
    c = TestClient(create_app(Settings(tmp_path / "artifacts", tmp_path / "tickets.db")))
    response = c.post("/api/route", json={
        "subject": "Payment issue",
        "body": "I was charged twice and need help with my invoice",
    })
    assert response.status_code == 200
    body = response.json()
    assert body["category"] == "billing"
    assert body["queue"] == "Billing Operations"

    batch = c.post("/api/route/batch", json={"items": [
        {"subject": "Login issue", "body": "I am locked out of my account"},
        {"subject": "Feature", "body": "Please add dark mode"},
    ]})
    assert batch.status_code == 200
    assert len(batch.json()) == 2

    feedback = c.post(
        f"/api/tickets/{body['ticket_id']}/feedback",
        json={"correct_category": "billing", "notes": "correct"},
    )
    assert feedback.status_code == 200
    metrics = c.get("/api/metrics").json()
    assert metrics["tickets"] == 3
    assert metrics["feedback"] == 1
