from sqlalchemy import String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from robot_task_management.flask_apps import sa
from robot_task_management.models.base import TimestampedModel


class RobotTasks(sa.Model, TimestampedModel):
    __tablename__ = "robot_tasks"
    __table_args__ = (UniqueConstraint("name", name="unique_task_name"),)

    name: Mapped[str] = mapped_column(String(200), nullable=False)
    task_type_id: Mapped[int] = mapped_column(
        sa.ForeignKey("robot_task_type.id"), nullable=False, index=True
    )
    task_type: Mapped["RobotTaskType"] = sa.relationship(back_populates="tasks")
    robot_task_executions: Mapped["RobotTaskExecutions"] = sa.relationship(
        back_populates="task"
    )
