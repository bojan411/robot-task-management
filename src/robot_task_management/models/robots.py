from sqlalchemy import String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from robot_task_management.flask_apps import sa
from robot_task_management.models.base import TimestampedModel


class Robots(sa.Model, TimestampedModel):
    __tablename__ = "robots"
    __table_args__ = (UniqueConstraint("name", name="unique_robot_name"),)

    name: Mapped[str] = mapped_column(String(50), nullable=False)
    robot_type_id: Mapped[int] = mapped_column(
        sa.ForeignKey("robot_type.id"), nullable=False, index=True
    )
    robot_type: Mapped["RobotType"] = sa.relationship(back_populates="robots")
    robot_task_executions: Mapped["RobotTaskExecutions"] = sa.relationship(
        back_populates="robot"
    )
