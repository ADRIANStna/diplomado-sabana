# Steering · convenciones del proyecto

Reglas que aplican a los tres módulos. Se actualiza al cierre de cada clase; cada cambio queda en el commit de esa clase.

## Principio

El modelo propone; el backend valida, decide y ejecuta. Ningún control de permisos, aprobación o estado depende del agente ni de la interfaz.

## Reglas que bloquean una entrega

- Sin secretos en el código, en los prompts ni en los logs. Las variables viven en `.env` (raíz, no versionado) y se documentan en `.env.example` sin valores reales.
- Toda entrada y salida de la API se valida con Pydantic.
- Toda herramienta tiene prueba.
- Todo acceso a datos verifica propiedad: un recurso ajeno responde 404.
- Ninguna acción con efectos se ejecuta sin aprobación real.
- Sin pruebas en verde no se integra.
- Solo datos sintéticos (Ley 1581 de 2012).

## Fronteras entre módulos

1. `backend/` solo importa `ai.engine.build_engine()` y `contracts/`; nunca nodos internos de `ai/`.
2. `ai/` no importa nada de `backend/` ni abre conexiones a la base de datos; recibe sus dependencias por inyección.
3. Ninguna escritura ocurre dentro de `ai/`.
4. Cada lado se prueba sin el otro: `ai/` con implementaciones locales de los puertos; `backend/` con `StubAgentEngine`.
5. Un cambio en `contracts/` requiere acuerdo de los tres docentes y un registro en `docs/decisions/`.

## Python

- Python 3.12, fijado en `.python-version` de `ai/` y `backend/`.
- Entornos y dependencias con uv: `uv add`, `uv add --dev`, `uv sync`, `uv run`. No se usan `pip install`, `python -m venv` ni `requirements.txt`.
- Cada módulo tiene su `pyproject.toml` y su `uv.lock`. Los archivos de bloqueo se versionan y no se actualizan durante el curso sin acuerdo docente.
- `ai/` no se empaqueta: el paquete `ai` se importa desde la raíz del repositorio (`uv run --project ai python -m ai.<modulo>`).

## API

- Prefijo `/v1`. La aplicación se construye con `create_app()`.
- Formato de error único: `{"error": {"code", "message", "request_id"}}`.
- Estados del run: `queued → running → waiting_for_approval → running → completed`; `failed` y `canceled` desde cualquier estado activo. Un estado terminal no se vuelve a ejecutar.

## Git

- `main` siempre ejecutable; trabajo en ramas `claseNN/descripcion` (por ejemplo `clase07/fastapi-contratos`).
- Commits con prefijo y módulo: `feat(api): v1 health y conversaciones`. Prefijos: `feat`, `fix`, `test`, `docs`, `refactor`, `chore`.
- Al cerrar cada laboratorio: un commit, una prueba que falla a propósito documentada y la evidencia en el README del módulo.
- Las carpetas vacías llevan `.gitkeep` para que aparezcan en GitHub; se borra cuando la carpeta recibe su primer archivo.

## Registro de cambios de este documento

| Clase | Cambio |
|---|---|
| 0 | Versión inicial: reglas base, fronteras, uv y Python 3.12. |
