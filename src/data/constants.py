"""Constantes compartidas: rutas, mapeos de dominio y etiquetas en español."""

from __future__ import annotations

from pathlib import Path
from typing import Final

PROJECT_ROOT: Final[Path] = Path(__file__).resolve().parents[2]
DATA_DIR: Final[Path] = PROJECT_ROOT / "data"
RAW_DIR: Final[Path] = DATA_DIR / "raw"
PROCESSED_DIR: Final[Path] = DATA_DIR / "processed"
ASSETS_DIR: Final[Path] = PROJECT_ROOT / "assets"

DEATHS_FILE: Final[Path] = RAW_DIR / "Anexo1.NoFetal2019_CE_15-03-23.xlsx"
DEATH_CODES_FILE: Final[Path] = RAW_DIR / "Anexo2.CodigosDeMuerte_CE_15-03-23.xlsx"
DIVIPOLA_FILE: Final[Path] = RAW_DIR / "Divipola_CE_.xlsx"
GEOJSON_FILE: Final[Path] = ASSETS_DIR / "colombia-departamentos.geo.json"

ENRICHED_DEATHS_FILE: Final[Path] = PROCESSED_DIR / "deaths_enriched.parquet"
DEPARTMENTS_FILE: Final[Path] = PROCESSED_DIR / "departments.parquet"
SUMMARY_FILE: Final[Path] = PROCESSED_DIR / "summary.json"

SEX_LABELS: Final[dict[int, str]] = {
    1: "Hombre",
    2: "Mujer",
    3: "Indeterminado",
}

MONTH_LABELS: Final[dict[int, str]] = {
    1: "Enero",
    2: "Febrero",
    3: "Marzo",
    4: "Abril",
    5: "Mayo",
    6: "Junio",
    7: "Julio",
    8: "Agosto",
    9: "Septiembre",
    10: "Octubre",
    11: "Noviembre",
    12: "Diciembre",
}

VIOLENT_DEATH_PREFIX: Final[str] = "X95"

ANALYSIS_YEAR: Final[int] = 2019
