"""Las dos herramientas de LangChain de la sesión 1."""
from langchain.tools import tool
from ai.tools.business_rules import (
    consultar_solicitud as consultar_datos,
    calcular_puntuacion as puntuar,
)
from ai.tools.schemas import PuntuacionInput

@tool
def consultar_solicitud(codigo: str) -> dict:
    """Consulta el impacto y la urgencia de una solicitud por su código."""
    return consultar_datos(codigo)

@tool(args_schema=PuntuacionInput)
def calcular_puntuacion(impacto: int, urgencia: int) -> dict:
    """Calcula una puntuación usando impacto multiplicado por urgencia."""
    return {"puntuacion": puntuar(impacto, urgencia)}
