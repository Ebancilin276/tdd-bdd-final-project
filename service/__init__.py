"""
Service Package - Flask Application Factory
"""
import os
from flask import Flask
from service.models import db, Product

app = Flask(__name__)

# Configuration
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
    "DATABASE_URI", "sqlite:///test.db"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "supersecretkey"

db.init_app(app)

# Import routes after app is created to avoid circular imports
from service import routes  # noqa: F401, E402
