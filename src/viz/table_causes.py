"""Tabla con las diez principales causas de muerte según CIE-10."""

from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go

from src.viz import theme

DATA_SOURCE = "DANE — Estadísticas Vitales 2019, catálogo CIE-10."


def create(
    deaths: pd.DataFrame,
    department: str | None = None,
    n: int = 10,
) -> go.Figure:
    """Tabla Plotly con las ``n`` causas más frecuentes para el alcance dado."""
    scope = deaths if department is None else deaths[deaths["DEPARTAMENTO"] == department]
    top = (
        scope.groupby(["COD_MUERTE", "DESC_MUERTE"])
        .size()
        .reset_index(name="total")
        .sort_values("total", ascending=False)
        .head(n)
    )

    scope_label = department if department else "Colombia"
    title = f"Diez principales causas de muerte — {scope_label}, 2019"
    formatted_totals = [f"{value:,}" for value in top["total"]]

    fig = go.Figure(
        go.Table(
            columnwidth=[80, 380, 100],
            header=dict(
                values=["<b>Código CIE-10</b>", "<b>Causa de muerte</b>", "<b>Defunciones</b>"],
                fill_color=theme.PRIMARY,
                font=dict(family=theme.BODY_FONT, color=theme.BACKGROUND, size=12),
                align=["left", "left", "right"],
                height=32,
            ),
            cells=dict(
                values=[top["COD_MUERTE"], top["DESC_MUERTE"], formatted_totals],
                fill_color=[[theme.BACKGROUND, theme.GRID] * (len(top) // 2 + 1)],
                align=["left", "left", "right"],
                font=dict(family=theme.BODY_FONT, color=theme.NEUTRAL_DARK, size=11),
                height=28,
            ),
        )
    )

    theme.apply_layout(fig, title=title, height=440, show_legend=False)
    theme.annotate_source(fig, DATA_SOURCE)
    return fig
