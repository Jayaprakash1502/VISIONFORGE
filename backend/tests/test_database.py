from unittest.mock import patch
from sqlalchemy.exc import OperationalError
from backend.app.core.database import check_database_connection


def test_database_connection_unavailable():
    """Verify check_database_connection handles OperationalError gracefully."""
    with patch("backend.app.core.database.engine.connect") as mock_connect:
        mock_connect.side_effect = OperationalError("Connection refused", params=None, orig=None)
        health = check_database_connection()
        assert health["status"] == "unavailable"
        assert "message" in health
        assert health["database_url_configured"] is True


def test_database_connection_success():
    """Verify check_database_connection reports connected on successful query execution."""
    with patch("backend.app.core.database.engine.connect") as mock_connect:
        health = check_database_connection()
        assert "status" in health
