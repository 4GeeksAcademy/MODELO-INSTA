"""
This module takes care of starting the API Server, loading the DB and adding the endpoints.
"""
import os
from flask import Flask, jsonify
from flask_migrate import Migrate
from flask_cors import CORS
from admin import setup_admin
from models import db, User
from utils import APIException, generate_sitemap

app = Flask(__name__)
app.url_map.strict_slashes = False

# Configuración de la base de datos
db_url = os.getenv("DATABASE_URL")
if db_url:
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url.replace("postgres://", "postgresql://")
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////tmp/test.db"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Extensiones
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Manejo de errores en JSON
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# Sitemap de endpoints
@app.route("/")
def sitemap():
    return generate_sitemap(app)

# Endpoint de ejemplo
@app.route("/user", methods=["GET"])
def handle_hello():
    return jsonify({"msg": "Hello, this is your GET /user response "}), 200

# Ejecutar el servidor
if __name__ == "__main__":
    PORT = int(os.environ.get("PORT", 3000))
    app.run(host="0.0.0.0", port=PORT, debug=False)
