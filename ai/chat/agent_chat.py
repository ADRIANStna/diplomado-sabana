"""Diapositiva: chat agéntico con historial entre turnos."""
from langchain_core.messages import HumanMessage
from ai.agents.basic_agent import agent

history = []
while True:
    question = input("Usuario: ").strip()
    if question.lower() == "salir":
        break
    if not question:
        continue
    history.append(HumanMessage(content=question))
    result = agent.invoke({"messages": history})
    history = result["messages"]
    print("Agente:", history[-1].content)
