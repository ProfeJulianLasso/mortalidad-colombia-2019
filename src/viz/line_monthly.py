"""Línea de defunciones mensuales con filtro opcional por departamento."""

from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go

from src.data.constants import MONTH_LABELS
from src.viz import theme


def create(deaths: pd.DataFrame, department: str | None = None) -> go.Figure:
    """Defunciones mes a mes. Si se indica un departamento, lo filtra."""
    filtered = deaths if department is None else deaths[deaths["DEPARTAMENTO"] == department]

    monthly = (
        filtered.groupby(["MES"]).size().reset_index(name="total").sort_values("MES")
    )
    monthly["MES_NOMBRE"] = monthly["MES"].map(MONTH_LABELS)

    scope = department if department else "Colombia"
    title = f"Defunciones mensuales — {scope}, 2019"

    fig = go.Figure(
        go.Scatter(
            x=monthly["MES_NOMBRE"],
            y=monthly["total"],
            mode="lines+markers",
            line=dict(color=theme.PRIMARY, width=2),
            marker=dict(size=8, color=theme.PRIMARY, line=dict(width=1, color=theme.BACKGROUND)),
            hovertemplate="<b>%{x}</b><br>Defunciones: %{y:,}<extra></extra>",
        )
    )

    theme.apply_layout(fig, title=title, height=380, show_legend=False)
    fig.update_xaxes(title="Mes")
    fig.update_yaxes(title="Defunciones registradas", tickformat=",d")
    return fig
