import pytest
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.core.config import Settings, get_settings


@pytest.fixture
def client():
    """Provides a FastAPI TestClient instance."""
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def mock_settings(monkeypatch):
    """Fixture for setting custom environment settings during tests."""
    def _set_env(**kwargs):
        for key, value in kwargs.items():
            monkeypatch.setenv(key, str(value))
        get_settings.cache_clear()
        return get_settings()
    return _set_env
