from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from robot_task_management.flask_apps import sa
from robot_task_management.models import TimestampedModel
from robot_task_management.models.robot_tasks import RobotTasks


class RobotTaskType(sa.Model, TimestampedModel):
    __tablename__ = "robot_task_type"

    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    tasks: Mapped[RobotTasks] = sa.relationship(back_populates="task_type")
