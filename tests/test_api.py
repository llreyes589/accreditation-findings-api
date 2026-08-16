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
    assert findings[0]["institution"] == "Hospital Alpha"
    assert findings[0]["inspection_date"] == "2026-01-15T00:00:00"
    assert findings[0]["corrective_action_days"] == 30.0

def test_quality_report():
    response = client.get("/findings/quality-report")

    assert response.status_code == 200

    report = response.json()

    assert report["total_rows"] == 12
    assert report["duplicate_finding_id_count"] == 1
    assert report["invalid_inspection_date_count"] == 1
    assert report["missing_values"] == {
        "institution": 1,
        "inspection_date": 1,
        "corrective_action_days": 1
    }