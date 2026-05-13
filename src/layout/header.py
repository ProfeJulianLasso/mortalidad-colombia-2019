"""Encabezado y pie de la aplicación."""

from __future__ import annotations

from dash import html


def render_header() -> html.Header:
    return html.Header(
        className="app-header",
        children=[
            html.Div(
                className="header-content",
                children=[
                    html.H1(
                        "Análisis de la mortalidad en Colombia, 2019",
                        className="app-title",
                    ),
                    html.P(
                        "Aplicación web interactiva sobre los microdatos de "
                        "defunciones no fetales publicados por el DANE.",
                        className="app-subtitle",
                    ),
                ],
            ),
        ],
    )


def render_footer() -> html.Footer:
    return html.Footer(
        className="app-footer",
        children=[
            html.P(
                children=[
                    "Fuente: Departamento Administrativo Nacional de Estadística "
                    "(DANE). Estadísticas Vitales 2019 — Defunciones no fetales. ",
                    html.A(
                        "Catálogo de microdatos.",
                        href="https://microdatos.dane.gov.co/index.php/catalog/696",
                        target="_blank",
                        rel="noopener noreferrer",
                    ),
                ]
            ),
            html.P(
                "Maestría en Inteligencia Artificial — Universidad de La Salle. "
                "Curso: Aplicaciones de Inteligencia Artificial.",
                className="footer-meta",
            ),
        ],
    )
