import os
import uuid
from pathlib import Path
from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.utils import secure_filename
import mysql.connector
from mysql.connector import Error
import sqlite3
from dotenv import load_dotenv

# Charger les variables d'environnement (.env)
load_dotenv()

try:
    import numpy as np
    from PIL import Image
    import tensorflow as tf
except Exception:
    np = None
    Image = None
    tf = None

BASE_DIR = Path(__file__).resolve().parent
UPLOAD_FOLDER = BASE_DIR / "static" / "uploads"
MODEL_PATH = BASE_DIR / "model" / "vgg16_skin_cancer.h5"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "change-this-secret-key")
app.config["UPLOAD_FOLDER"] = str(UPLOAD_FOLDER)
app.config["MAX_CONTENT_LENGTH"] = 8 * 1024 * 1024

_loaded_model = None
DB_CONFIG = {
    "host": "localhost",
    "user": "skin_app",
    "password": "1234",
    "database": "skin_cancer_db",
}


def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS





def login_required():
    if "user_id" not in session:
        flash("Veuillez vous connecter pour accéder au tableau de bord.", "warning")
        return False
    return True


def get_model():
    global _loaded_model
    if _loaded_model is None:
        if tf is None:
            raise RuntimeError("TensorFlow n'est pas installé. Installez requirements.txt ou activez le mode démo.")
        if not MODEL_PATH.exists():
            raise FileNotFoundError("Modèle introuvable : placez vgg16_skin_cancer.h5 dans le dossier model/.")
        _loaded_model = tf.keras.models.load_model(str(MODEL_PATH))
    return _loaded_model


def predict_image(image_path: Path):
    """
    Returns (result, probability, prediction_mode).
    Real mode uses VGG16 .h5 when available. Demo mode keeps the interface testable without the model.
    """
    demo_enabled = os.getenv("DEMO_MODE", "auto").lower() in {"1", "true", "yes", "auto"}

    try:
        model = get_model()
        if Image is None or np is None:
            raise RuntimeError("Pillow ou NumPy n'est pas installé.")

        image = Image.open(image_path).convert("RGB").resize((224, 224))
        arr = np.asarray(image, dtype="float32") / 255.0
        arr = np.expand_dims(arr, axis=0)
        pred = model.predict(arr, verbose=0)
        pred = np.asarray(pred).reshape(-1)

        if len(pred) == 1:
            malignant_probability = float(pred[0])
        else:
            # Common convention: index 1 = malignant. Adapt here if your model uses another order.
            malignant_probability = float(pred[1])

        malignant_probability = max(0.0, min(1.0, malignant_probability))
        result = "Malignant" if malignant_probability >= 0.5 else "Benign"
        probability = malignant_probability if result == "Malignant" else 1 - malignant_probability
        return result, round(probability * 100, 2), "VGG16"

    except Exception as exc:
        if not demo_enabled:
            raise exc

        # Deterministic demo fallback based on image brightness/contrast.
        # It is ONLY for interface testing and must not be used as a medical prediction.
        if Image is not None and np is not None:
            img = Image.open(image_path).convert("L").resize((80, 80))
            pixels = np.asarray(img, dtype="float32") / 255.0
            score = float(0.35 + (pixels.std() * 0.75) + (1 - pixels.mean()) * 0.20)
            score = max(0.12, min(0.92, score))
        else:
            score = 0.64
        result = "Malignant" if score >= 0.5 else "Benign"
        probability = score if result == "Malignant" else 1 - score
        return result, round(probability * 100, 2), "Démo interface"


@app.context_processor
def inject_globals():
    return {
        "current_year": datetime.now().year,
        "app_name": "Skin Cancer AI",
    }


