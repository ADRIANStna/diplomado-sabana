"""Pruebas de consulta, cálculo y validación de la sesión 1."""
import pytest
from pydantic import ValidationError
from ai.tools.business_rules import consultar_solicitud, calcular_puntuacion
from ai.tools.schemas import PuntuacionInput

def test_consulta_solicitud():
    assert consultar_solicitud("SOL-014") == {
        "codigo": "SOL-014", "impacto": 3, "urgencia": 2
    }

def test_codigo_inexistente():
    assert consultar_solicitud("SOL-999") == {"error": "solicitud_no_encontrada"}

def test_puntuacion_correcta():
    assert calcular_puntuacion(3, 2) == 6

def test_impacto_invalido():
    with pytest.raises(ValueError):
        calcular_puntuacion(9, 2)

def test_esquema_invalido():
    with pytest.raises(ValidationError):
        PuntuacionInput(impacto=9, urgencia=2)
