"""Inventario inicial de los Excel del DANE.

Genera un Markdown con columnas, dtypes y conteo de filas de cada archivo.
Se ejecuta una sola vez para conocer la estructura real antes de construir
los loaders y transformers. El archivo de salida queda fuera del repo
(ver .gitignore: notas-inventario.md).
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

RAW_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"
OUTPUT = Path(__file__).resolve().parent.parent / "notas-inventario.md"


def describe_excel(path: Path) -> str:
    lines: list[str] = [f"## {path.name}", ""]

    sheets = pd.ExcelFile(path).sheet_names
    lines.append(f"- Hojas: {sheets}")
    lines.append("")

    for sheet in sheets:
        df = pd.read_excel(path, sheet_name=sheet, dtype=str)
        lines.append(f"### Hoja `{sheet}`")
        lines.append("")
        lines.append(f"- Filas: {len(df):,}")
        lines.append(f"- Columnas: {len(df.columns)}")
        lines.append("")
        lines.append("| Columna | Tipo inferido | No nulos | Ejemplo |")
        lines.append("|---|---|---:|---|")
        for col in df.columns:
            non_null = df[col].notna().sum()
            sample = df[col].dropna().head(1).tolist()
            sample_str = str(sample[0]) if sample else ""
            sample_str = sample_str.replace("|", "\\|")[:60]
            lines.append(f"| `{col}` | str | {non_null:,} | {sample_str} |")
        lines.append("")

    return "\n".join(lines)


def main() -> None:
    sections: list[str] = ["# Inventario de columnas — datos DANE 2019", ""]

    for path in sorted(RAW_DIR.glob("*.xlsx")):
        sections.append(describe_excel(path))
        sections.append("---")
        sections.append("")

    OUTPUT.write_text("\n".join(sections), encoding="utf-8")
    print(f"Inventario escrito en {OUTPUT}")


if __name__ == "__main__":
    main()
