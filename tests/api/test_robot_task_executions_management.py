import json
import pytest
from tests.factories import RobotsFactory, RobotTasksFactory, RobotTaskExecutionsFactory


def test_get_executions__succeeds(client):
    response = client.get("/robot_task_executions/")
    assert response.status_code == 200
    assert isinstance(response.json, list)


@pytest.mark.usefixtures("app_ctx")
def test_create_execution__succeeds(client, robot, robot_task):
    data = {
        "robot_id": robot.id,
        "task_id": robot_task.id,
    }

    response = client.post(
        "/robot_task_executions/",
        data=json.dumps(data),
        content_type="application/json",
    )

    assert response.status_code == 201
    assert response.json["robot_id"] == robot.id
    assert response.json["task_id"] == robot_task.id


@pytest.mark.usefixtures("app_ctx")
def test_filter_executions_by_robot__succeeds(client, robot, robot_task):
    RobotTaskExecutionsFactory.create_batch(3, robot_id=robot.id, task_id=robot_task.id)
    response = client.get(f"/robot_task_executions/?robot_id={robot.id}")
    assert response.status_code == 200
    assert len(response.json) >= 3
    assert all(exec["robot_id"] == robot.id for exec in response.json)


@pytest.mark.usefixtures("app_ctx")
def test_filter_executions_by_task__succeeds(client, robot, robot_task):
    RobotTaskExecutionsFactory.create_batch(3, robot_id=robot.id, task_id=robot_task.id)

    response = client.get(f"/robot_task_executions/?robot_task_id={robot_task.id}")
    assert response.status_code == 200
    assert len(response.json) >= 3
    assert all(exec["task_id"] == robot_task.id for exec in response.json)


@pytest.mark.usefixtures("app_ctx")
def test_filter_executions_by_robot_type__succeeds(client, robot_type):
    robots = RobotsFactory.create_batch(2, robot_type_id=robot_type.id)
    task = RobotTasksFactory()

    for robot in robots:
        RobotTaskExecutionsFactory.create_batch(2, robot_id=robot.id, task_id=task.id)

    response = client.get(f"/robot_task_executions/?robot_type_id={robot_type.id}")
    assert response.status_code == 200
    assert len(response.json) >= 4


@pytest.mark.usefixtures("app_ctx")
def test_filter_executions_by_task_type__succeeds(client, robot_task_type):
    tasks = RobotTasksFactory.create_batch(2, task_type_id=robot_task_type.id)
    robot = RobotsFactory()
    for task in tasks:
        RobotTaskExecutionsFactory.create_batch(2, robot_id=robot.id, task_id=task.id)

    response = client.get(
        f"/robot_task_executions/?robot_task_type_id={robot_task_type.id}"
    )
    assert response.status_code == 200
    assert len(response.json) >= 4


@pytest.mark.usefixtures("app_ctx")
def test_filter_executions_with_multiple_filters__succeeds(
    client, robot_type, robot_task_type
):
    robots = RobotsFactory.create_batch(2, robot_type_id=robot_type.id)
    another_robot = RobotsFactory()

    tasks = RobotTasksFactory.create_batch(2, task_type_id=robot_task_type.id)
    another_task = RobotTasksFactory()

    for robot in robots:
        for task in tasks:
            RobotTaskExecutionsFactory.create_batch(
                1, robot_id=robot.id, task_id=task.id
            )

    # This will not match filters
    RobotTaskExecutionsFactory.create_batch(
        2, robot_id=another_robot.id, task_id=tasks[0].id
    )
    RobotTaskExecutionsFactory.create_batch(
        2, robot_id=robots[0].id, task_id=another_task.id
    )

    response = client.get(
        f"/robot_task_executions/?robot_type_id={robot_type.id}&robot_task_type_id={robot_task_type.id}"
    )
    assert response.status_code == 200

    expected_execution_count_based_on_filter = 4
    assert len(response.json) == expected_execution_count_based_on_filter

    for execution in response.json:
        assert execution["robot_id"] in [robot.id for robot in robots]
        assert execution["task_id"] in [task.id for task in tasks]
