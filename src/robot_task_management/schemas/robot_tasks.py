from robot_task_management import ma
from marshmallow_sqlalchemy import fields
from robot_task_management.models.robot_tasks import RobotTasks
from robot_task_management.schemas.robot_task_type import RobotTaskTypeSchema


class RobotTasksSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = RobotTasks
        load_instance = True
        include_relationships = True
        include_fk = True
        exclude = ("created_at", "updated_at")

    task_type = fields.Nested(RobotTaskTypeSchema, dump_only=True)
