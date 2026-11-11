# contracts · acuerdos entre módulos

Lo que aquí se define es la frontera entre `ai/`, `backend/` y `frontend/`. Un cambio requiere acuerdo de los tres docentes y un registro en [`docs/decisions/`](../docs/decisions/).

| Archivo | Qué define | Clase |
|---|---|---|
| `tool_schemas.py` | esquemas de herramientas | 1 |
| `engine.py` | `AgentEngine`, `ToolGateway`, `Retriever` | 6 |
| `openapi.json` | API pública `/v1` | 7 |
| `examples/` | peticiones y respuestas de ejemplo | 7 |
| `events.schema.json` | eventos SSE | 9 |
