# Seguimiento al PAC 2026 · INETER




## Acceso con contraseña

El dashboard está protegido con una contraseña única (no hay usuarios, es solo
una llave compartida). Se configura con dos variables de entorno:

- `DASHBOARD_PASSWORD`: la contraseña para entrar.
- `FLASK_SECRET_KEY`: clave para firmar la sesión (pon cualquier texto largo y aleatorio).

Si se define `DASHBOARD_PASSWORD`, el dashboard queda abierto (útil solo para
desarrollo local). **En rndr se configura**



## Correr localmente

```bash
pip install -r requirements.txt
export DASHBOARD_PASSWORD=tu-contraseña
export FLASK_SECRET_KEY=una-clave-larga-y-aleatoria
python app.py
# abre http://localhost:5000
```

