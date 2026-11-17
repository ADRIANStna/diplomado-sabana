"""Diapositiva: bind_tools muestra tool_calls, pero no las ejecuta."""
from ai.config.model import get_chat_model
from ai.tools.agent_tools import consultar_solicitud, calcular_puntuacion

model = get_chat_model().bind_tools([consultar_solicitud, calcular_puntuacion])
response = model.invoke("Consulta SOL-014 y calcula su puntuación.")
print("Llamadas solicitadas:", response.tool_calls)
print("Respuesta textual:", response.content)
