"""Diapositiva: primera invocación a un modelo."""
from ai.config.model import get_chat_model

model = get_chat_model()
response = model.invoke("Hola. Preséntate en una frase.")
print(response.content)
