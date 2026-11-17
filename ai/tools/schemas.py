"""Esquema de argumentos para la herramienta de puntuación."""
from pydantic import BaseModel, Field

class PuntuacionInput(BaseModel):
    impacto: int = Field(ge=1, le=3)
    urgencia: int = Field(ge=1, le=3)
