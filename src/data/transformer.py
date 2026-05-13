"""Transformaciones de datos crudos a un dataset enriquecido y agregados.

El dataset enriquecido es la única fuente de verdad para la aplicación
Dash. A partir de él se generan en memoria las agregaciones que alimentan
cada visualización, lo que permite que los callbacks filtren por
departamento sin necesidad de mantener parquets duplicados.
"""

from __future__ import annotations

import pandas as pd

from src.data import age_groups
from src.data.constants import MONTH_LABELS, SEX_LABELS


def build_department_catalog(divipola: pd.DataFrame) -> pd.DataFrame:
    """Resumen único de departamentos con su código DANE y nombre."""
    catalog = (
        divipola[["COD_DEPARTAMENTO", "DEPARTAMENTO"]]
        .drop_duplicates()
        .sort_values("DEPARTAMENTO")
        .reset_index(drop=True)
    )
    return catalog


def enrich_deaths(
    deaths: pd.DataFrame,
    divipola: pd.DataFrame,
    cause_dictionary: dict[str, str],
) -> pd.DataFrame:
    """Combina las defunciones con los lookups necesarios para la app."""
    municipality_lookup = divipola[
        ["COD_DANE", "DEPARTAMENTO", "MUNICIPIO"]
    ].drop_duplicates(subset=["COD_DANE"])

    enriched = deaths.merge(municipality_lookup, on="COD_DANE", how="left")

    enriched["SEXO_LABEL"] = (
        enriched["SEXO"].map(SEX_LABELS).fillna("Sin información")
    )
    enriched["MES_NOMBRE"] = enriched["MES"].map(MONTH_LABELS)
    enriched["CICLO_VITAL"] = enriched["GRUPO_EDAD1"].apply(
        lambda code: age_groups.categorize(int(code) if pd.notna(code) else None)
    )
    enriched["RANGO_EDAD"] = enriched["CICLO_VITAL"].map(age_groups.LIFE_STAGE_RANGE)

    enriched["DESC_MUERTE"] = enriched["COD_MUERTE"].map(cause_dictionary)
    missing_four_char = enriched["DESC_MUERTE"].isna()
    enriched.loc[missing_four_char, "DESC_MUERTE"] = (
        enriched.loc[missing_four_char, "COD_MUERTE"].str[:3].map(cause_dictionary)
    )
    enriched["DESC_MUERTE"] = enriched["DESC_MUERTE"].fillna("Causa no clasificada")

    keep_columns = [
        "COD_DANE",
        "COD_DEPARTAMENTO",
        "DEPARTAMENTO",
        "MUNICIPIO",
        "MES",
        "MES_NOMBRE",
        "SEXO",
        "SEXO_LABEL",
        "GRUPO_EDAD1",
        "CICLO_VITAL",
        "RANGO_EDAD",
        "COD_MUERTE",
        "DESC_MUERTE",
        "MANERA_MUERTE",
    ]
    return enriched[keep_columns]


def integrity_report(enriched: pd.DataFrame) -> dict[str, object]:
    """Resumen numérico para validar el procesamiento."""
    total = len(enriched)
    no_department = enriched["DEPARTAMENTO"].isna().sum()
    no_cause = (enriched["DESC_MUERTE"] == "Causa no clasificada").sum()
    return {
        "total_defunciones": int(total),
        "departamentos_distintos": int(enriched["DEPARTAMENTO"].dropna().nunique()),
        "municipios_distintos": int(enriched["MUNICIPIO"].dropna().nunique()),
        "filas_sin_departamento": int(no_department),
        "filas_sin_causa": int(no_cause),
        "porcentaje_homicidios": round(
            (enriched["MANERA_MUERTE"] == "Homicidio").mean() * 100, 2
        ),
        "total_por_manera": enriched["MANERA_MUERTE"]
        .value_counts(dropna=False)
        .to_dict(),
    }
