# backend · Módulo II: backend e integración

Clases 7–12 · Docente: David Guasca · Hito II: API operativa (clase 12).

API FastAPI bajo `/v1`. Valida, decide y ejecuta: el agente solo propone. Usa [uv](https://docs.astral.sh/uv/) y Python 3.12 (fijado en `.python-version`).

## Puesta en marcha

Desde la carpeta `backend/` (el `.env` vive en la raíz del repositorio: `cp ../.env.example ../.env`):

```bash
uv sync
uv run fastapi dev app/main.py     # http://127.0.0.1:8000/docs
uv run pytest                      # no requiere claves de LLM
```

Dependencias nuevas: `uv add <paquete>` o `uv add --dev <paquete>`.

## Estado de la clase 7

Ya existe:

- `create_app()` en [`app/main.py`](app/main.py) y rutas en [`app/api/routes.py`](app/api/routes.py) bajo `/v1`.
- `GET /v1/health` y `POST /v1/conversations` (201).
- `POST /v1/conversations/{id}/runs`: hoy responde 201 de forma síncrona con un run `completed` y una respuesta simulada de `generate_reply(history, message)` ([`app/services/assistant.py`](app/services/assistant.py)).
- Almacenamiento en memoria dentro de [`app/services/conversations.py`](app/services/conversations.py).

Falta para cumplir el contrato de la clase 7:

- [ ] `POST /v1/conversations/{id}/runs` → 202 `{run_id, conversation_id, status}`.
- [ ] `GET /v1/conversations/{id}` y `GET /v1/runs/{id}` (200 · 404).
- [ ] `POST /v1/documents` (201 · 413 · 415, límite `MAX_UPLOAD_MB`).
- [ ] Formato de error único `{"error": {"code", "message", "request_id"}}` en `core/errors.py`.
- [ ] Identificadores en `core/ids.py`.
- [ ] Identidad temporal `X-User-Id` en `api/deps.py` y propiedad (recurso ajeno → 404).
- [ ] Mover el almacenamiento a `repositories/` (en memoria).
- [ ] `generate_reply` → `services/stub_engine.py` (`StubAgentEngine`).
- [ ] Exportar `contracts/openapi.json` y ejemplos en `contracts/examples/`.

## Laboratorios

| Clase | Entregable | Estado | Evidencia |
|---|---|---|---|
| 7 | `app/`, `contracts/openapi.json` | en curso | |
| 8 | `app/models/`, `app/db/`, `migrations/` | pendiente | |
| 9 | `app/api/stream.py`, `app/services/run_manager.py`, `contracts/events.schema.json` | pendiente | |
| 10 | `app/security/` | pendiente | |
| 11 | `app/integrations/` | pendiente | |
| 12 | `infrastructure/`, `.github/workflows/ci.yml`, `docs/backend_runbook.md` | pendiente | |
