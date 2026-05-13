"""Mapeo de la variable GRUPO_EDAD1 del DANE a etapas del ciclo vital.

El DANE codifica la edad al fallecimiento en grupos numéricos de 0 a 29.
La actividad solicita agruparlos en categorías de ciclo vital con un rango
de edad aproximado para facilitar la lectura demográfica de los datos.
"""

from __future__ import annotations

from typing import Final

LIFE_STAGE_ORDER: Final[list[str]] = [
    "Mortalidad neonatal",
    "Mortalidad infantil",
    "Primera infancia",
    "Niñez",
    "Adolescencia",
    "Juventud",
    "Adultez temprana",
    "Adultez intermedia",
    "Vejez",
    "Longevidad",
    "Edad desconocida",
]

LIFE_STAGE_RANGE: Final[dict[str, str]] = {
    "Mortalidad neonatal": "Menor de 1 mes",
    "Mortalidad infantil": "1 a 11 meses",
    "Primera infancia": "1 a 4 años",
    "Niñez": "5 a 14 años",
    "Adolescencia": "15 a 19 años",
    "Juventud": "20 a 29 años",
    "Adultez temprana": "30 a 44 años",
    "Adultez intermedia": "45 a 59 años",
    "Vejez": "60 a 84 años",
    "Longevidad": "85 a 100 años o más",
    "Edad desconocida": "Sin información",
}

_CODE_TO_STAGE: Final[dict[int, str]] = {}
for code in range(0, 5):
    _CODE_TO_STAGE[code] = "Mortalidad neonatal"
for code in range(5, 7):
    _CODE_TO_STAGE[code] = "Mortalidad infantil"
for code in range(7, 9):
    _CODE_TO_STAGE[code] = "Primera infancia"
for code in range(9, 11):
    _CODE_TO_STAGE[code] = "Niñez"
_CODE_TO_STAGE[11] = "Adolescencia"
for code in range(12, 14):
    _CODE_TO_STAGE[code] = "Juventud"
for code in range(14, 17):
    _CODE_TO_STAGE[code] = "Adultez temprana"
for code in range(17, 20):
    _CODE_TO_STAGE[code] = "Adultez intermedia"
for code in range(20, 25):
    _CODE_TO_STAGE[code] = "Vejez"
for code in range(25, 29):
    _CODE_TO_STAGE[code] = "Longevidad"
_CODE_TO_STAGE[29] = "Edad desconocida"


def categorize(code: int | None) -> str:
    """Convierte un código DANE de GRUPO_EDAD1 en su etapa del ciclo vital."""
    if code is None:
        return "Edad desconocida"
    return _CODE_TO_STAGE.get(int(code), "Edad desconocida")


def life_stage_with_range(stage: str) -> str:
    """Devuelve la etapa concatenada con el rango aproximado para tooltips."""
    return f"{stage} ({LIFE_STAGE_RANGE[stage]})"
