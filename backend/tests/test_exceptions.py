from fastapi import status
from fastapi.testclient import TestClient
from unittest.mock import patch
from backend.app.main import app


def test_404_not_found(client):
    """Verify that non-existent routes return structured JSON error responses."""
    response = client.get("/api/v1/nonexistent-route")
    assert response.status_code == status.HTTP_404_NOT_FOUND

    data = response.json()
    assert data["error"] is True
    assert data["code"] == status.HTTP_404_NOT_FOUND
    assert "message" in data


def test_unhandled_exception_structure():
    """Verify unhandled exceptions return structured JSON 500 without leaking stack traces."""
    client_no_raise = TestClient(app, raise_server_exceptions=False)
    with patch("backend.app.api.v1.endpoints.health.check_database_connection") as mock_check:
        mock_check.side_effect = RuntimeError("Simulated crash")
        response = client_no_raise.get("/api/v1/health")
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR

        data = response.json()
        assert data["error"] is True
        assert data["code"] == 500
        assert data["message"] == "An internal server error occurred"
        # Ensure no traceback or internal exception message leaked in response body
        assert "Simulated crash" not in str(data)
        assert "Traceback" not in str(data)
