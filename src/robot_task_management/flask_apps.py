from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_restx import Api
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


sa = SQLAlchemy(model_class=Base)
migrate = Migrate()
ma = Marshmallow()
restx_api = Api(
    title="Robot task management API",
    version="0.1.0",
    description="API for managing robots",
    doc="/docs",
)
