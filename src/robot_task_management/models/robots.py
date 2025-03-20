from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from robot_task_management.flask_apps import sa
from robot_task_management.models import TimestampedModel
from robot_task_management.models.robot_type import RobotType
from robot_task_management.models.robot_task_executions import RobotTaskExecutions


class Robots(sa.Model, TimestampedModel):
    __tablename__ = "robots"

    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    robot_type_id: Mapped[int] = mapped_column(
        sa.ForeignKey("robot_type.id"), nullable=False, index=True
    )
    robot_type: Mapped[RobotType] = sa.relationship(back_populates="robots")
    robot_task_executions: Mapped[RobotTaskExecutions] = sa.relationship(
        back_populates="robot"
    )
