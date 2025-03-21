import json
import pytest
from robot_task_management.models.robots import Robots
from robot_task_management.models.robot_type import RobotType
from tests.factories import RobotTypeFactory


def test_get_robots__succeeds(client):
    response = client.get("/robots/")
    assert response.status_code == 200
    assert isinstance(response.json, list)


@pytest.mark.usefixtures("app_ctx")
def test_create_robot__succeeds(client, robot_type):
    data = {"name": "Robot", "robot_type_id": robot_type.id}
    response = client.post(
        "/robots/", data=json.dumps(data), content_type="application/json"
    )
    assert response.status_code == 201
    assert response.json["name"] == "Robot"
    assert response.json["robot_type_id"] == robot_type.id


@pytest.mark.usefixtures("app_ctx")
def test_create_robot__already_exists(client, robot):
    data = {"name": robot.name, "robot_type_id": robot.robot_type.id}
    response = client.post(
        "/robots/", data=json.dumps(data), content_type="application/json"
    )

    assert response.status_code == 400
    assert "Robot already exists" in response.json["message"]


@pytest.mark.usefixtures("app_ctx")
def test_get_robot__succeeds(client, robot):
    response = client.get(f"/robots/{robot.id}")
    assert response.status_code == 200
    assert response.json["name"] == "Test robot"


@pytest.mark.usefixtures("app_ctx")
def test_update_robot__succeeds(client, robot, robot_type):
    data = {"name": "Updated robot", "robot_type_id": robot_type.id}
    response = client.put(
        f"/robots/{robot.id}", data=json.dumps(data), content_type="application/json"
    )
    assert response.status_code == 200
    assert response.json["name"] == "Updated robot"


@pytest.mark.usefixtures("app_ctx")
def test_delete_robot__succeeds(client, robot, db):
    response = client.delete(f"/robots/{robot.id}")
    assert response.status_code == 204

    deleted_robot = db.session.get(Robots, robot.id)
    assert deleted_robot is None


def test_get_robot_types__succeeds(client):
    response = client.get("/robots/types")
    assert response.status_code == 200
    assert isinstance(response.json, list)


@pytest.mark.usefixtures("app_ctx")
def test_create_robot_type__succeeds(client):
    data = {"name": "Robot type"}
    response = client.post(
        "/robots/types", data=json.dumps(data), content_type="application/json"
    )
    assert response.status_code == 201
    assert response.json["name"] == "Robot type"


@pytest.mark.usefixtures("app_ctx")
def test_create_robot_type__already_exists(client, robot_type):
    data = {"name": robot_type.name}
    response = client.post(
        "/robots/types", data=json.dumps(data), content_type="application/json"
    )
    assert response.status_code == 400
    assert "Robot type already exists" in response.json["message"]


@pytest.mark.usefixtures("app_ctx")
def test_get_robot_type__succeeds(client, robot_type):
    response = client.get(f"/robots/types/{robot_type.id}")
    assert response.status_code == 200
    assert response.json["name"] == "Test robot type"


@pytest.mark.usefixtures("app_ctx")
def test_update_robot_type__succeeds(client, robot_type):
    data = {"name": "Updated robot type"}
    response = client.put(
        f"/robots/types/{robot_type.id}",
        data=json.dumps(data),
        content_type="application/json",
    )
    assert response.status_code == 200
    assert response.json["name"] == "Updated robot type"


@pytest.mark.usefixtures("app_ctx")
def test_delete_robot_type__succeeds(client, db):
    robot_type = RobotTypeFactory(name="Another test robot type")

    response = client.delete(f"/robots/types/{robot_type.id}")
    assert response.status_code == 204

    deleted_robot_type = db.session.get(RobotType, robot_type.id)
    assert deleted_robot_type is None
