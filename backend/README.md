# Backend

API de Agéntica Aplicada, construida con FastAPI. Usa [uv](https://docs.astral.sh/uv/) para gestionar Python y las dependencias.

## Instalación

Desde la carpeta `backend/`:

```powershell
uv sync
Copy-Item .env.example .env
```

## Ejecución

```powershell
uv run fastapi dev app/main.py
```

- Verificación de estado: <http://127.0.0.1:8000/api/health>
- Documentación interactiva: <http://127.0.0.1:8000/docs>

## Pruebas

```powershell
uv run pytest
```

## Dependencias

```powershell
uv add <paquete>        # dependencia de la aplicación
uv add --dev <paquete>  # dependencia de desarrollo
```
