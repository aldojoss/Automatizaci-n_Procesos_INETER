import json
import os
from datetime import datetime
from functools import wraps

from flask import Flask, jsonify, redirect, render_template, request, session, url_for

from parser import parse_workbook

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
DATA_FILE = os.path.join(DATA_DIR, "current.json")
os.makedirs(DATA_DIR, exist_ok=True)

MAX_UPLOAD_MB = 15
app.config["MAX_CONTENT_LENGTH"] = MAX_UPLOAD_MB * 1024 * 1024

# autenticacion
# la contra se lee de la clave de entorno,
# .
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev-secret-cambia-esto-en-produccion")
DASHBOARD_PASSWORD = os.environ.get("DASHBOARD_PASSWORD")


def login_required(view_func):
    @wraps(view_func)
    def wrapped(*args, **kwargs):
        if not session.get("authenticated"):
            return redirect(url_for("login"))
        return view_func(*args, **kwargs)
    return wrapped


@app.route("/login", methods=["GET", "POST"])
def login():
    if not DASHBOARD_PASSWORD:
        # si no se configuró contraseña ,
        # no bloqueamos el acceso para no romper el flujo local.
        session["authenticated"] = True
        return redirect(url_for("index"))

    if request.method == "POST":
        if request.form.get("password") == DASHBOARD_PASSWORD:
            session["authenticated"] = True
            return redirect(url_for("index"))
        return render_template("login.html", error="Contraseña incorrecta."), 401

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


def load_current_data():
    if not os.path.exists(DATA_FILE):
        return {"records": [], "updatedAt": None, "fileName": None}
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_current_data(records, file_name):
    payload = {
        "records": records,
        "updatedAt": datetime.utcnow().isoformat() + "Z",
        "fileName": file_name,
    }
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False)
    return payload


@app.route("/")
@login_required
def index():
    return render_template("index.html")


@app.route("/api/data")
@login_required
def api_data():
    return jsonify(load_current_data())


@app.route("/upload", methods=["POST"])
@login_required
def upload():
    if "file" not in request.files:
        return jsonify({"ok": False, "error": "No se recibió ningún archivo."}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"ok": False, "error": "Nombre de archivo vacío."}), 400

    if not file.filename.lower().endswith((".xlsm", ".xlsx")):
        return jsonify({"ok": False, "error": "Solo se aceptan archivos .xlsm o .xlsx."}), 400

    tmp_path = os.path.join(DATA_DIR, "_upload_tmp.xlsm")
    file.save(tmp_path)

    try:
        records = parse_workbook(tmp_path)
    except Exception as exc:  # noqa: BLE001
        return jsonify({"ok": False, "error": f"No se pudo leer el archivo: {exc}"}), 400
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)

    if not records:
        return jsonify({"ok": False, "error": "El archivo se leyó pero no se encontraron filas de datos."}), 400

    payload = save_current_data(records, file.filename)
    return jsonify({"ok": True, "count": len(records), "updatedAt": payload["updatedAt"]})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    # use_reloader=false si no, el servidor se reinicia solo
    # cada vez que se sube un archivo (porque el upload escribe data/current.json
    # dentro de la carpeta del proyecto, y el reloader lo detecta como cambio de
    # código), cortando la conexión a mitad de la subida.
    app.run(host="0.0.0.0", port=port, debug=True, use_reloader=False)
