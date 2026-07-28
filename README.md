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

## Acceso con contraseña

El dashboard está protegido con una contraseña única (no hay usuarios, es solo
una llave compartida). Se configura con dos variables de entorno:

- `DASHBOARD_PASSWORD`: la contraseña para entrar.
- `FLASK_SECRET_KEY`: clave para firmar la sesión (pon cualquier texto largo y aleatorio).

Si se define `DASHBOARD_PASSWORD`, el dashboard queda abierto (útil solo para
desarrollo local). **En producción (Render) siempre debes configurarla.**



## Correr localmente

```bash
pip install -r requirements.txt
export DASHBOARD_PASSWORD=tu-contraseña
export FLASK_SECRET_KEY=una-clave-larga-y-aleatoria
python app.py
# abre http://localhost:5000
```

