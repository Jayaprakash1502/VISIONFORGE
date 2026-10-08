from backend.app.core.config import Settings, get_settings


def test_default_settings():
    """Verify default settings instantiation."""
    settings = Settings()
    assert settings.PROJECT_NAME == "VISIONFORGE API"
    assert settings.API_PORT == 8000
    assert isinstance(settings.CORS_ORIGINS, list)


def test_cors_origins_parsing():
    """Verify CORS_ORIGINS parser handles string and JSON list inputs."""
    s1 = Settings(CORS_ORIGINS='["http://localhost:3000", "http://example.com"]')
    assert s1.CORS_ORIGINS == ["http://localhost:3000", "http://example.com"]

    s2 = Settings(CORS_ORIGINS="http://localhost:5173, http://127.0.0.1:5173")
    assert s2.CORS_ORIGINS == ["http://localhost:5173", "http://127.0.0.1:5173"]
