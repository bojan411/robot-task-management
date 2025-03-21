import os
from flask import Flask
from dotenv import load_dotenv

from .flask_apps import sa, ma, migrate, restx_api
from .api import robots_api, robot_tasks_api, robot_task_executions_api


load_dotenv()


def create_app(is_testing=True):
    app = Flask(__name__)

    config_app(app, is_testing)

    sa.init_app(app)
    migrate.init_app(app, sa)
    ma.init_app(app)
    restx_api.init_app(app)

    restx_api.add_namespace(robots_api)
    restx_api.add_namespace(robot_tasks_api)
    restx_api.add_namespace(robot_task_executions_api)

    with app.app_context():
        sa.create_all()

    return app


def config_app(app: Flask, is_testing: bool):
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "some_secret_key")
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "some_secret_key")
    if is_testing:
        app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("TEST_DATABASE_URL")
        app.config["TESTING"] = True
    else:
        app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["RESTX_MASK_SWAGGER"] = (
        os.getenv("RESTX_MASK_SWAGGER", "False").lower() == "false"
    )
    app.config["RESTX_ERROR_404_HELP"] = (
        os.getenv("RESTX_ERROR_404_HELP", "False").lower() == "true"
    )
