from robot_task_management import ma
from marshmallow_sqlalchemy import fields
from robot_task_management.models.robots import Robots
from robot_task_management.schemas.robot_type import RobotTypeSchema


class RobotsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Robots
        load_instance = True
        include_relationships = True
        include_fk = True
        exclude = ("created_at", "updated_at")

    robot_type = fields.Nested(RobotTypeSchema, dump_only=True)
