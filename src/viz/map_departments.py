"""Mapa coroplético de defunciones por departamento."""

from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go

from src.viz import theme


def create(deaths: pd.DataFrame, geojson: dict) -> go.Figure:
    """Construye el coroplético nacional. No se filtra por departamento."""
    counts = (
        deaths.groupby(["COD_DEPARTAMENTO", "DEPARTAMENTO"])
        .size()
        .reset_index(name="total")
    )

    fig = go.Figure(
        go.Choropleth(
            geojson=geojson,
            featureidkey="properties.DPTO",
            locations=counts["COD_DEPARTAMENTO"],
            z=counts["total"],
            colorscale=theme.SEQUENTIAL_SCALE,
            marker=dict(line=dict(color=theme.BACKGROUND, width=0.5)),
            colorbar=dict(
                title=dict(text="Defunciones", font=dict(family=theme.BODY_FONT, size=12)),
                thickness=14,
                len=0.75,
                tickformat=",d",
                tickfont=dict(family=theme.BODY_FONT, size=11),
                outlinewidth=0,
            ),
            customdata=counts["DEPARTAMENTO"],
            hovertemplate=(
                "<b>%{customdata}</b><br>Defunciones registradas: %{z:,}<extra></extra>"
            ),
        )
    )

    fig.update_geos(
        visible=False,
        projection=dict(type="mercator"),
        fitbounds="locations",
        bgcolor=theme.BACKGROUND,
    )

    theme.apply_layout(
        fig,
        title="Distribución de defunciones por departamento, Colombia 2019",
        height=620,
        show_legend=False,
    )
    return fig
