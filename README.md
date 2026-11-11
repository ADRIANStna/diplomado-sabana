# Agentic ServiceDesk · diplomado-sabana

Proyecto integrador del diplomado **Agentic Builders: Desarrollo de Agentes de IA en Producción** (Universidad de La Sabana, 2026-II).

Una aplicación agéntica que revisa solicitudes de servicio contra la política vigente. El agente consulta documentos (RAG), lee los datos de la solicitud (MCP), pide un análisis a un agente remoto (A2A) y **propone** un cambio de estado. Un usuario autorizado aprueba o rechaza. Si aprueba, el backend ejecuta la acción una sola vez y deja trazabilidad.

> **Principio del proyecto:** el modelo propone; el backend valida, decide y ejecuta.
> Ningún control de permisos, aprobación o estado depende del agente ni de la interfaz.

El resultado final se despliega en un entorno de **staging**, no de producción. Las limitaciones se declaran en [`docs/limitations.md`](docs/limitations.md).

---

## Caso de referencia: SOL-014

1. El usuario escribe «Revisa SOL-014».
2. El agente recupera la sección vigente de la política, con documento, versión y sección.
3. Consulta los datos de SOL-014 (impacto, urgencia, estado) con una herramienta de solo lectura.
4. Pide un análisis estructurado al agente remoto.
5. Propone `request.update_status(SOL-014, "en_revision")`. El backend responde `require_approval` y el run queda en `waiting_for_approval`.
6. El usuario aprueba. El backend verifica permiso, expiración e idempotencia, ejecuta la acción y reanuda el agente.
7. La respuesta final cita sus fuentes y el run queda en `completed`.

Todos los datos son **sintéticos**. No se usan datos personales reales (Ley 1581 de 2012).

---

## Módulos y docentes

| Módulo | Clases | Docente | Carpeta principal | Hito |
|---|---|---|---|---|
| IA: motor agéntico | 1–6 | Oscar Rodríguez | [`ai/`](ai/) | I. Motor agéntico evaluado (clase 6) |
| Backend e integración | 7–12 | David Guasca | [`backend/`](backend/) | II. API operativa (clase 12) |
| Frontend y despliegue | 13–18 | Adrián Gil | [`frontend/`](frontend/), [`infrastructure/`](infrastructure/) | III. Aplicación en staging (clase 18) |

Los tres módulos se coordinan a través de [`contracts/`](contracts/). Un cambio en un contrato requiere acuerdo de los tres docentes y queda registrado en [`docs/decisions/`](docs/decisions/).

---

## Arquitectura en una vista

```
 Navegador (React)
     │  HTTPS: REST + SSE
     ▼
 API FastAPI /v1 ──► Policy Engine ──► allow · deny · require_approval
     │
 RunManager (estados del run, eventos)
     │  AgentEngine.stream / resume            ◄── frontera: contracts/
     ▼
 Motor de IA (LangGraph)
     │  puertos inyectados por el backend: ToolGateway · Retriever · checkpointer
     ▼
 Adaptadores del backend ──► Servidor MCP (solo lectura)
                         ──► Agente A2A analista
                         ──► PostgreSQL + pgvector
```

Reglas de frontera:

1. `backend/` solo importa `ai.engine.build_engine()` y `contracts/`; nunca nodos internos de `ai/`.
2. `ai/` no importa nada de `backend/` ni abre conexiones a la base de datos; recibe sus dependencias por inyección.
3. Ninguna escritura ocurre dentro de `ai/`. El grafo propone; el backend ejecuta tras la aprobación.
4. Cada lado se prueba sin el otro: `ai/` con implementaciones locales de los puertos; `backend/` con `StubAgentEngine`.

Detalle completo en [`docs/architecture/`](docs/architecture/).

---

## Estructura del repositorio

Las carpetas existen desde el inicio. Cada clase llena las suyas; la columna indica cuándo.

