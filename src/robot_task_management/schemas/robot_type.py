from robot_task_management import ma
from robot_task_management.models.robot_type import RobotType


class RobotTypeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = RobotType
        load_instance = True
        include_fk = True
        exclude = ("created_at", "updated_at")
