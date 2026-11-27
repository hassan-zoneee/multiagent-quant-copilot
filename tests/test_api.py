import psycopg
from fastapi.testclient import TestClient

from copilot import __version__, api

client = TestClient(api.app)


class FakeResult:
    def __init__(self, row):
        self._row = row

    def fetchone(self):
        return self._row


class FakeConnection:
    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    def execute(self, query):
        return FakeResult(("0.8.0",))


def test_health_ok():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "version": __version__}


def test_health_db_ok(monkeypatch):
    monkeypatch.setattr(api, "get_connection", lambda: FakeConnection())
    response = client.get("/health/db")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "database": "up", "pgvector": "0.8.0"}


def test_health_db_unavailable(monkeypatch):
    def broken():
        raise psycopg.OperationalError("boom")

    monkeypatch.setattr(api, "get_connection", broken)
    response = client.get("/health/db")
    assert response.status_code == 503
    assert response.json() == {"detail": "database unavailable"}
