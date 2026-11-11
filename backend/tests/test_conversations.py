from datetime import datetime
from uuid import UUID

import pytest
from fastapi.testclient import TestClient

from app.core.config import settings
from app.main import app
from app.services import conversations as conversations_service

client = TestClient(app)
URL = f"{settings.api_prefix}/conversations"


def test_create_conversation_with_title() -> None:
    response = client.post(URL, json={"title": "Mi conversación"})

    assert response.status_code == 201
    body = response.json()
    assert body["title"] == "Mi conversación"
    assert datetime.fromisoformat(body["created_at"]).tzinfo is not None
    assert UUID(body["id"]) in conversations_service._conversations


def test_create_conversation_without_title() -> None:
    response = client.post(URL, json={})

    assert response.status_code == 201
    assert response.json()["title"] is None


def test_each_conversation_gets_its_own_id() -> None:
    first = client.post(URL, json={}).json()
    second = client.post(URL, json={}).json()

    assert first["id"] != second["id"]


@pytest.mark.parametrize("title", ["", "x" * 201])
def test_create_conversation_rejects_invalid_title(title: str) -> None:
    response = client.post(URL, json={"title": title})

    assert response.status_code == 422
