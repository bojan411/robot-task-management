from robot_task_management.flask_apps import ma
from robot_task_management.models.robot_task_executions import RobotTaskExecutions


class RobotTaskExecutionsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = RobotTaskExecutions
        load_instance = True
        include_relationships = True
        include_fk = True
        exclude = ("created_at", "updated_at")
