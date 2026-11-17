"""Lectura de solicitudes desde el CSV del proyecto (sesión 1)."""
import csv
from pathlib import Path

CSV_PATH = Path(__file__).resolve().parents[2] / "data" / "solicitudes.csv"

def buscar_solicitud(codigo: str) -> dict | None:
    with CSV_PATH.open(encoding="utf-8", newline="") as archivo:
        for fila in csv.DictReader(archivo):
            if fila["codigo"] == codigo:
                return {
                    "codigo": fila["codigo"],
                    "impacto": int(fila["impacto"]),
                    "urgencia": int(fila["urgencia"]),
                }
    return None
