"""
Módulo Analyzer — Fase 2: Tablero de auditoría dinámica.

Calcula KPIs financieros y detecta anomalías sobre el conjunto de
facturas válidas.
"""

from __future__ import annotations

import pandas as pd


def calculate_kpis(df: pd.DataFrame) -> dict:
    """Calcula los indicadores clave del periodo: ingresos, gastos
    e IVA neto.

        IVA Neto = IVA Trasladado - IVA Acreditable
    """
    if df.empty:
        return {"ingresos": 0.0, "gastos": 0.0, "iva_neto": 0.0}

    tipo = df["tipo_comprobante"].astype(str).str.lower()

    ingresos = df.loc[tipo == "ingreso", "total"].sum()
    gastos = df.loc[tipo == "egreso", "total"].sum()

    iva_trasladado = df.loc[tipo == "ingreso", "iva"].sum()
    iva_acreditable = df.loc[tipo == "egreso", "iva"].sum()
    iva_neto = iva_trasladado - iva_acreditable

    return {
        "ingresos": float(ingresos),
        "gastos": float(gastos),
        "iva_neto": float(iva_neto),
    }


def detect_anomalies(df: pd.DataFrame, expense_zscore_threshold: float = 2.5) -> pd.DataFrame:
    """Detecta focos rojos: UUIDs duplicados y picos atípicos de gastos
    usando una desviación estándar (z-score) como umbral."""
    if df.empty:
        return df.copy()

    anomalies = []

    duplicated = df[df.duplicated(subset=["uuid"], keep=False)]
    for _, row in duplicated.iterrows():
        anomalies.append({**row.to_dict(), "tipo_anomalia": "UUID duplicado"})

    if "tipo_comprobante" in df.columns:
        gastos = df[df["tipo_comprobante"].astype(str).str.lower() == "egreso"]
        if len(gastos) > 1:
            media = gastos["total"].mean()
            desviacion = gastos["total"].std() or 0
            if desviacion > 0:
                picos = gastos[
                    (gastos["total"] - media).abs() > expense_zscore_threshold * desviacion
                ]
                for _, row in picos.iterrows():
                    anomalies.append({**row.to_dict(), "tipo_anomalia": "Gasto atípico"})

    return pd.DataFrame(anomalies)


def razon_circulante(activo_circulante: float, pasivo_circulante: float) -> float | None:
    """Calcula la Razón Circulante para medir liquidez inmediata.

        Razón Circulante = Activo Circulante / Pasivo Circulante
    """
    if not pasivo_circulante:
        return None
    return activo_circulante / pasivo_circulante
