# 📊 Statix

**Motor Visual de Auditoría y Analítica Fiscal**

Statix transforma archivos crudos de facturación (CSV y JSON) en tableros de control financieros y reportes de auditoría fiscal, usando un stack 100% Python.

---

## 📑 Tabla de Contenidos

- [Descripción](#-descripción)
- [Stack Tecnológico](#-stack-tecnológico)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Instalación](#-instalación)
- [Uso](#-uso)
- [Formato de Datos Esperado](#-formato-de-datos-esperado)
- [Hoja de Ruta](#-hoja-de-ruta)
- [Contribuir](#-contribuir)
- [Licencia](#-licencia)

---

## 📌 Descripción

Statix automatiza la detección de discrepancias impositivas, calcula la salud financiera de una entidad y ofrece una interfaz gráfica moderna sin necesidad de servidores empresariales ni entornos de ejecución complejos.

## 🛠️ Stack Tecnológico

| Componente | Tecnología | Propósito |
|---|---|---|
| Interfaz de Usuario | [Streamlit](https://streamlit.io/) | Aplicación web interactiva en Python puro |
| Motor de Datos | [Pandas](https://pandas.pydata.org/) | Manipulación y estructuración de registros |
| Precisión Financiera | `decimal` (stdlib) | Aritmética de punto fijo para evitar pérdida de centavos |
| Motor de Reportes | [Jinja2](https://jinja.palletsprojects.com/) | Generación de plantillas HTML y Markdown |

## 🗂️ Estructura del Proyecto

```
statix/
├── app.py                     # Punto de entrada de la app Streamlit
├── requirements.txt
├── src/
│   ├── reader.py               # Fase 1 — Carga e integridad de datos
│   ├── analyzer.py             # Fase 2 — KPIs y detección de anomalías
│   └── writer.py                # Fase 3 — Exportación de reportes
├── templates/
│   ├── report_template.html     # Reporte "Classic Elegant"
│   └── report_template.md
├── data/                       # Archivos cargados localmente (ignorado por git)
├── tests/
└── .streamlit/
    └── config.toml             # Tema visual de la app
```

## ⚙️ Instalación

```bash
git clone https://github.com/<tu-usuario>/statix.git
cd statix

python -m venv venv
source venv/bin/activate   # En Windows: venv\Scripts\activate

pip install -r requirements.txt
```

## ▶️ Uso

```bash
streamlit run app.py
```

Abre el navegador en `http://localhost:8501`, arrastra tu archivo `.csv` o `.json` de facturación y explora el tablero de auditoría.

## 📋 Formato de Datos Esperado

El sistema espera las siguientes columnas mínimas en el archivo de entrada (CFDI):

`uuid`, `fecha`, `rfc_emisor`, `rfc_receptor`, `subtotal`, `iva`, `retenciones`, `total`, `tipo_comprobante`

La validación se basa en la ecuación fiscal:

```
Total = Subtotal + IVA - Retenciones
```

## 🗺️ Hoja de Ruta

- [ ] **Fase 1 — MVP Visual:** Carga inteligente y filtro de sanitización de datos.
- [ ] **Fase 2 — Tablero de Auditoría:** KPIs, filtros laterales y detección de anomalías.
- [ ] **Fase 3 — Exportación Ejecutiva:** Reportes descargables en HTML y Markdown.

## 🤝 Contribuir

Las contribuciones son bienvenidas. Abre un *issue* para discutir cambios mayores antes de enviar un *pull request*.

## 📄 Licencia

Este proyecto está bajo la licencia MIT. Consulta el archivo [LICENSE](./LICENSE) para más detalles.
