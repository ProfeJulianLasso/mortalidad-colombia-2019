"""Comparación apilada de defunciones por sexo en cada departamento."""

from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go

from src.viz import theme

DATA_SOURCE = "DANE — Estadísticas Vitales 2019."

_SEX_ORDER = ["Hombre", "Mujer", "Indeterminado"]


def create(deaths: pd.DataFrame) -> go.Figure:
    """Barras apiladas Hombre/Mujer (e Indeterminado) por departamento."""
    pivot = (
        deaths.groupby(["DEPARTAMENTO", "SEXO_LABEL"])
        .size()
        .unstack(fill_value=0)
    )
    pivot["total"] = pivot.sum(axis=1)
    pivot = pivot.sort_values("total", ascending=True)

    fig = go.Figure()
    for sex in _SEX_ORDER:
        if sex not in pivot.columns:
            continue
        fig.add_trace(
            go.Bar(
                x=pivot[sex],
                y=pivot.index,
                name=sex,
                orientation="h",
                marker=dict(
                    color=theme.SEX_COLORS[sex],
                    line=dict(color=theme.BACKGROUND, width=0.4),
                ),
                hovertemplate=(
                    f"<b>%{{y}}</b><br>{sex}: %{{x:,}}<extra></extra>"
                ),
            )
        )

    fig.update_layout(barmode="stack")
    theme.apply_layout(
        fig,
        title="Defunciones por sexo y departamento — Colombia, 2019",
        height=720,
        show_legend=True,
        legend_orientation="h",
    )
    fig.update_xaxes(title="Defunciones registradas", tickformat=",d")
    fig.update_yaxes(title="", automargin=True)
    theme.annotate_source(fig, DATA_SOURCE)
    return fig