```
diplomado-sabana/
├── ai/                          Módulo I · IA (Oscar)
│   ├── agents/                  agente básico, supervisor                    clases 1, 5
│   ├── tools/                   funciones deterministas con Pydantic         clase 1
│   ├── rag/                     ingest, index, retrieve, agentic             clase 2
│   ├── graphs/                  state, workflow, checkpoints                 clase 3
│   ├── mcp_server/              server, client, policies                     clase 4
│   ├── a2a_agent/               server, client                               clase 5
│   ├── prompts/                 prompts versionados                          clases 1–6
│   ├── evals/                   cases.jsonl, run_eval.py, report.csv         clase 6
│   ├── engine.py                build_engine(): única entrada pública        clase 6
│   ├── tests/
│   └── pyproject.toml
│
├── backend/                     Módulo II · Backend (David)
│   ├── app/
│   │   ├── main.py              create_app()                                 clase 7
│   │   ├── api/                 routes.py, deps.py, stream.py                clases 7, 9
│   │   ├── schemas/             entrada y salida Pydantic                    clase 7
│   │   ├── services/            conversations, runs, run_manager, stub_engine clases 7, 9
│   │   ├── repositories/        acceso a datos (memoria → PostgreSQL)        clases 7, 8
│   │   ├── models/              SQLAlchemy                                   clase 8
│   │   ├── db/                  session.py                                   clase 8
│   │   ├── security/            auth.py, policies.py                         clase 10
│   │   ├── integrations/        tool_gateway, mcp_adapter, a2a_adapter       clase 11
│   │   └── core/                config.py, errors.py, ids.py                 clase 7
│   ├── migrations/              Alembic                                      clase 8
│   ├── tests/
│   └── pyproject.toml
│
├── frontend/                    Módulo III · Frontend (Adrián)
│   ├── src/
│   │   ├── api/                 client.js, validación con Zod                clase 13
│   │   ├── features/            chat, conversations, runs, documents, approvals  clases 13–16
│   │   ├── components/          SourceCard, ArtifactCard                     clase 15
│   │   ├── hooks/               useRunStream                                 clase 14
│   │   └── types.js             tipos con JSDoc                              clase 13
│   ├── tests/                   unit/, e2e/                                  clase 17
│   └── package.json
│
├── contracts/                   Acuerdos entre módulos (cambios con los tres docentes)
│   ├── openapi.json             API pública                                  clase 7
│   ├── events.schema.json       eventos SSE                                  clase 9
│   ├── tool_schemas.py          esquemas de herramientas                     clase 1
│   ├── engine.py                AgentEngine, ToolGateway, Retriever          clase 6
│   └── examples/                peticiones y respuestas de ejemplo           clase 7
│
├── data/                        Solo datos sintéticos
│   ├── corpus/                  politicas_v1.pdf, politicas_v2.pdf, procedimientos.pdf
│   ├── seed/                    solicitudes.csv, usuarios.json
│   └── eval/                    eval_cases.jsonl, attacks.jsonl, malformed.pdf
│
├── infrastructure/              Dockerfile.backend, compose.yaml, Caddyfile  clases 12, 18
├── scripts/                     backup.sh, restore.sh                        clase 12
├── docs/
│   ├── architecture/            diagramas y flujo de un run
│   ├── decisions/               registros de decisión (0001-streaming.md, ...)
│   ├── ai_contracts.md          entrega del Hito I                           clase 6
│   ├── backend_runbook.md                                                    clase 12
│   ├── deployment.md · runbook.md · evaluation_report.md                     clase 18
│   └── limitations.md           lo que el sistema no cubre
├── .github/workflows/           ci.yml (lint, pruebas, escaneos), deploy.yml
├── steering.md                  convenciones del proyecto (se actualiza cada clase)
├── .env.example                 variables sin valores reales
├── .gitignore
└── README.md
```

Las carpetas que todavía no tienen contenido llevan un `.gitkeep`, un archivo vacío que solo sirve para que Git (y GitHub) las conserve. Se borra cuando la clase agrega el primer archivo a la carpeta.

---

## Requisitos

