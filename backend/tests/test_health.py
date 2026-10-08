from fastapi import status


def test_health_endpoint_v1(client):
    """Test that GET /api/v1/health returns 200 and expected schema."""
    response = client.get("/api/v1/health")
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert "status" in data
    assert data["service"] == "visionforge-api"
    assert "version" in data
    assert "environment" in data
    assert "database" in data
    assert isinstance(data["database"], dict)
    assert "status" in data["database"]


def test_health_endpoint_aliases(client):
    """Test top-level health endpoint aliases (/api/health and /health)."""
    res1 = client.get("/api/health")
    assert res1.status_code == status.HTTP_200_OK

    res2 = client.get("/health")
    assert res2.status_code == status.HTTP_200_OK
