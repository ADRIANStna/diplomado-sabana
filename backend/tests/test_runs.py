from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.core.config import settings
from app.main import app

client = TestClient(app)
CONVERSATIONS_URL = f"{settings.api_prefix}/conversations"


def new_conversation() -> str:
    return client.post(CONVERSATIONS_URL, json={}).json()["id"]


def post_run(conversation_id: str, message: str = "Hola"):
    return client.post(
        f"{CONVERSATIONS_URL}/{conversation_id}/runs",
        json={"message": message},
    )


def test_run_returns_simulated_reply() -> None:
    conversation_id = new_conversation()

    response = post_run(conversation_id)

    assert response.status_code == 201
    body = response.json()
    UUID(body["id"])
    assert body["conversation_id"] == conversation_id
    assert body["status"] == "completed"
    assert body["input"] == "Hola"
    assert body["output"] == "[Simulación] Respuesta 1 a: Hola"


def test_run_receives_previous_runs_of_its_conversation() -> None:
    conversation_id = new_conversation()

    post_run(conversation_id, "Primera")
    body = post_run(conversation_id, "Segunda").json()

    assert body["output"] == "[Simulación] Respuesta 2 a: Segunda"


def test_history_is_not_shared_between_conversations() -> None:
    post_run(new_conversation())

    body = post_run(new_conversation()).json()

    assert body["output"] == "[Simulación] Respuesta 1 a: Hola"


def test_unknown_conversation_returns_404() -> None:
    assert post_run(str(uuid4())).status_code == 404


@pytest.mark.parametrize("message", ["", "   ", "x" * 20_001])
def test_invalid_message_returns_422(message: str) -> None:
    assert post_run(new_conversation(), message).status_code == 422
