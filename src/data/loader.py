"""Carga normalizada de los tres archivos de entrada del DANE.

Cada loader devuelve un DataFrame con columnas y tipos predecibles. Los
códigos administrativos siempre se preservan como cadenas con sus ceros a
la izquierda; los uniones posteriores dependen de esto.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


def load_deaths(path: Path) -> pd.DataFrame:
    """Carga el Anexo 1 (defunciones no fetales 2019).

    Normaliza los códigos de departamento (2 chars) y municipio (3 chars) y
    convierte a entero solo las variables numéricas que se usan como tales.
    """
    df = pd.read_excel(path, sheet_name="No_Fetales_2019", dtype=str)

    df["COD_DEPARTAMENTO"] = df["COD_DEPARTAMENTO"].str.zfill(2)
    df["COD_MUNICIPIO"] = df["COD_MUNICIPIO"].str.zfill(3)
    df["COD_DANE"] = df["COD_DEPARTAMENTO"] + df["COD_MUNICIPIO"]

    df["MES"] = pd.to_numeric(df["MES"], errors="coerce").astype("Int64")
    df["SEXO"] = pd.to_numeric(df["SEXO"], errors="coerce").astype("Int64")
    df["GRUPO_EDAD1"] = pd.to_numeric(df["GRUPO_EDAD1"], errors="coerce").astype(
        "Int64"
    )

    df["COD_MUERTE"] = df["COD_MUERTE"].str.strip().str.upper()

    return df


def load_death_codes(path: Path) -> pd.DataFrame:
    """Carga el Anexo 2 (catálogo CIE-10 de causas de muerte).

    El archivo trae 8 filas de metadata antes de la cabecera real. Tras
    leerlo, las columnas se renombran a slugs estables.
    """
    df = pd.read_excel(path, sheet_name="Final", header=8, dtype=str)
    df.columns = [
        "capitulo_num",
        "capitulo_nombre",
        "cod_3",
        "desc_3",
        "cod_4",
        "desc_4",
    ]
    for column in df.columns:
        df[column] = df[column].astype("string").str.strip()
    df = df.dropna(subset=["cod_3"]).reset_index(drop=True)
    return df


def build_cause_dictionary(codes: pd.DataFrame) -> dict[str, str]:
    """Construye un diccionario {código CIE-10: descripción}.

    Privilegia el código de 4 caracteres y cae al de 3 caracteres si el
    primero no está disponible. Esto cubre las dos longitudes presentes en
    el campo COD_MUERTE del Anexo 1.
    """
    dictionary: dict[str, str] = {}

    three_char = codes.dropna(subset=["cod_3", "desc_3"])
    for _, row in three_char.iterrows():
        code = str(row["cod_3"]).strip().upper()
        if code and code not in dictionary:
            dictionary[code] = str(row["desc_3"]).strip()

    four_char = codes.dropna(subset=["cod_4", "desc_4"])
    for _, row in four_char.iterrows():
        code = str(row["cod_4"]).strip().upper()
        if code:
            dictionary[code] = str(row["desc_4"]).strip()

    return dictionary


def load_divipola(path: Path) -> pd.DataFrame:
    """Carga la división político-administrativa colombiana.

    Devuelve un DataFrame de municipios con código DANE de 5 caracteres,
    código y nombre de departamento, y código y nombre del municipio.
    """
    df = pd.read_excel(path, sheet_name="Hoja1", dtype=str)
    df["COD_DEPARTAMENTO"] = df["COD_DEPARTAMENTO"].str.zfill(2)
    df["COD_MUNICIPIO"] = df["COD_MUNICIPIO"].str.zfill(3)
    df["COD_DANE"] = df["COD_DEPARTAMENTO"] + df["COD_MUNICIPIO"]

    cleaned = df[
        ["COD_DANE", "COD_DEPARTAMENTO", "DEPARTAMENTO", "COD_MUNICIPIO", "MUNICIPIO"]
    ].copy()
    cleaned["DEPARTAMENTO"] = cleaned["DEPARTAMENTO"].str.title()
    cleaned["MUNICIPIO"] = cleaned["MUNICIPIO"].str.title()
    return cleaned
