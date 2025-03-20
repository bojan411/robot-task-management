from robot_task_management import ma
from robot_task_management.models.robots import Robots


class RobotsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Robots
        load_instance = True
        include_relationships = True
        include_fk = True
        exclude = ("created_at", "updated_at")
