from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from robot_task_management.flask_apps import sa
from robot_task_management.models import TimestampedModel
from robot_task_management.models.robots import Robots


class RobotType(sa.Model, TimestampedModel):
    __tablename__ = "robot_type"

    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    robots: Mapped[Robots] = sa.relationship(back_populates="robot_type")
