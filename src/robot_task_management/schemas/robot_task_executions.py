from robot_task_management.flask_apps import ma
from marshmallow_sqlalchemy import fields
from robot_task_management.models.robot_task_executions import RobotTaskExecutions
from .robots import RobotsSchema
from .robot_tasks import RobotTasksSchema


class RobotTaskExecutionsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = RobotTaskExecutions
        load_instance = True
        include_relationships = True
        include_fk = True
        exclude = ("created_at", "updated_at")

    robot = fields.Nested(RobotsSchema, dump_only=True)
    task = fields.Nested(RobotTasksSchema, dump_only=True)
