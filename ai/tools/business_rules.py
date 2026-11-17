"""Funciones Python independientes del modelo de lenguaje."""
from ai.data.requests import buscar_solicitud

def consultar_solicitud(codigo: str) -> dict:
    solicitud = buscar_solicitud(codigo)
    if solicitud is None:
        return {"error": "solicitud_no_encontrada"}
    return solicitud

def calcular_puntuacion(impacto: int, urgencia: int) -> int:
    if not (1 <= impacto <= 3 and 1 <= urgencia <= 3):
        raise ValueError("Impacto y urgencia deben estar entre 1 y 3")
    return impacto * urgencia
