"""Tests for FastAPI endpoints."""

from fastapi.testclient import TestClient

from backend.api.main import app

client = TestClient(app)


def test_root():
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()


def test_health():
    """Test health endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_analyze_endpoint():
    """Test analyze endpoint."""
    response = client.post("/analyze", json={"adresse": "Paris, France"})
    assert response.status_code == 200
    assert "workflow_id" in response.json()


def test_status_endpoint():
    """Test status endpoint."""
    # First create a workflow
    analyze_response = client.post("/analyze", json={"adresse": "Paris, France"})
    workflow_id = analyze_response.json()["workflow_id"]

    # Then check status
    response = client.get(f"/status/{workflow_id}")
    assert response.status_code == 200
    assert response.json()["workflow_id"] == workflow_id


def test_status_endpoint_not_found():
    """Test status endpoint with non-existent workflow."""
    response = client.get("/status/non-existent-id")
    assert response.status_code == 404






