from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class RunCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    message: str = Field(min_length=1, max_length=20_000)


class RunRead(BaseModel):
    id: UUID
    conversation_id: UUID
    status: Literal["completed"]
    input: str
    output: str
    created_at: datetime
