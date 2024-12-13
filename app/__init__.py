from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import json
import os

# Initialize the database
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # Load database config from JSON file
    with open('connect_main.json', 'r') as file:
        config = json.load(file)["postgres_sql"]

    user = os.getenv("USER", "default_user")
    password = os.getenv("PASSWORD", "default_password")
    host = os.getenv("IPADDRESS", "localhost")
    port = os.getenv("PORT", "5432")
    database = "databaseprod_987y"
    sslmode = "require"
    # Configure the app
    app.config['SQLALCHEMY_DATABASE_URI'] = (
        f"postgresql://{user}:{password}@{host}:{port}/{database}?sslmode=require"
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions
    db.init_app(app)

    # Register blueprints (routes)
    from app.routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
