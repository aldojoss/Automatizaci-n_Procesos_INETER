# Seguimiento al PAC 2026 · INETER

Dashboard web con backend en Flask. A diferencia del HTML "standalone" original,
esta versión permite **subir el archivo .xlsm directamente desde el navegador**
y el dashboard se actualiza solo — sin pasar por Google Sheets.

## Cómo funciona

1. El usuario sube el `.xlsm`/`.xlsx` (hoja `PAC_III_MOD`) desde el panel superior del dashboard.
2. El backend (`parser.py`) lo lee con `openpyxl`, normaliza texto (MODALIDAD, FUENTE FINANCIA.),
   parsea fechas y montos, y guarda el resultado en `data/current.json`.
3. El frontend (`templates/index.html`) consulta `/api/data` y pinta KPIs, tabla mensual,
   gráficos (donut, barras apiladas, Procedimientos de Contratación, Modalidad) y alertas.
4. Cada vez que se sube un nuevo archivo, todo el dashboard se recalcula automáticamente.

## Correr localmente

```bash
pip install -r requirements.txt
python app.py
# abre http://localhost:5000
```

## Desplegar en Render (gratis)

1. Crea un repositorio en GitHub y sube esta carpeta completa (`app.py`, `parser.py`,
   `templates/`, `requirements.txt`, `Procfile`, `render.yaml`).
2. Entra a https://render.com → **New +** → **Web Service**.
3. Conecta tu repositorio de GitHub.
4. Render detecta el `render.yaml` automáticamente (o configura a mano):
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
   - **Plan:** Free
5. **Importante — persistencia de datos:** el plan gratis de Render usa disco
   efímero (se borra en cada redeploy). Si vas a subir el Excel con frecuencia
   eso no es problema porque simplemente subes de nuevo el archivo después de
   cada redeploy. Si quieres que el último archivo subido sobreviva reinicios
   del servidor (no solo redeploys), agrega un **Disk** en Render (plan pagado,
   $1/mes por 1GB) apuntando a `/opt/render/project/src/data` — el `render.yaml`
   ya lo deja configurado, solo actívalo desde el dashboard de Render si decides
   pagarlo.
6. Dale **Create Web Service**. En unos 2-3 minutos tendrás una URL pública
   tipo `https://pac-2026-ineter.onrender.com`.
7. Entra a esa URL, sube el `.xlsm` desde el panel de "Actualizar datos", y listo.

## Actualizar los datos después de desplegado

Solo entra a la URL pública, usa el botón **"Subir y actualizar"**, selecciona
el `.xlsm` más reciente. No necesitas volver a desplegar ni tocar código.

## Estructura de archivos

```
app.py              → servidor Flask (rutas: /, /api/data, /upload)
parser.py           → lee el .xlsm y normaliza los datos
templates/index.html → dashboard (HTML + CSS + JS con Chart.js)
data/current.json   → último set de datos procesado (se genera solo)
requirements.txt    → dependencias Python
Procfile            → comando de arranque para Render
render.yaml         → configuración de despliegue
```
