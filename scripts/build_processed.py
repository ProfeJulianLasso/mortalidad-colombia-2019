"""Genera los datasets procesados que consume la aplicación Dash.

Se ejecuta una sola vez en desarrollo. Su salida son los archivos en
``data/processed/`` que se commiten al repositorio para que el despliegue
en Render no tenga que abrir los Excel originales al arrancar.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.data import loader, transformer  # noqa: E402
from src.data.constants import (  # noqa: E402
    ANALYSIS_YEAR,
    DEATH_CODES_FILE,
    DEATHS_FILE,
    DEPARTMENTS_FILE,
    DIVIPOLA_FILE,
    ENRICHED_DEATHS_FILE,
    PROCESSED_DIR,
    SUMMARY_FILE,
)


def main() -> None:
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    print("Cargando archivos del DANE...")
    deaths = loader.load_deaths(DEATHS_FILE)
    codes = loader.load_death_codes(DEATH_CODES_FILE)
    divipola = loader.load_divipola(DIVIPOLA_FILE)
    cause_dictionary = loader.build_cause_dictionary(codes)

    print(f"  Defunciones: {len(deaths):,}")
    print(f"  Códigos CIE-10 en diccionario: {len(cause_dictionary):,}")
    print(f"  Municipios en DIVIPOLA: {len(divipola):,}")

    print("Enriqueciendo dataset...")
    enriched = transformer.enrich_deaths(deaths, divipola, cause_dictionary)

    department_catalog = transformer.build_department_catalog(divipola)

    print(f"Escribiendo {ENRICHED_DEATHS_FILE.name}...")
    enriched.to_parquet(ENRICHED_DEATHS_FILE, index=False)

    print(f"Escribiendo {DEPARTMENTS_FILE.name}...")
    department_catalog.to_parquet(DEPARTMENTS_FILE, index=False)

    report = transformer.integrity_report(enriched)
    report["año_analisis"] = ANALYSIS_YEAR
    SUMMARY_FILE.write_text(json.dumps(report, ensure_ascii=False, indent=2))

    print("\nResumen de integridad:")
    for key, value in report.items():
        print(f"  {key}: {value}")

    print(f"\nProcesamiento completo. Salida en {PROCESSED_DIR}")


if __name__ == "__main__":
    main()