| Herramienta | Versión | Para qué |
|---|---|---|
| Python | 3.12 (fijado en `.python-version` de cada módulo) | `ai/` y `backend/` |
| [uv](https://docs.astral.sh/uv/) | reciente | entornos y dependencias de Python; descarga Python 3.12 si falta |
| Node.js | 20 o superior | `frontend/` |
| Docker y Docker Compose | recientes | PostgreSQL y el stack completo (desde la clase 8) |
| Git | cualquiera reciente | todo |

Las dependencias se fijan por cohorte en archivos de bloqueo (`uv.lock` y `package-lock.json`). No se actualizan durante el curso sin acuerdo docente. No se usan `pip install` ni `requirements.txt`: todo pasa por `uv add`, `uv sync` y `uv run`.

---

## Puesta en marcha

### 1. Variables de entorno

```bash
cp .env.example .env      # en la raíz; nunca se versiona .env
```

| Variable | Ejemplo | Uso |
|---|---|---|
| `ENV` | `dev` | `dev` habilita la identidad temporal por cabecera (solo hasta la clase 10) |
| `ENGINE` | `stub` | `stub` (sin LLM) o `real` (motor de `ai/`) |
| `MAX_UPLOAD_MB` | `10` | límite de documentos (413 si se excede) |
| `DATABASE_URL` | `postgresql+psycopg://...` | desde la clase 8 |
| `LLM_PROVIDER`, `LLM_MODEL`, `LLM_API_KEY` | | credenciales de laboratorio con límite de costo |
| `MCP_SERVER_URL`, `A2A_AGENT_URL` | | desde la clase 11 |
| `JWT_SECRET`, `JWT_ISSUER`, `JWT_AUDIENCE` | | desde la clase 10 |

### 2. Backend (desde la clase 7)

```bash
cd backend
uv sync                                  # crea .venv con Python 3.12 y el grupo dev
uv run fastapi dev app/main.py           # http://localhost:8000/docs
uv run pytest                            # no requiere claves de LLM
```

Con la identidad temporal de desarrollo, cada petición lleva la cabecera `X-User-Id: user-a` (o `user-b` para probar aislamiento). **No es un control de seguridad**; se reemplaza por JWT en cookie en la clase 10.

### 3. Motor de IA (clases 1–6)

El paquete `ai` se importa desde la raíz del repositorio, así que estos comandos se ejecutan **desde la raíz**:

```bash
uv sync --project ai
uv run --project ai python -m ai.run "Revisa SOL-014"     # ejecución local
uv run --project ai python -m ai.evals.run_eval           # suite de evaluación
uv run --project ai pytest ai/tests
```

### 4. Frontend (desde la clase 13)

```bash
cd frontend
npm ci
npm run dev                           # usa el backend o el stub según VITE_API_URL
npm test
```

### 5. Stack completo (desde la clase 12)

```bash
docker compose -f infrastructure/compose.yaml up --build
```

---

## Contratos clave

**Formato de error único**

```json
{"error": {"code": "not_found", "message": "Conversación no encontrada", "request_id": "req-7f3a9c01d2e4"}}
```

**Identificadores**

| Identificador | Qué identifica | Lo genera |
|---|---|---|
| `user_id` | persona autenticada | sistema |
| `conversation_id` | hilo de conversación | API |
| `run_id` | una ejecución del agente | API |
| `thread_id` | checkpoint del grafo | servicio de ejecución |
| `task_id` | tarea en el agente A2A (se mapea a `run_id`) | agente remoto |
| `approval_id` | propuesta que requiere decisión; clave de idempotencia | servicio de aprobaciones |
| `trace_id` | traza distribuida | instrumentación |

**Estados del run:** `queued → running → waiting_for_approval → running → completed`. `failed` y `canceled` desde cualquier estado activo. Un estado terminal no se vuelve a ejecutar.

**Eventos SSE:** `run_started`, `tool_started`, `tool_finished`, `tool_failed`, `delta`, `run_completed`, `run_failed`, `run_canceled`, `document_status`. Cada evento lleva `event_id` creciente por run, `run_id`, `seq`, `type`, `at` y `payload` sin datos internos.

**Endpoints base (`/v1`)**

| Método y ruta | Respuesta | Clase |
|---|---|---|
| `GET /v1/health` | 200 | 7 |
| `POST /v1/conversations` | 201 | 7 |
| `GET /v1/conversations/{id}` | 200 · 404 | 7 |
| `POST /v1/conversations/{id}/runs` | 202 `{run_id, conversation_id, status}` | 7 |
| `GET /v1/runs/{id}` | 200 · 404 | 7 |
| `POST /v1/documents` | 201 · 413 · 415 | 7 |
| `GET /v1/runs/{id}/events` | SSE con `Last-Event-ID` | 9 |
| `POST /v1/approvals/{id}/decision` | 200 · 403 · 409 | 10 |

---

## Convenciones

Las reglas completas están en [`steering.md`](steering.md). Las que bloquean una entrega:

- Sin secretos en el código, en los prompts ni en los logs.
- Toda entrada y salida de la API se valida con Pydantic.
- Toda herramienta tiene prueba.
- Todo acceso a datos verifica propiedad: un recurso ajeno responde 404.
- Ninguna acción con efectos se ejecuta sin aprobación real.
- Sin pruebas en verde no se integra.

**Ramas y commits**

- `main` siempre ejecutable; trabajo en ramas `claseNN/descripcion`.
- Commits con prefijo: `feat`, `fix`, `test`, `docs`, `refactor`, `chore`, y el módulo entre paréntesis: `feat(api): v1 health y conversaciones`.
- Al cerrar cada laboratorio: un commit, una prueba que falla a propósito documentada y la evidencia en el README del módulo.

**CI** (desde la clase 12): `ruff`, `pytest`, auditoría de dependencias y escaneo de secretos en cada cambio. Si algo falla, no se integra.

---

## Hoja de ruta

| # | Clase | Entregable principal |
|---|---|---|
| 1 | De un LLM a un agente funcional | `ai/agents/basic_agent.py`, `ai/tools/requests.py` |
| 2 | RAG clásico, RAG agéntico e ingesta | `ai/rag/` |
| 3 | LangGraph: grafos, estado y memoria | `ai/graphs/` |
| 4 | MCP: tools, resources y prompts | `ai/mcp_server/` |
| 5 | Multiagente y A2A | `ai/agents/supervisor.py`, `ai/a2a_agent/` |
| 6 | Evaluación, observabilidad y seguridad (**Hito I**) | `ai/evals/`, `docs/ai_contracts.md` |
| 7 | FastAPI y contratos HTTP | `backend/app/`, `contracts/openapi.json` |
| 8 | PostgreSQL, pgvector y propiedad de datos | `backend/app/models/`, `migrations/` |
| 9 | Procesos asíncronos, SSE y estados | `backend/app/api/stream.py`, `contracts/events.schema.json` |
| 10 | Autenticación, autorización y Policy Engine | `backend/app/security/` |
| 11 | El backend como cliente de MCP y A2A | `backend/app/integrations/` |
| 12 | Contenedores, CI y observabilidad (**Hito II**) | `infrastructure/`, `.github/workflows/ci.yml` |
| 13 | React y JavaScript: interfaz y contratos | `frontend/src/features/chat/`, `api/client.js` |
| 14 | Streaming en la interfaz | `frontend/src/hooks/useRunStream.js` |
| 15 | Documentos, evidencia y citas | `frontend/src/features/documents/` |
| 16 | Human-in-the-loop | `frontend/src/features/approvals/` |
| 17 | Pruebas de frontend, accesibilidad y seguridad | `frontend/tests/` |
| 18 | Despliegue en staging y defensa (**Hito III**) | `docs/deployment.md`, `docs/limitations.md` |

---

## Lo que este proyecto no cubre

SLA contractual, alta disponibilidad, recuperación ante desastres multirregión, operación 24/7, certificaciones de seguridad, OAuth2/OIDC completo con proveedor externo y escalado horizontal del servicio de ejecución. Declararlo es parte de la competencia, no una falla.
