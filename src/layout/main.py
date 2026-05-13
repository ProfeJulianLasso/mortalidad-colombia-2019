"""Layout principal del dashboard de mortalidad."""

from __future__ import annotations

from dash import dcc, html
from plotly.graph_objects import Figure

from src.layout import header

ALL_DEPARTMENTS_LABEL = "Todos los departamentos"


def build_department_options(department_names: list[str]) -> list[dict[str, str]]:
    return [{"label": ALL_DEPARTMENTS_LABEL, "value": ALL_DEPARTMENTS_LABEL}] + [
        {"label": name, "value": name} for name in department_names
    ]


def render(
    department_options: list[dict[str, str]],
    figures: dict[str, Figure],
) -> html.Div:
    return html.Div(
        className="app-container",
        children=[
            header.render_header(),
            _render_controls(department_options),
            _render_dashboard(figures),
            header.render_footer(),
        ],
    )


def _render_controls(department_options: list[dict[str, str]]) -> html.Section:
    return html.Section(
        className="controls",
        children=[
            html.Div(
                className="control-group",
                children=[
                    html.Label(
                        "Filtrar resultados por departamento",
                        htmlFor="department-filter",
                        className="control-label",
                    ),
                    dcc.Dropdown(
                        id="department-filter",
                        options=department_options,
                        value=ALL_DEPARTMENTS_LABEL,
                        clearable=False,
                        searchable=True,
                        className="control-dropdown",
                    ),
                    html.Small(
                        "El mapa nacional y la comparación de sexo por "
                        "departamento conservan el alcance nacional para "
                        "preservar la comparabilidad.",
                        className="control-help",
                    ),
                ],
            )
        ],
    )


def _render_dashboard(figures: dict[str, Figure]) -> html.Main:
    return html.Main(
        className="dashboard",
        children=[
            _section(
                title="Distribución geográfica y temporal",
                children=[
                    _figure("graph-map", figures["map"], wide=True),
                    _figure("graph-line", figures["line"]),
                ],
                layout="two-columns-wide-left",
            ),
            _section(
                title="Focos de violencia y municipios con menor mortalidad",
                children=[
                    _figure("graph-violent", figures["violent"]),
                    _figure("graph-pie", figures["pie"]),
                ],
                layout="two-columns-equal",
            ),
            _section(
                title="Principales causas de muerte",
                children=[_figure("graph-table", figures["table"], wide=True)],
                layout="single",
            ),
            _section(
                title="Distribución por sexo y por etapa del ciclo vital",
                children=[
                    _figure("graph-stacked", figures["stacked"], wide=True),
                    _figure("graph-histogram", figures["histogram"], wide=True),
                ],
                layout="single",
            ),
        ],
    )


def _section(title: str, children: list, layout: str) -> html.Section:
    return html.Section(
        className="dashboard-section",
        children=[
            html.H2(title, className="section-title"),
            html.Div(className=f"section-body {layout}", children=children),
        ],
    )


def _figure(component_id: str, figure: Figure, *, wide: bool = False) -> html.Div:
    return html.Div(
        className="figure-card" + (" wide" if wide else ""),
        children=[
            dcc.Graph(
                id=component_id,
                figure=figure,
                config={
                    "displaylogo": False,
                    "modeBarButtonsToRemove": [
                        "lasso2d",
                        "select2d",
                        "autoScale2d",
                        "toggleSpikelines",
                    ],
                    "responsive": True,
                },
            )
        ],
    )
