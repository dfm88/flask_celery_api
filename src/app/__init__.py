import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.config import Config
from dotenv import load_dotenv
from flask_migrate import Migrate
from flask_migrate import upgrade



db = SQLAlchemy()

def create_app(config_class=Config) -> Flask:
    """
    Pluggable function to create different instances
    of the app with different configuration classes
    """
    load_dotenv()
    app = Flask(__name__)
    app.config.from_object(config_class)

    Migrate(app, db)
    db.init_app(app)
    # migrate.init_app(app, db)

    # blueprint init
    from app.main.routes import main
    app.register_blueprint(main)

    return app