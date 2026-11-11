# ai · Módulo I: motor agéntico

Clases 1–6 · Docente: Oscar Rodríguez · Hito I: motor agéntico evaluado (clase 6).

El motor se expone al resto del sistema solo a través de `ai.engine.build_engine()` y de los puertos definidos en [`contracts/`](../contracts/). No importa nada de `backend/`, no abre conexiones a la base de datos y no escribe: propone.

## Puesta en marcha

Desde la **raíz** del repositorio (el paquete `ai` se importa desde ahí):

```bash
uv sync --project ai
uv run --project ai pytest ai/tests
uv run --project ai python -m ai.run "Revisa SOL-014"
```

Dependencias nuevas: `uv add --project ai <paquete>` (o `--dev` para herramientas de prueba).

## Mientras tanto

Hasta que exista `build_engine()`, el backend responde con una simulación en `generate_reply(history, message)` ([`backend/app/services/assistant.py`](../backend/app/services/assistant.py)), que pasará a ser `StubAgentEngine`.

## Laboratorios

| Clase | Entregable | Estado | Evidencia |
|---|---|---|---|
| 1 | `agents/basic_agent.py`, `tools/requests.py`, `contracts/tool_schemas.py` | pendiente | |
| 2 | `rag/` | pendiente | |
| 3 | `graphs/` | pendiente | |
| 4 | `mcp_server/` | pendiente | |
| 5 | `agents/supervisor.py`, `a2a_agent/` | pendiente | |
| 6 | `evals/`, `engine.py`, `docs/ai_contracts.md` | pendiente | |