@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        try:
            conn, db_type = get_db_connection()
            cursor = conn.cursor(dictionary=True) if db_type == "mysql" else conn.cursor()
            
            if db_type == "mysql":
                cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s LIMIT 1", (username, password))
                user = cursor.fetchone()
            else:
                cursor.execute("SELECT * FROM users WHERE username=? AND password=? LIMIT 1", (username, password))
                row = cursor.fetchone()
                user = dict(zip([c[0] for c in cursor.description], row)) if row else None
                
            cursor.close()
            conn.close()
        except Exception as err:
            flash(f"Erreur de connexion : {err}", "danger")
            return render_template("login.html", hide_nav=True)

        if user:
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            flash("Connexion réussie. Bienvenue dans votre espace d'analyse.", "success")
            return redirect(url_for("dashboard"))

        flash("Nom d'utilisateur ou mot de passe incorrect.", "danger")
    return render_template("login.html", hide_nav=True)


@app.route("/dashboard")
def dashboard():
    if not login_required():
        return redirect(url_for("login"))

    stats = {"patients": 0, "benign": 0, "malignant": 0, "avg_confidence": 0}
    recent_patients = []
    try:
        conn, db_type = get_db_connection()
        cursor = conn.cursor(dictionary=True) if db_type == "mysql" else conn.cursor()
        
        # Patients count
        cursor.execute("SELECT COUNT(*) AS total FROM patients")
        res = cursor.fetchone()
        stats["patients"] = res["total"] if db_type == "mysql" else res[0]
        
        # Benign count
        q = "SELECT COUNT(*) AS total FROM patients WHERE result=%s" if db_type == "mysql" else "SELECT COUNT(*) AS total FROM patients WHERE result=?"
        cursor.execute(q, ("Benign",))
        res = cursor.fetchone()
        stats["benign"] = res["total"] if db_type == "mysql" else res[0]
        
        # Malignant count
        cursor.execute(q, ("Malignant",))
        res = cursor.fetchone()
        stats["malignant"] = res["total"] if db_type == "mysql" else res[0]
        
        # Confidence
        cursor.execute("SELECT COALESCE(AVG(probability), 0) AS avg_confidence FROM patients")
        res = cursor.fetchone()
        stats["avg_confidence"] = round(float(res["avg_confidence"] if db_type == "mysql" else res[0]), 1)
        
        # Recent patients
        cursor.execute("SELECT * FROM patients ORDER BY created_at DESC LIMIT 5")
        if db_type == "mysql":
            recent_patients = cursor.fetchall()
        else:
            columns = [c[0] for c in cursor.description]
            recent_patients = [dict(zip(columns, row)) for row in cursor.fetchall()]
            
        cursor.close()
        conn.close()
    except Exception as err:
        flash(f"Impossible de charger les statistiques : {err}", "warning")

    return render_template("dashboard.html", stats=stats, recent_patients=recent_patients)


@app.route("/predict", methods=["GET", "POST"])
def predict():
    if not login_required():
        return redirect(url_for("login"))

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        age = request.form.get("age", "").strip()
        image_file = request.files.get("image")

        if not name or not age or not image_file:
            flash("Veuillez compléter tous les champs du formulaire.", "warning")
            return redirect(url_for("predict"))

        try:
            age = int(age)
            if age <= 0 or age > 120:
                raise ValueError
        except ValueError:
            flash("L'âge doit être un nombre valide entre 1 et 120.", "warning")
            return redirect(url_for("predict"))

        if image_file.filename == "" or not allowed_file(image_file.filename):
            flash("Format non accepté. Utilisez PNG, JPG, JPEG ou WEBP.", "danger")
            return redirect(url_for("predict"))

        UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)
        safe_name = secure_filename(image_file.filename)
        extension = safe_name.rsplit(".", 1)[1].lower()
        filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}.{extension}"
        saved_path = UPLOAD_FOLDER / filename
        image_file.save(saved_path)

        try:
            result, probability, prediction_mode = predict_image(saved_path)
            image_path = f"uploads/{filename}"

            conn, db_type = get_db_connection()
            cursor = conn.cursor()
            
            q = "INSERT INTO patients (name, age, result, probability, image_path) VALUES (%s, %s, %s, %s, %s)" if db_type == "mysql" else "INSERT INTO patients (name, age, result, probability, image_path) VALUES (?, ?, ?, ?, ?)"
            cursor.execute(q, (name, age, result, probability, image_path))
            
            conn.commit()
            cursor.close()
            conn.close()

            return render_template(
                "result.html",
                name=name,
                age=age,
                result=result,
                probability=probability,
                img=image_path,
                prediction_mode=prediction_mode,
            )
        except Exception as err:
            flash(f"Erreur pendant l'analyse : {err}", "danger")
            return redirect(url_for("predict"))

    return render_template("predict.html")

