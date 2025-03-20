from robot_task_management import ma
from robot_task_management.models.robot_task_type import RobotTaskType


class RobotTaskTypeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = RobotTaskType
        load_instance = True
        include_fk = True
        exclude = ("created_at", "updated_at")
