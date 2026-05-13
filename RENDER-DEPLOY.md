# Guía de despliegue en Render

Esta guía contiene los pasos necesarios para publicar la aplicación en Render como **Web Service** en el plan **Free**. Todos los archivos requeridos por la plataforma (`requirements.txt`, `Procfile`, `runtime.txt`) ya están en el repositorio.

## Prerrequisitos

- Cuenta en [Render](https://render.com) iniciada con la misma cuenta de GitHub donde está alojado el repositorio.
- Repositorio `mortalidad-colombia-2019` accesible desde la cuenta de Render (autorizado al iniciar sesión con GitHub).

## Pasos

1. Ingresar al [dashboard de Render](https://dashboard.render.com).
2. Hacer clic en **New +** (esquina superior derecha) y elegir **Web Service**.
3. En la pantalla **Create a new Web Service**, seleccionar la opción **Build and deploy from a Git repository** y continuar.
4. Elegir el repositorio `mortalidad-colombia-2019`. Si no aparece, hacer clic en **Configure account** y conceder acceso a Render desde GitHub.
5. Completar el formulario de creación con los siguientes parámetros:

   | Parámetro | Valor |
   |---|---|
   | Name | `mortalidad-colombia-2019` |
   | Project | *(opcional)* `Maestría IA - Aplicaciones I` |
   | Region | `Oregon (US West)` |
   | Branch | `main` |
   | Root Directory | *(dejar vacío)* |
   | Runtime | `Python 3` |
   | Build Command | `pip install -r requirements.txt` |
   | Start Command | `gunicorn app:server --workers 1 --threads 4 --timeout 120 --bind 0.0.0.0:$PORT` |
   | Instance Type | `Free` |

6. Desplegar las opciones **Advanced** y verificar:
   - **Auto-Deploy**: activado, branch `main`.
   - **Health Check Path**: dejar vacío (Render usa la raíz por defecto, que devuelve HTTP 200).
   - No es necesario configurar variables de entorno adicionales para esta aplicación.

7. Hacer clic en **Create Web Service**. El primer build toma entre 5 y 10 minutos.
8. Cuando el deploy termine, Render expone una URL pública con el formato `https://mortalidad-colombia-2019.onrender.com`. Esa es la URL que debe registrarse en el comentario de la entrega.

## Validación posterior al despliegue

- Abrir la URL pública en una ventana de navegador limpia (incógnito) y confirmar que las siete visualizaciones se cargan.
- Cambiar el valor del dropdown **Filtrar resultados por departamento** y verificar que las cinco gráficas reactivas se actualizan.
- En la primera visita tras un periodo de inactividad, la instancia puede tardar entre 30 y 60 segundos en responder. Es el comportamiento esperado del plan Free.

## Si algo falla

| Síntoma | Causa probable | Solución |
|---|---|---|
| `ModuleNotFoundError: No module named 'src'` | Render arrancó en la carpeta equivocada | Confirmar que **Root Directory** está vacío. |
| El build falla por versión de Python | Render no respetó `runtime.txt` | Editar **Environment** y agregar la variable `PYTHON_VERSION=3.11.9`. |
| `Worker failed to boot` | Tiempo de arranque insuficiente | El parámetro `--timeout 120` del Start Command resuelve esto. Verificar que no se haya cambiado. |
| 502 Bad Gateway | Memoria insuficiente | Reintentar el deploy. Si persiste, escalar a plan Starter. |

## Documentación oficial de Render

- [Deploy a Dash app on Render](https://render.com/docs/deploy-dash)
- [Python runtime in Render](https://render.com/docs/python-version)
