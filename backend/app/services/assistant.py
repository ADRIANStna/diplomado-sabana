from app.schemas.run import RunRead


def generate_reply(history: list[RunRead], message: str) -> str:
    """Simula la respuesta del asistente. Aquí se conectará la capa de IA real."""
    return f"[Simulación] Respuesta {len(history) + 1} a: {message}"
