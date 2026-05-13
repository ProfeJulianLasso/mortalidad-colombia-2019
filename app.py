"""Punto de entrada de la aplicación Dash.

Carga el dataset enriquecido en memoria al iniciar el servidor, construye las
figuras iniciales con alcance nacional y registra los callbacks que las
recalculan cuando el usuario filtra por departamento.
"""

from __future__ import annotations

import json
import os
from typing import Final

import pandas as pd
from dash import Dash, Input, Output

from src.data.constants import (
    DEPARTMENTS_FILE,
    ENRICHED_DEATHS_FILE,
    GEOJSON_FILE,
)
from src.layout import main as main_layout
from src.viz import (
    bar_violent_cities,
    histogram_age,
    line_monthly,
    map_departments,
    pie_low_mortality,
    stacked_sex_dept,
    table_causes,
)

APP_TITLE: Final[str] = "Mortalidad en Colombia, 2019"

deaths_df = pd.read_parquet(ENRICHED_DEATHS_FILE)
departments_df = pd.read_parquet(DEPARTMENTS_FILE)
with GEOJSON_FILE.open(encoding="utf-8") as fh:
    geojson_data = json.load(fh)


def _resolve_department(value: str) -> str | None:
    return None if value == main_layout.ALL_DEPARTMENTS_LABEL else value


def _build_initial_figures():
    return {
        "map": map_departments.create(deaths_df, geojson_data),
        "line": line_monthly.create(deaths_df),
        "violent": bar_violent_cities.create(deaths_df),
        "pie": pie_low_mortality.create(deaths_df),
        "table": table_causes.create(deaths_df),
        "stacked": stacked_sex_dept.create(deaths_df),
        "histogram": histogram_age.create(deaths_df),
    }


app = Dash(__name__, title=APP_TITLE, update_title=None)
server = app.server

department_options = main_layout.build_department_options(
    sorted(departments_df["DEPARTAMENTO"].dropna().unique().tolist())
)
app.layout = main_layout.render(department_options, _build_initial_figures())


@app.callback(
    Output("graph-line", "figure"),
    Output("graph-violent", "figure"),
    Output("graph-pie", "figure"),
    Output("graph-table", "figure"),
    Output("graph-histogram", "figure"),
    Input("department-filter", "value"),
)
def refresh_filtered_figures(department_value: str):
    department = _resolve_department(department_value)
    return (
        line_monthly.create(deaths_df, department),
        bar_violent_cities.create(deaths_df, department),
        pie_low_mortality.create(deaths_df, department),
        table_causes.create(deaths_df, department),
        histogram_age.create(deaths_df, department),
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8050"))
    app.run(host="0.0.0.0", port=port, debug=False)
