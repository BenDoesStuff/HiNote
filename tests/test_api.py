import importlib
import os

import pytest
from fastapi.testclient import TestClient

# Fixture to create TestClient with temporary music directory
@pytest.fixture
def client(tmp_path, monkeypatch):
    monkeypatch.setenv("MUSIC_DIR", str(tmp_path))
    monkeypatch.setenv("HINOTE_TOKEN", "testtoken")
    import hinote.main as main
    importlib.reload(main)
    with TestClient(main.app) as c:
        yield c


def test_get_songs_requires_auth(client):
    response = client.get("/api/songs")
    assert response.status_code == 401


def test_get_songs_returns_list(client):
    headers = {"Authorization": "Bearer testtoken"}
    response = client.get("/api/songs", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)
