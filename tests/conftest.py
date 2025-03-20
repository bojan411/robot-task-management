import pytest
from robot_task_management import create_app
from robot_task_management.flask_apps import sa
from tests.factories import (
    BaseFactory,
    RobotTypeFactory,
    RobotsFactory,
    RobotTaskTypeFactory,
    RobotTasksFactory,
    RobotTaskExecutionsFactory,
)


@pytest.fixture
def app():
    app = create_app(is_testing=True)

    with app.app_context():
        sa.create_all()

    BaseFactory._meta.sqlalchemy_session = sa.session

    yield app

    with app.app_context():
        sa.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def robot_type(app):
    with app.app_context():
        return RobotTypeFactory(name="Test robot type")


@pytest.fixture
def robot(app, robot_type):
    with app.app_context():
        return RobotsFactory(name="Test robot", robot_type=robot_type)


@pytest.fixture
def robot_task_type(app):
    with app.app_context():
        return RobotTaskTypeFactory(name="Test task type")


@pytest.fixture
def robot_task(app, robot_task_type):
    with app.app_context():
        return RobotTasksFactory(name="Test task", task_type=robot_task_type)


@pytest.fixture
def robot_task_execution(app, robot, robot_task):
    with app.app_context():
        return RobotTaskExecutionsFactory(robot=robot, task=robot_task)
