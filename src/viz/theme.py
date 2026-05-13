"""Tema visual sobrio para la aplicación.

Define una paleta monocromática azul-gris alineada con el estándar APA:
fondo blanco, grilla discreta, tipografía serif para títulos y sans-serif
para cuerpo. Todas las visualizaciones la usan vía ``apply_layout``.
"""

from __future__ import annotations

from typing import Final

import plotly.graph_objects as go

PRIMARY: Final[str] = "#1F3A5F"
SECONDARY: Final[str] = "#4A6B8A"
TERTIARY: Final[str] = "#7A8B99"
QUATERNARY: Final[str] = "#A8B5BF"
SUBTLE: Final[str] = "#D1D8DE"

NEUTRAL_DARK: Final[str] = "#1A1A1A"
NEUTRAL_MEDIUM: Final[str] = "#4A4A4A"
NEUTRAL_LIGHT: Final[str] = "#9E9E9E"

GRID: Final[str] = "#E8E8E8"
BACKGROUND: Final[str] = "#FFFFFF"

TITLE_FONT: Final[str] = "Source Serif Pro, Georgia, 'Times New Roman', serif"
BODY_FONT: Final[str] = "Source Sans Pro, Helvetica, Arial, sans-serif"

SEX_COLORS: Final[dict[str, str]] = {
    "Hombre": PRIMARY,
    "Mujer": TERTIARY,
    "Indeterminado": NEUTRAL_LIGHT,
}

SEQUENTIAL_SCALE: Final[list[list[float | str]]] = [
    [0.0, "#F2F4F7"],
    [0.25, "#C7D1DC"],
    [0.5, TERTIARY],
    [0.75, SECONDARY],
    [1.0, PRIMARY],
]

CATEGORICAL_SEQUENCE: Final[list[str]] = [
    PRIMARY,
    SECONDARY,
    TERTIARY,
    QUATERNARY,
    NEUTRAL_MEDIUM,
    NEUTRAL_LIGHT,
    SUBTLE,
    "#5C7C99",
    "#34495E",
    "#8FA3B5",
]


def apply_layout(
    fig: go.Figure,
    *,
    title: str = "",
    height: int | None = None,
    show_legend: bool = True,
    legend_orientation: str = "h",
) -> go.Figure:
    """Aplica el tema sobrio a una figura Plotly ya construida."""
    fig.update_layout(
        title=dict(
            text=title,
            font=dict(family=TITLE_FONT, size=16, color=NEUTRAL_DARK),
            x=0.02,
            xanchor="left",
        ),
        font=dict(family=BODY_FONT, size=12, color=NEUTRAL_DARK),
        paper_bgcolor=BACKGROUND,
        plot_bgcolor=BACKGROUND,
        margin=dict(l=70, r=30, t=70, b=60),
        height=height,
        showlegend=show_legend,
        legend=dict(
            orientation=legend_orientation,
            yanchor="bottom" if legend_orientation == "h" else "top",
            y=-0.2 if legend_orientation == "h" else 1.0,
            xanchor="left",
            x=0.0,
            font=dict(family=BODY_FONT, size=11),
        ),
        hoverlabel=dict(
            bgcolor=BACKGROUND,
            bordercolor=NEUTRAL_MEDIUM,
            font=dict(family=BODY_FONT, size=12, color=NEUTRAL_DARK),
        ),
    )
    fig.update_xaxes(
        showgrid=False,
        linecolor=NEUTRAL_MEDIUM,
        tickcolor=NEUTRAL_MEDIUM,
        ticks="outside",
        title_font=dict(family=BODY_FONT, size=12, color=NEUTRAL_DARK),
    )
    fig.update_yaxes(
        showgrid=True,
        gridcolor=GRID,
        zeroline=False,
        linecolor=NEUTRAL_MEDIUM,
        tickcolor=NEUTRAL_MEDIUM,
        ticks="outside",
        title_font=dict(family=BODY_FONT, size=12, color=NEUTRAL_DARK),
    )
    return fig


def annotate_source(fig: go.Figure, source: str) -> go.Figure:
    """Añade nota al pie con la fuente del dato (estilo APA)."""
    fig.add_annotation(
        text=f"<i>Fuente:</i> {source}",
        xref="paper",
        yref="paper",
        x=0,
        y=-0.18,
        showarrow=False,
        font=dict(family=BODY_FONT, size=10, color=NEUTRAL_MEDIUM),
        xanchor="left",
    )
    return fig
