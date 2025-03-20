import factory
from factory.alchemy import SQLAlchemyModelFactory
from datetime import datetime
from zoneinfo import ZoneInfo

from robot_task_management.flask_apps import sa
from robot_task_management.models.robots import Robots
from robot_task_management.models.robot_type import RobotType
from robot_task_management.models.robot_tasks import RobotTasks
from robot_task_management.models.robot_task_type import RobotTaskType
from robot_task_management.models.robot_task_executions import RobotTaskExecutions


class BaseFactory(SQLAlchemyModelFactory):
    class Meta:
        abstract = True
        sqlalchemy_session = sa.session
        sqlalchemy_session_persistence = "commit"


class RobotTypeFactory(BaseFactory):
    class Meta:
        model = RobotType

    name = factory.Sequence(lambda n: f"Robot Type {n}")
    created_at = datetime.now(tz=ZoneInfo("UTC"))
    updated_at = datetime.now(tz=ZoneInfo("UTC"))


class RobotsFactory(BaseFactory):
    class Meta:
        model = Robots

    name = factory.Sequence(lambda n: f"Robot {n}")
    robot_type = factory.SubFactory(RobotTypeFactory)
    created_at = datetime.now(tz=ZoneInfo("UTC"))
    updated_at = datetime.now(tz=ZoneInfo("UTC"))


class RobotTaskTypeFactory(BaseFactory):
    class Meta:
        model = RobotTaskType

    name = factory.Sequence(lambda n: f"Task Type {n}")
    created_at = datetime.now(tz=ZoneInfo("UTC"))
    updated_at = datetime.now(tz=ZoneInfo("UTC"))


class RobotTasksFactory(BaseFactory):
    class Meta:
        model = RobotTasks

    name = factory.Sequence(lambda n: f"Task {n}")
    task_type = factory.SubFactory(RobotTaskTypeFactory)
    created_at = datetime.now(tz=ZoneInfo("UTC"))
    updated_at = datetime.now(tz=ZoneInfo("UTC"))


class RobotTaskExecutionsFactory(BaseFactory):
    class Meta:
        model = RobotTaskExecutions

    robot = factory.SubFactory(RobotsFactory)
    task = factory.SubFactory(RobotTasksFactory)
    created_at = datetime.now(tz=ZoneInfo("UTC"))
    updated_at = datetime.now(tz=ZoneInfo("UTC"))
