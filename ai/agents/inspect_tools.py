"""Diapositiva: observar llamadas y resultados de herramientas."""
from langchain_core.messages import ToolMessage
from ai.agents.basic_agent import agent

result = agent.invoke({
    "messages": [{"role": "user", "content": "Consulta SOL-014 y calcula su puntuación"}]
})
for message in result["messages"]:
    if getattr(message, "tool_calls", None):
        print("Herramientas solicitadas:", message.tool_calls)
    if isinstance(message, ToolMessage):
        print("Resultado de herramienta:", message.name, message.content)
print("Respuesta final:", result["messages"][-1].content)
