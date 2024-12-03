from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import json

# Initialize the database
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # Load database config from JSON file
    with open('connect_main.json', 'r') as file:
        config = json.load(file)["postgres_sql"]

    user = config["User"]
    password = config["Password"]
    host = config["IPAddress"]
    port = config["Port"]
    database = "databaseprod_987y"  # Replace with your actual database name

    # Configure the app
    app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{user}:{password}@{host}:{port}/{database}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions
    db.init_app(app)

    # Register blueprints (routes)
    from app.routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
