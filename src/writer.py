"""
Módulo Writer — Fase 3: Motor de exportación ejecutiva.

Renderiza los resultados de la auditoría en reportes portátiles
HTML y Markdown usando plantillas de Jinja2.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from jinja2 import Environment, FileSystemLoader, select_autoescape

TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "templates"

_env = Environment(
    loader=FileSystemLoader(str(TEMPLATES_DIR)),
    autoescape=select_autoescape(["html"]),
)


def _build_context(
    kpis: dict,
    valid_df: pd.DataFrame,
    invalid_df: pd.DataFrame,
    anomalies: pd.DataFrame,
) -> dict:
    return {
        "kpis": kpis,
        "valid_invoices": valid_df.to_dict(orient="records"),
        "invalid_invoices": invalid_df.to_dict(orient="records"),
        "anomalies": anomalies.to_dict(orient="records") if not anomalies.empty else [],
    }


def render_html_report(
    kpis: dict, valid_df: pd.DataFrame, invalid_df: pd.DataFrame, anomalies: pd.DataFrame
) -> str:
    """Genera el reporte HTML 'Classic Elegant', autocontenido y listo
    para compartir por correo."""
    template = _env.get_template("report_template.html")
    return template.render(**_build_context(kpis, valid_df, invalid_df, anomalies))


def render_markdown_report(
    kpis: dict, valid_df: pd.DataFrame, invalid_df: pd.DataFrame, anomalies: pd.DataFrame
) -> str:
    """Genera el reporte en Markdown, ideal para documentar juntas o
    minutas de trabajo en Notion."""
    template = _env.get_template("report_template.md")
    return template.render(**_build_context(kpis, valid_df, invalid_df, anomalies))
