"""Carga la configuración de OpenRouter desde secrets/llm.env."""
import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_openrouter import ChatOpenRouter

ROOT = Path(__file__).resolve().parents[2]
load_dotenv(ROOT / "secrets" / "llm.env")

def get_chat_model():
    api_key = os.getenv("OPENROUTER_API_KEY", "")
    model_name = os.getenv("LLM_MODEL", "")
    if not api_key or api_key == "REEMPLAZAR":
        raise ValueError("Configura OPENROUTER_API_KEY en secrets/llm.env")
    if not model_name or model_name.startswith("REEMPLAZAR"):
        raise ValueError("Configura LLM_MODEL en secrets/llm.env")
    return ChatOpenRouter(model=model_name, temperature=0)
