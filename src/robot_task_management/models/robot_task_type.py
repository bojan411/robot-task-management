from sqlalchemy import String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from robot_task_management.flask_apps import sa
from robot_task_management.models.base import TimestampedModel


class RobotTaskType(sa.Model, TimestampedModel):
    __tablename__ = "robot_task_type"
    __table_args__ = (UniqueConstraint("name", name="unique_task_type_name"),)

    name: Mapped[str] = mapped_column(String(50), nullable=False)
    tasks: Mapped["RobotTasks"] = sa.relationship(back_populates="task_type")
