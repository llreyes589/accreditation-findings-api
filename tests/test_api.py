from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_findings_summary():
    response = client.get("/findings/summary")

    assert response.status_code == 200
    assert response.json() == {
        "raw_records": 12,
        "valid_records": 8
    }

def test_open_high_findings():
    response = client.get("/findings/open-high")

    assert response.status_code == 200

    findings = response.json()

    assert len(findings) == 3
    assert [finding["finding_id"] for finding in findings] == [
        "F-001",
        "F-004",
        "F-006",
    ]