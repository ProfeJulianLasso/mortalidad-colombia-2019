"""Top de ciudades por homicidios con arma de fuego (CIE-10 X95)."""

from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go

from src.data.constants import VIOLENT_DEATH_PREFIX
from src.viz import theme


def create(
    deaths: pd.DataFrame,
    department: str | None = None,
    n: int = 5,
) -> go.Figure:
    """Top ``n`` ciudades por homicidios con disparo de arma de fuego."""
    scope = deaths if department is None else deaths[deaths["DEPARTAMENTO"] == department]
    violent = scope[
        scope["COD_MUERTE"].str.startswith(VIOLENT_DEATH_PREFIX, na=False)
    ]

    top = (
        violent.groupby(["MUNICIPIO", "DEPARTAMENTO"])
        .size()
        .reset_index(name="total")
        .sort_values("total", ascending=False)
        .head(n)
        .iloc[::-1]
    )

    scope_label = department if department else "Colombia"
    title = (
        f"Ciudades con mayor número de homicidios con arma de fuego — "
        f"{scope_label}, 2019"
    )

    fig = go.Figure(
        go.Bar(
            x=top["total"],
            y=top["MUNICIPIO"],
            orientation="h",
            marker=dict(color=theme.PRIMARY, line=dict(color=theme.NEUTRAL_DARK, width=0.4)),
            text=top["total"].map("{:,}".format),
            textposition="outside",
            textfont=dict(family=theme.BODY_FONT, size=11, color=theme.NEUTRAL_DARK),
            customdata=top["DEPARTAMENTO"],
            hovertemplate=(
                "<b>%{y}</b> (%{customdata})<br>Homicidios X95: %{x:,}<extra></extra>"
            ),
        )
    )

    theme.apply_layout(fig, title=title, height=380, show_legend=False)
    fig.update_xaxes(title="Homicidios registrados", tickformat=",d")
    fig.update_yaxes(title="", automargin=True)
    return fig