# --- CONFIGURATION BASE DE DONNÉES ---
# Identifiants Aiven (Cloud)
AIVEN_CONFIG = {
    'host': 'skin-cancer-db-skin-cancer-ai.h.aivencloud.com',
    'port': 16185,
    'user': 'avnadmin',
    'password': 'AVNS_KudJcEj6iBkr-sTogoU',
    'database': 'defaultdb'
}

# Identifiants Locaux (votre ordinateur)
LOCAL_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'skin_cancer_db'
}

_db_conn = None

def get_db_connection():
    """Tente Aiven d'abord, puis MySQL local, sinon SQLite. Utilise une connexion persistante."""
    global _db_conn
    
    # Si on a déjà une connexion et qu'elle est vivante, on la réutilise
    if _db_conn:
        try:
            if hasattr(_db_conn, 'is_connected') and _db_conn.is_connected():
                return _db_conn, "mysql"
            # Pour SQLite
            elif not hasattr(_db_conn, 'is_connected'):
                return _db_conn, "sqlite"
        except:
            _db_conn = None

    # 1. Tentative Aiven (Cloud)
    try:
        conn = mysql.connector.connect(**AIVEN_CONFIG)
        # Création des tables... (on garde la logique au cas où)
        _db_conn = conn
        return _db_conn, "mysql"
    except Exception as e:
        print(f"📡 Aiven indisponible, tentative local... {e}")

    # 2. Tentative MySQL Local
    try:
        conn = mysql.connector.connect(**LOCAL_CONFIG)
        return conn, "mysql"
    except Exception as e:
        print(f"⚠️ MySQL Local indisponible, bascule sur SQLite... {e}")
        
    # 3. Bascule SQLite (Dernier recours)
    db_path = '/tmp/database.db' if os.path.exists('/tmp') else 'database.db'
    conn = sqlite3.connect(db_path, check_same_thread=False)
    # (Le reste du code SQLite est géré automatiquement par la structure existante)
    return conn, "sqlite"

def execute_query(query, params=(), is_select=True):
    conn, db_type = get_db_connection()
    cursor = conn.cursor(dictionary=True) if db_type == "mysql" else conn.cursor()
    
    try:
        # Adapter la syntaxe SQL de %s vers ? pour SQLite
        if db_type == "sqlite":
            query = query.replace('%s', '?')
            
        cursor.execute(query, params)
        
        if is_select:
            if db_type == "sqlite":
                # Convertir les tuples SQLite en dictionnaires pour garder la compatibilité
                columns = [column[0] for column in cursor.description]
                result = [dict(zip(columns, row)) for row in cursor.fetchall()]
            else:
                result = cursor.fetchall()
            return result
        else:
            conn.commit()
            return cursor.lastrowid
    finally:
        conn.close()


@app.route("/patients")
def patients():
    if not login_required():
        return redirect(url_for("login"))

    rows = []
    try:
        conn, db_type = get_db_connection()
        cursor = conn.cursor(dictionary=True) if db_type == "mysql" else conn.cursor()
        cursor.execute("SELECT * FROM patients ORDER BY created_at DESC")
        
        if db_type == "mysql":
            rows = cursor.fetchall()
        else:
            columns = [c[0] for c in cursor.description]
            rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
            
        cursor.close()
        conn.close()
    except Exception as err:
        flash(f"Erreur lors du chargement des patients : {err}", "danger")

    return render_template("patients.html", patients=rows)


@app.route("/logout")
def logout():
    session.clear()
    flash("Session fermée avec succès.", "info")
    return redirect(url_for("login"))


if __name__ == "__main__":
    UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)
    app.run(debug=True)
