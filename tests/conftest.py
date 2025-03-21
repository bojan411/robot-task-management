import pytest
from robot_task_management import create_app
from robot_task_management.flask_apps import sa
from tests.factories import (
    RobotTypeFactory,
    RobotsFactory,
    RobotTaskTypeFactory,
    RobotTasksFactory,
    RobotTaskExecutionsFactory,
    init_factories,
)


@pytest.fixture
def app_ctx(app):
    with app.app_context():
        yield


@pytest.fixture
def db():
    yield sa


@pytest.fixture
def app():
    app = create_app(is_testing=True)

    with app.app_context():
        sa.create_all()
        init_factories(sa.session)

    yield app

    with app.app_context():
        sa.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
@pytest.mark.usefixtures("app_ctx")
def robot_type():
    return RobotTypeFactory(name="Test robot type")


@pytest.fixture
@pytest.mark.usefixtures("app_ctx")
def robot(robot_type):
    return RobotsFactory(name="Test robot", robot_type=robot_type)


@pytest.fixture
@pytest.mark.usefixtures("app_ctx")
def robot_task_type():
    return RobotTaskTypeFactory(name="Test task type")


@pytest.fixture
@pytest.mark.usefixtures("app_ctx")
def robot_task(robot_task_type):
    return RobotTasksFactory(name="Test task", task_type=robot_task_type)


@pytest.fixture
@pytest.mark.usefixtures("app_ctx")
def robot_task_execution(robot, robot_task):
    return RobotTaskExecutionsFactory(robot=robot, task=robot_task)
