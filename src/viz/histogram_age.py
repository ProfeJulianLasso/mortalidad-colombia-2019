"""Distribución de defunciones por etapa del ciclo vital."""

from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go

from src.data.age_groups import LIFE_STAGE_ORDER, LIFE_STAGE_RANGE
from src.viz import theme

DATA_SOURCE = (
    "DANE — Estadísticas Vitales 2019. Agrupación por ciclo vital según los "
    "códigos GRUPO_EDAD1 del DANE."
)


def create(deaths: pd.DataFrame, department: str | None = None) -> go.Figure:
    """Histograma ordenado por etapa del ciclo vital."""
    scope = deaths if department is None else deaths[deaths["DEPARTAMENTO"] == department]
    counts = scope.groupby("CICLO_VITAL").size().reindex(LIFE_STAGE_ORDER, fill_value=0)

    labels = [f"{stage}<br><span style='font-size:10px'>{LIFE_STAGE_RANGE[stage]}</span>"
              for stage in LIFE_STAGE_ORDER]

    scope_label = department if department else "Colombia"
    title = f"Defunciones por etapa del ciclo vital — {scope_label}, 2019"

    fig = go.Figure(
        go.Bar(
            x=labels,
            y=counts.values,
            marker=dict(color=theme.PRIMARY, line=dict(color=theme.NEUTRAL_DARK, width=0.4)),
            text=[f"{value:,}" for value in counts.values],
            textposition="outside",
            textfont=dict(family=theme.BODY_FONT, size=10, color=theme.NEUTRAL_DARK),
            hovertemplate="<b>%{x}</b><br>Defunciones: %{y:,}<extra></extra>",
            customdata=LIFE_STAGE_ORDER,
        )
    )

    theme.apply_layout(fig, title=title, height=480, show_legend=False)
    fig.update_xaxes(title="Etapa del ciclo vital", tickangle=-30)
    fig.update_yaxes(title="Defunciones registradas", tickformat=",d")
    theme.annotate_source(fig, DATA_SOURCE)
    return fig
