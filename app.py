"""
Statix — Motor Visual de Auditoría y Analítica Fiscal
Punto de entrada principal de la aplicación Streamlit.
"""

import streamlit as st

from src.reader import load_invoices, validate_invoices
from src.analyzer import calculate_kpis, detect_anomalies
from src.writer import render_html_report, render_markdown_report

st.set_page_config(
    page_title="Statix · Auditoría Fiscal",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)


def main() -> None:
    st.title("📊 Statix")
    st.caption("Motor Visual de Auditoría y Analítica Fiscal")

    # --- Panel lateral: filtros (se activan tras cargar datos) ---
    with st.sidebar:
        st.header("⚙️ Filtros")
        st.info("Carga un archivo para habilitar los filtros de fecha, cliente y tipo de comprobante.")

    # --- Fase 1: Carga e integridad de datos ---
    st.subheader("1. Carga de Archivos")
    uploaded_file = st.file_uploader(
        "Arrastra tu archivo de facturación (CFDI)",
        type=["csv", "json"],
        help="Formatos soportados: CSV y JSON",
    )

    if uploaded_file is None:
        st.info("Esperando un archivo `.csv` o `.json` para comenzar la auditoría.")
        return

    df = load_invoices(uploaded_file)
    valid_df, invalid_df = validate_invoices(df)

    col_valid, col_invalid = st.columns(2)
    with col_valid:
        st.markdown("### 🟢 Facturas Válidas")
        st.dataframe(valid_df, use_container_width=True)
    with col_invalid:
        st.markdown("### 🔴 Alertas de Integridad")
        st.dataframe(invalid_df, use_container_width=True)

    # --- Fase 2: Tablero de auditoría dinámica ---
    st.subheader("2. Tablero de Auditoría")
    kpis = calculate_kpis(valid_df)

    kpi_cols = st.columns(3)
    kpi_cols[0].metric("Total de Ingresos", f"${kpis['ingresos']:,.2f}")
    kpi_cols[1].metric("Total de Gastos", f"${kpis['gastos']:,.2f}")
    kpi_cols[2].metric(
        "IVA Neto",
        f"${kpis['iva_neto']:,.2f}",
        delta="Por pagar" if kpis["iva_neto"] > 0 else "Saldo a favor",
    )

    anomalies = detect_anomalies(valid_df)
    if not anomalies.empty:
        st.warning("Se detectaron anomalías en el periodo cargado.")
        st.dataframe(anomalies, use_container_width=True)

    # --- Fase 3: Exportación ejecutiva ---
    st.subheader("3. Exportar Reporte")
    export_cols = st.columns(2)
    with export_cols[0]:
        if st.button("⬇️ Generar Reporte HTML"):
            html_report = render_html_report(kpis, valid_df, invalid_df, anomalies)
            st.download_button(
                "Guardar reporte.html",
                data=html_report,
                file_name="statix_reporte.html",
                mime="text/html",
            )
    with export_cols[1]:
        if st.button("⬇️ Generar Reporte Markdown"):
            md_report = render_markdown_report(kpis, valid_df, invalid_df, anomalies)
            st.download_button(
                "Guardar reporte.md",
                data=md_report,
                file_name="statix_reporte.md",
                mime="text/markdown",
            )


if __name__ == "__main__":
    main()
