# Mortalidad en Colombia 2019 — Aplicación web interactiva

Aplicación web dinámica desarrollada en Python con Dash y Plotly para el análisis interactivo de la mortalidad en Colombia durante el año 2019, a partir de los microdatos publicados por el DANE.

---

## Introducción

Este proyecto presenta un dashboard interactivo que permite explorar visualmente la mortalidad no fetal registrada en Colombia en 2019. Integra los microdatos de defunciones publicados por el DANE con los catálogos de códigos CIE-10 (causas de muerte) y la División Político-Administrativa (DIVIPOLA), de forma que el usuario pueda identificar patrones demográficos y regionales mediante visualizaciones interactivas.

## Objetivo

Analizar la mortalidad en Colombia durante 2019 e identificar:

- La distribución geográfica de las muertes por departamento.
- La evolución temporal a lo largo del año.
- Las ciudades con mayor incidencia de violencia (homicidios por arma de fuego).
- Las principales causas de muerte a nivel nacional.
- Las diferencias por sexo y por etapa del ciclo vital.

## Estructura del proyecto

```
mortalidad-colombia-2019/
├── app.py                  # Punto de entrada de la aplicación Dash
├── pyproject.toml          # Configuración del proyecto y dependencias
├── requirements.txt        # Dependencias para despliegue en Render
├── Procfile                # Comando de arranque para Render (gunicorn)
├── runtime.txt             # Versión de Python para Render
├── data/
│   ├── raw/                # Archivos Excel originales del DANE
│   └── processed/          # Datasets agregados en Parquet (generados)
├── src/
│   ├── data/               # Carga y transformación de datos
│   ├── viz/                # Funciones generadoras de figuras Plotly
│   └── layout/             # Componentes de layout de Dash
├── scripts/                # Scripts auxiliares (build_processed, inventario)
├── assets/                 # Recursos estáticos (CSS, imágenes)
└── README.md
```

## Requisitos

- Python 3.11
- Dash
- Plotly
- Pandas
- openpyxl (lectura de Excel)
- pyarrow (lectura/escritura de Parquet)
- gunicorn (servidor WSGI para producción)

Las versiones exactas se encuentran fijadas en `pyproject.toml` y `requirements.txt`.

## Despliegue en Render

La aplicación se despliega como **Web Service** en Render usando los siguientes parámetros:

- **Build command:** `pip install -r requirements.txt`
- **Start command:** `gunicorn app:server`
- **Runtime:** Python 3.11
- **Plan:** Free

> Nota: el plan Free de Render suspende el servicio tras 15 minutos de inactividad. El primer acceso puede tardar ~30 segundos en responder mientras la instancia se reactiva.

URL de la aplicación desplegada: *pendiente de publicación*

## Software utilizado

- Python 3.11
- Dash y Plotly para la capa de visualización e interacción
- Pandas para el procesamiento de los microdatos
- uv como gestor de entorno y dependencias en desarrollo
- gunicorn como servidor WSGI en producción
- Render como plataforma como servicio (PaaS) para el despliegue

## Instalación local

Clonar el repositorio y crear el entorno con `uv`:

```bash
git clone git@github.com:ProfeJulianLasso/mortalidad-colombia-2019.git
cd mortalidad-colombia-2019
uv sync
```

Generar los datasets procesados a partir de los Excel originales:

```bash
uv run python scripts/build_processed.py
```

Ejecutar la aplicación localmente:

```bash
uv run python app.py
```

La aplicación queda disponible en `http://127.0.0.1:8050/`.

## Visualizaciones y hallazgos

*Esta sección se completa al finalizar el desarrollo, con capturas de pantalla y la interpretación cuantitativa de cada gráfico.*

### 1. Mapa: Distribución de muertes por departamento

*Pendiente.*

### 2. Línea: Muertes por mes

*Pendiente.*

### 3. Barras: Cinco ciudades más violentas

*Pendiente.*

### 4. Pastel: Diez ciudades con menor mortalidad

*Pendiente.*

### 5. Tabla: Diez principales causas de muerte

*Pendiente.*

### 6. Barras apiladas: Muertes por sexo y departamento

*Pendiente.*

### 7. Histograma: Mortalidad por etapa del ciclo vital

*Pendiente.*

## Fuente de los datos

Departamento Administrativo Nacional de Estadística (DANE). *Estadísticas Vitales (EEVV) 2019 — Defunciones No Fetales*. Catálogo de microdatos 696. Disponible en: <https://microdatos.dane.gov.co/index.php/catalog/696>

## Autor

Julián Andrés Lasso Figueroa
Maestría en Inteligencia Artificial — Universidad de La Salle
Curso: Aplicaciones de Inteligencia Artificial
