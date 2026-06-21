"""Pruebas unitarias básicas para el módulo Reader."""

import pandas as pd

from src.reader import validate_invoices, _is_valid_rfc


def test_rfc_valido_persona_moral():
    assert _is_valid_rfc("ABC850101AB1")


def test_rfc_invalido():
    assert not _is_valid_rfc("123-INVALIDO")


def test_validate_invoices_detecta_descuadre_fiscal():
    df = pd.DataFrame([{
        "uuid": "11111111-1111-1111-1111-111111111111",
        "fecha": "2026-01-01",
        "rfc_emisor": "ABC850101AB1",
        "rfc_receptor": "XYZ900101XY2",
        "subtotal": 100,
        "iva": 16,
        "retenciones": 0,
        "total": 999,  # Total incorrecto a propósito
        "tipo_comprobante": "Ingreso",
    }])

    valid_df, invalid_df = validate_invoices(df)

    assert valid_df.empty
    assert len(invalid_df) == 1
    assert "Descuadre fiscal" in invalid_df.iloc[0]["_errores"]


def test_validate_invoices_acepta_factura_correcta():
    df = pd.DataFrame([{
        "uuid": "22222222-2222-2222-2222-222222222222",
        "fecha": "2026-01-02",
        "rfc_emisor": "ABC850101AB1",
        "rfc_receptor": "XYZ900101XY2",
        "subtotal": 100,
        "iva": 16,
        "retenciones": 0,
        "total": 116,
        "tipo_comprobante": "Ingreso",
    }])

    valid_df, invalid_df = validate_invoices(df)

    assert len(valid_df) == 1
    assert invalid_df.empty
