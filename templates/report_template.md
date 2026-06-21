# 📊 Statix — Reporte de Auditoría Fiscal

## Indicadores Clave

| Indicador | Monto |
|---|---|
| Total de Ingresos | ${{ "%.2f"|format(kpis.ingresos) }} |
| Total de Gastos | ${{ "%.2f"|format(kpis.gastos) }} |
| IVA Neto | ${{ "%.2f"|format(kpis.iva_neto) }} |

## 🟢 Facturas Válidas ({{ valid_invoices|length }})

| UUID | Fecha | RFC Emisor | RFC Receptor | Total |
|---|---|---|---|---|
{% for inv in valid_invoices -%}
| {{ inv.uuid }} | {{ inv.fecha }} | {{ inv.rfc_emisor }} | {{ inv.rfc_receptor }} | ${{ "%.2f"|format(inv.total) }} |
{% endfor %}

## 🔴 Alertas de Integridad ({{ invalid_invoices|length }})

| UUID | Errores Detectados |
|---|---|
{% for inv in invalid_invoices -%}
| {{ inv.uuid }} | {{ inv._errores }} |
{% endfor %}

{% if anomalies %}
## ⚠️ Anomalías Detectadas ({{ anomalies|length }})

| UUID | Tipo de Anomalía | Total |
|---|---|---|
{% for a in anomalies -%}
| {{ a.uuid }} | {{ a.tipo_anomalia }} | ${{ "%.2f"|format(a.total) }} |
{% endfor %}
{% endif %}
