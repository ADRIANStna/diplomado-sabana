from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class ConversationCreate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)


class ConversationRead(BaseModel):
    id: UUID
    title: str | None
    created_at: datetime
