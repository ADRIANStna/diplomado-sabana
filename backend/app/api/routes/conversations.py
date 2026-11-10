from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from app.schemas.conversation import ConversationCreate, ConversationRead
from app.schemas.run import RunCreate, RunRead
from app.services import conversations as conversations_service

router = APIRouter()


@router.post(
    "/conversations",
    response_model=ConversationRead,
    status_code=status.HTTP_201_CREATED,
)
def create_conversation(payload: ConversationCreate) -> ConversationRead:
    return conversations_service.create_conversation(payload)


@router.post(
    "/conversations/{conversation_id}/runs",
    response_model=RunRead,
    status_code=status.HTTP_201_CREATED,
)
def create_run(conversation_id: UUID, payload: RunCreate) -> RunRead:
    try:
        return conversations_service.create_run(conversation_id, payload)
    except conversations_service.ConversationNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversación no encontrada.",
        ) from exc
