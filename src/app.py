"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, jsonify
from flask_migrate import Migrate
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Post, Comment, Follower
app = Flask(__name__)
app.url_map.strict_slashes = False

# inja database ro set mikonim (agar env nabashe -> sqlite)
db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url.replace("postgres://", "postgresql://")
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////tmp/instagram.db"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# init database
db.init_app(app)

# migrate baraye version control db
MIGRATE = Migrate(app, db)

CORS(app)
setup_admin(app)

# error handler
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# sitemap
@app.route("/")
def sitemap():
    return generate_sitemap(app)

# test route (bara inke مطمئن بشim server ok-e)
@app.route("/ping", methods=["GET"])
def ping():
    return jsonify({"msg": "pong ✅ Instagram models ready"}), 200

# IMPORTANT: force Flask to load all models before migrations/diagram
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    PORT = int(os.environ.get("PORT", 3000))
    app.run(host="0.0.0.0", port=PORT, debug=True)