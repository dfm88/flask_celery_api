import os

from dotenv import load_dotenv

from flask import Flask

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from flask_celeryext import FlaskCeleryExt

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from project.celery_conf import build_celery
from project.config import config 


db = SQLAlchemy()
ext_celery = FlaskCeleryExt(create_celery_app=build_celery)


def create_app(config_name=None) -> Flask:
    """
    Pluggable function to create different instances
    of the app with different configuration classes
    """
    load_dotenv()

    if config_name is None:
        config_name = os.environ.get("FLASK_CONFIG", "development")

    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # if os.environ.get("SERVICE") == 'api':
    Migrate(app, db)
    db.init_app(app)
    # migrate.init_app(app, db)

    # blueprint init
    from project.main.routes import main_blueprint
    app.register_blueprint(main_blueprint)

    # admin
    from project.main.models import Restaurant, Address, Info, ChildView
    admin = Admin(app)
    admin.add_view(ChildView(Restaurant, db.session))
    admin.add_view(ModelView(Address, db.session))
    admin.add_view(ModelView(Info, db.session))

    # shell context for flask cli
    @app.shell_context_processor
    def ctx():
        return {"app": app, "db": db}

    return app
