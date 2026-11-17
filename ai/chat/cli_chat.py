"""Diapositiva: chat de terminal con historial en memoria."""
from langchain_core.messages import SystemMessage, HumanMessage
from ai.config.model import get_chat_model

model = get_chat_model()
history = [SystemMessage(content="Eres un asistente ServiceDesk.")]

while True:
    question = input("Usuario: ").strip()
    if question.lower() == "salir":
        break
    if not question:
        continue
    history.append(HumanMessage(content=question))
    response = model.invoke(history)
    print("Asistente:", response.content)
    history.append(response)
