import factory
from factory.alchemy import SQLAlchemyModelFactory
from datetime import datetime
from zoneinfo import ZoneInfo

from robot_task_management.models.robots import Robots
from robot_task_management.models.robot_type import RobotType
from robot_task_management.models.robot_tasks import RobotTasks
from robot_task_management.models.robot_task_type import RobotTaskType
from robot_task_management.models.robot_task_executions import RobotTaskExecutions


def init_factories(session):
    RobotTypeFactory._meta.sqlalchemy_session = session
    RobotsFactory._meta.sqlalchemy_session = session
    RobotTaskTypeFactory._meta.sqlalchemy_session = session
    RobotTasksFactory._meta.sqlalchemy_session = session
    RobotTaskExecutionsFactory._meta.sqlalchemy_session = session


class RobotTypeFactory(SQLAlchemyModelFactory):
    class Meta:
        model = RobotType
        sqlalchemy_session_persistence = "commit"

    name = factory.Sequence(lambda n: f"Robot Type {n}")
    created_at = datetime.now(tz=ZoneInfo("UTC"))
    updated_at = datetime.now(tz=ZoneInfo("UTC"))


class RobotsFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Robots
        sqlalchemy_session_persistence = "commit"

    name = factory.Sequence(lambda n: f"Robot {n}")
    robot_type_id = factory.Faker("random_int", min=1, max=100)
    created_at = datetime.now(tz=ZoneInfo("UTC"))
    updated_at = datetime.now(tz=ZoneInfo("UTC"))


class RobotTaskTypeFactory(SQLAlchemyModelFactory):
    class Meta:
        model = RobotTaskType
        sqlalchemy_session_persistence = "commit"

    name = factory.Sequence(lambda n: f"Task Type {n}")
    created_at = datetime.now(tz=ZoneInfo("UTC"))
    updated_at = datetime.now(tz=ZoneInfo("UTC"))


class RobotTasksFactory(SQLAlchemyModelFactory):
    class Meta:
        model = RobotTasks
        sqlalchemy_session_persistence = "commit"

    name = factory.Sequence(lambda n: f"Task {n}")
    task_type_id = factory.Faker("random_int", min=1, max=100)
    created_at = datetime.now(tz=ZoneInfo("UTC"))
    updated_at = datetime.now(tz=ZoneInfo("UTC"))


class RobotTaskExecutionsFactory(SQLAlchemyModelFactory):
    class Meta:
        model = RobotTaskExecutions
        sqlalchemy_session_persistence = "commit"

    robot_id = factory.Faker("random_int", min=1, max=100)
    task_id = factory.Faker("random_int", min=1, max=100)
    created_at = datetime.now(tz=ZoneInfo("UTC"))
    updated_at = datetime.now(tz=ZoneInfo("UTC"))
