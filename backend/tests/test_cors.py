from fastapi import status


def test_cors_preflight_allowed_origin(client):
    """Test CORS preflight headers for an allowed origin."""
    headers = {
        "Origin": "http://localhost:5173",
        "Access-Control-Request-Method": "GET",
        "Access-Control-Request-Headers": "Content-Type",
    }
    response = client.options("/api/v1/health", headers=headers)
    assert response.status_code == status.HTTP_200_OK
    assert response.headers.get("access-control-allow-origin") == "http://localhost:5173"


def test_cors_disallowed_origin(client):
    """Test CORS preflight headers for an unapproved origin."""
    headers = {
        "Origin": "http://unauthorized-domain.com",
        "Access-Control-Request-Method": "GET",
    }
    response = client.options("/api/v1/health", headers=headers)
    # FastAPIs CORSMiddleware does not include access-control-allow-origin for unauthorized origins
    assert response.headers.get("access-control-allow-origin") != "http://unauthorized-domain.com"
