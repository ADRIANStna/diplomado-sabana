from datetime import datetime, timezone
from uuid import UUID, uuid4

from app.schemas.conversation import ConversationCreate, ConversationRead
from app.schemas.run import RunCreate, RunRead
from app.services import assistant

# Almacenamiento en memoria: los datos se pierden al reiniciar el servidor.
_conversations: dict[UUID, ConversationRead] = {}
_runs: dict[UUID, list[RunRead]] = {}


class ConversationNotFoundError(Exception):
    pass


def create_conversation(data: ConversationCreate) -> ConversationRead:
    conversation = ConversationRead(
        id=uuid4(),
        title=data.title,
        created_at=datetime.now(timezone.utc),
    )
    _conversations[conversation.id] = conversation
    return conversation


def create_run(conversation_id: UUID, data: RunCreate) -> RunRead:
    if conversation_id not in _conversations:
        raise ConversationNotFoundError

    history = _runs.setdefault(conversation_id, [])
    run = RunRead(
        id=uuid4(),
        conversation_id=conversation_id,
        status="completed",
        input=data.message,
        output=assistant.generate_reply(history, data.message),
        created_at=datetime.now(timezone.utc),
    )
    history.append(run)
    return run
