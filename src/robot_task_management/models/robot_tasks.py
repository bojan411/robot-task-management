from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from robot_task_management.flask_apps import sa
from robot_task_management.models import TimestampedModel
from robot_task_management.models.robot_task_type import RobotTaskType
from robot_task_management.models.robot_task_executions import RobotTaskExecutions


class RobotTasks(sa.Model, TimestampedModel):
    __tablename__ = "robot_tasks"

    name: Mapped[str] = mapped_column(String(200), nullable=False, unique=True)
    task_type_id: Mapped[int] = mapped_column(
        sa.ForeignKey("robot_task_type.id"), nullable=False, index=True
    )
    task_type: Mapped[RobotTaskType] = sa.relationship(back_populates="tasks")
    robot_task_executions: Mapped[RobotTaskExecutions] = sa.relationship(
        back_populates="task"
    )
