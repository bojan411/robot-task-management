from sqlalchemy.orm import Mapped, mapped_column

from robot_task_management.flask_apps import sa
from robot_task_management.models import TimestampedModel
from robot_task_management.models.robots import Robots
from robot_task_management.models.robot_tasks import RobotTasks


class RobotTaskExecutions(sa.Model, TimestampedModel):
    __tablename__ = "robot_task_executions"

    robot_id: Mapped[int] = mapped_column(sa.ForeignKey("robots.id"), nullable=False)
    task_id: Mapped[int] = mapped_column(
        sa.ForeignKey("robot_tasks.id"), nullable=False
    )
    robot: Mapped[Robots] = sa.relationship(back_populates="robot_task_executions")
    task: Mapped[RobotTasks] = sa.relationship(back_populates="robot_task_executions")
