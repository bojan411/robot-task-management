from robot_task_management import ma
from robot_task_management.models.robot_tasks import RobotTasks


class RobotTasksSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = RobotTasks
        load_instance = True
        include_relationships = True
        include_fk = True
        exclude = ("created_at", "updated_at")
