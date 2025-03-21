import json
import pytest
from robot_task_management.models.robot_task_type import RobotTaskType
from tests.factories import RobotTaskTypeFactory


def test_get_robot_tasks__succeeds(client):
    response = client.get("/robot_tasks/")
    assert response.status_code == 200
    assert isinstance(response.json, list)


@pytest.mark.usefixtures("app_ctx")
def test_create_robot_task__succeeds(client, robot_task_type):
    data = {"name": "New task", "task_type_id": robot_task_type.id}
    response = client.post(
        "/robot_tasks/", data=json.dumps(data), content_type="application/json"
    )

    assert response.status_code == 201
    assert response.json["name"] == "New task"
    assert response.json["task_type_id"] == robot_task_type.id


@pytest.mark.usefixtures("app_ctx")
def test_create_robot_task__already_exists(client, robot_task):
    data = {"name": robot_task.name, "task_type_id": robot_task.task_type.id}
    response = client.post(
        "/robot_tasks/", data=json.dumps(data), content_type="application/json"
    )
    assert response.status_code == 400
    assert "Robot task already exists" in response.json["message"]


@pytest.mark.usefixtures("app_ctx")
def test_get_robot_task__succeeds(client, robot_task):
    response = client.get(f"/robot_tasks/{robot_task.id}")
    assert response.status_code == 200
    assert response.json["name"] == "Test task"


@pytest.mark.usefixtures("app_ctx")
def test_update_robot_task__succeeds(client, robot_task, robot_task_type):
    data = {"name": "Updated task", "task_type_id": robot_task_type.id}
    response = client.put(
        f"/robot_tasks/{robot_task.id}",
        data=json.dumps(data),
        content_type="application/json",
    )
    assert response.status_code == 200
    assert response.json["name"] == "Updated task"


@pytest.mark.usefixtures("app_ctx")
def test_delete_robot_task__succeeds(client, robot_task):
    response = client.delete(f"/robot_tasks/{robot_task.id}")
    assert response.status_code == 204


@pytest.mark.usefixtures("app_ctx")
def test_get_robot_task_types__succeeds(client):
    response = client.get("/robot_tasks/types")
    assert response.status_code == 200
    assert isinstance(response.json, list)


def test_create_robot_task_type__succeeds(client):
    data = {"name": "New task type"}
    response = client.post(
        "/robot_tasks/types", data=json.dumps(data), content_type="application/json"
    )
    assert response.status_code == 201
    assert response.json["name"] == "New task type"


@pytest.mark.usefixtures("app_ctx")
def test_create_robot_task_type__already_exists(client, robot_task_type):
    data = {"name": robot_task_type.name}
    response = client.post(
        "/robot_tasks/types", data=json.dumps(data), content_type="application/json"
    )
    assert response.status_code == 400
    assert "Robot task type already exists" in response.json["message"]


@pytest.mark.usefixtures("app_ctx")
def test_get_robot_task_type__succeeds(client, robot_task_type):
    response = client.get(f"/robot_tasks/types/{robot_task_type.id}")
    assert response.status_code == 200
    assert response.json["name"] == "Test task type"


@pytest.mark.usefixtures("app_ctx")
def test_update_robot_task_type__succeeds(client, robot_task_type):
    data = {"name": "Updated task type"}
    response = client.put(
        f"/robot_tasks/types/{robot_task_type.id}",
        data=json.dumps(data),
        content_type="application/json",
    )
    assert response.status_code == 200
    assert response.json["name"] == "Updated task type"


@pytest.mark.usefixtures("app_ctx")
def test_delete_robot_task_type__succeeds(client, db):
    robot_task_type = RobotTaskTypeFactory(name="Another robot task type")

    response = client.delete(f"/robot_tasks/types/{robot_task_type.id}")
    assert response.status_code == 204

    deleted_robot_task_type = db.session.get(RobotTaskType, robot_task_type.id)
    assert deleted_robot_task_type is None
