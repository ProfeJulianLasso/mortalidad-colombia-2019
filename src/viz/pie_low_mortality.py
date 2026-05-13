"""Distribución de las 10 ciudades con menor número de defunciones."""

from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go

from src.viz import theme


def create(
    deaths: pd.DataFrame,
    department: str | None = None,
    n: int = 10,
) -> go.Figure:
    """Pie con los ``n`` municipios con menor mortalidad (>0 muertes)."""
    scope = deaths if department is None else deaths[deaths["DEPARTAMENTO"] == department]
    counts = (
        scope.groupby(["MUNICIPIO", "DEPARTAMENTO"])
        .size()
        .reset_index(name="total")
        .query("total > 0")
        .sort_values("total", ascending=True)
        .head(n)
    )

    scope_label = department if department else "Colombia"
    title = (
        f"Diez municipios con menor número de defunciones — {scope_label}, 2019"
    )

    fig = go.Figure(
        go.Pie(
            labels=counts["MUNICIPIO"],
            values=counts["total"],
            marker=dict(
                colors=theme.CATEGORICAL_SEQUENCE[: len(counts)],
                line=dict(color=theme.BACKGROUND, width=1.5),
            ),
            textinfo="label+value",
            textposition="outside",
            textfont=dict(family=theme.BODY_FONT, size=11, color=theme.NEUTRAL_DARK),
            customdata=counts["DEPARTAMENTO"],
            hovertemplate=(
                "<b>%{label}</b> (%{customdata})<br>Defunciones: %{value:,}"
                "<br>Participación: %{percent}<extra></extra>"
            ),
            sort=False,
            hole=0.35,
        )
    )

    theme.apply_layout(fig, title=title, height=460, show_legend=False)
    return fig
