"""Diapositiva: create_agent con dos herramientas y límite de llamadas."""
from langchain.agents import create_agent
from langchain.agents.middleware import ToolCallLimitMiddleware
from ai.config.model import get_chat_model
from ai.tools.agent_tools import consultar_solicitud, calcular_puntuacion

agent = create_agent(
    model=get_chat_model(),
    tools=[consultar_solicitud, calcular_puntuacion],
    system_prompt=(
        "Eres un asistente ServiceDesk. Consulta las solicitudes con herramientas. "
        "Calcula puntuaciones con la herramienta correspondiente. "
        "No inventes datos ni modifiques solicitudes."
    ),
    middleware=[ToolCallLimitMiddleware(run_limit=4, exit_behavior="error")],
)
