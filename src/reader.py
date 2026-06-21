"""
Módulo Reader — Fase 1: Carga e integridad de datos.

Responsable de leer archivos CSV/JSON de facturación (CFDI) y
separar los registros en facturas válidas y alertas de integridad.
"""

from __future__ import annotations

import re
from decimal import Decimal, InvalidOperation

import pandas as pd

# RFC mexicano: persona física (13 caracteres) o moral (12 caracteres)
RFC_PATTERN = re.compile(r"^([A-ZÑ&]{3,4})\d{6}([A-Z\d]{3})$")

REQUIRED_COLUMNS = [
    "uuid",
    "fecha",
    "rfc_emisor",
    "rfc_receptor",
    "subtotal",
    "iva",
    "retenciones",
    "total",
    "tipo_comprobante",
]


def load_invoices(uploaded_file) -> pd.DataFrame:
    """Carga un archivo CSV o JSON de facturación en un DataFrame."""
    name = uploaded_file.name.lower()

    if name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    elif name.endswith(".json"):
        df = pd.read_json(uploaded_file)
    else:
        raise ValueError("Formato no soportado. Usa archivos .csv o .json")

    df.columns = [col.strip().lower() for col in df.columns]
    return df


def _to_decimal(value) -> Decimal | None:
    """Convierte un valor a Decimal de forma segura, evitando errores de
    punto flotante en cálculos fiscales."""
    try:
        return Decimal(str(value))
    except (InvalidOperation, TypeError):
        return None


def _is_valid_rfc(rfc: str) -> bool:
    if not isinstance(rfc, str):
        return False
    return bool(RFC_PATTERN.match(rfc.strip().upper()))


def validate_invoices(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Audita cada fila del DataFrame y separa los registros en válidos
    e inválidos según la ecuación fiscal base:

        Total = Subtotal + IVA - Retenciones

    También valida la estructura de los RFC emisor/receptor y la
    presencia del Folio Fiscal (UUID).
    """
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"Faltan columnas requeridas en el archivo: {missing}")

    errors = []
    valid_mask = []

    for _, row in df.iterrows():
        row_errors = []

        subtotal = _to_decimal(row.get("subtotal"))
        iva = _to_decimal(row.get("iva"))
        retenciones = _to_decimal(row.get("retenciones")) or Decimal("0")
        total = _to_decimal(row.get("total"))

        if subtotal is None or iva is None or total is None:
            row_errors.append("Valores numéricos inválidos o nulos")
        else:
            esperado = subtotal + iva - retenciones
            if esperado != total:
                row_errors.append(
                    f"Descuadre fiscal: esperado {esperado}, encontrado {total}"
                )

        if not _is_valid_rfc(row.get("rfc_emisor", "")):
            row_errors.append("RFC emisor con estructura inválida")
        if not _is_valid_rfc(row.get("rfc_receptor", "")):
            row_errors.append("RFC receptor con estructura inválida")

        if pd.isna(row.get("uuid")) or not str(row.get("uuid")).strip():
            row_errors.append("Folio Fiscal (UUID) ausente")

        errors.append("; ".join(row_errors))
        valid_mask.append(len(row_errors) == 0)

    df = df.copy()
    df["_errores"] = errors

    mask = pd.Series(valid_mask, index=df.index)
    valid_df = df[mask].drop(columns=["_errores"]).reset_index(drop=True)
    invalid_df = df[~mask].reset_index(drop=True)

    return valid_df, invalid_df
