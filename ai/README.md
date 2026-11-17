# ai · Módulo I: motor agéntico

Clases 1–6 · Docente: Oscar Rodríguez · Hito I: motor agéntico evaluado (clase 6).

El motor se expone al resto del sistema solo a través de `ai.engine.build_engine()` y de los puertos definidos en [`contracts/`](../contracts/). No importa nada de `backend/`, no abre conexiones a la base de datos y no escribe: propone.

## Puesta en marcha de la sesión 1

Desde la raíz del repositorio, usando el entorno documentado en `README.md`:

```bash
python -m pip install -r requirements.txt
python -m ai.chat.agent_chat
python -m pytest -q tests/test_business_rules.py
```

La rama `feat/agente` contiene únicamente el código de la primera clase. Más
adelante se incorporarán `ai/engine.py`, RAG, grafos y conectores.

## Mientras tanto

Hasta que exista `build_engine()`, el backend responde con una simulación en `generate_reply(history, message)` ([`backend/app/services/assistant.py`](../backend/app/services/assistant.py)), que pasará a ser `StubAgentEngine`.

## Laboratorios

| Clase | Entregable | Estado | Evidencia |
|---|---|---|---|
| 1 | chat, `agents/basic_agent.py`, `tools/`, lectura CSV y pruebas | implementado | `tests/test_business_rules.py` |
| 2 | `rag/` | pendiente | |
| 3 | `graphs/` | pendiente | |
| 4 | `mcp_server/` | pendiente | |
| 5 | `agents/supervisor.py`, `a2a_agent/` | pendiente | |
| 6 | `evals/`, `engine.py`, `docs/ai_contracts.md` | pendiente | |
