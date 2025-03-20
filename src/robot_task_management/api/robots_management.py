from flask import request
from flask_restx import Namespace, Resource, fields
from sqlalchemy.exc import IntegrityError

from robot_task_management.flask_apps import sa
from robot_task_management.models.robots import Robots
from robot_task_management.models.robot_type import RobotType
from robot_task_management.schemas.robots import RobotsSchema
from robot_task_management.schemas.robot_type import RobotTypeSchema

robots_api = Namespace("robots", description="Robot management")

# Swagger
robot_type_model = robots_api.model(
    "RobotType",
    {
        "id": fields.Integer(readonly=True, description="Robot type unique identifier"),
        "name": fields.String(required=True, description="Robot type unique name"),
    },
)

robots_model = robots_api.model(
    "Robots",
    {
        "id": fields.Integer(readonly=True, description="Robot unique identifier"),
        "name": fields.String(required=True, description="Robot unique name"),
        "robot_type_id": fields.Integer(
            required=True, description="Robot type identifier"
        ),
    },
)

robot_schema = RobotsSchema()
robots_schema = RobotsSchema(many=True)
robot_type_schema = RobotTypeSchema()
robot_types_schema = RobotTypeSchema(many=True)


@robots_api.route("/robots")
class RobotsResource(Resource):
    @robots_api.doc("list_robots")
    @robots_api.marshal_list_with(robots_model)
    def get(self):
        robots = Robots.query.all()
        return robots_schema.dump(robots)

    @robots_api.doc("create_robot")
    @robots_api.expect(robots_model)
    @robots_api.marshal_with(robots_model, code=201)
    def post(self):
        robot_data = request.json
        try:
            RobotType.query.get_or_404(robot_data["robot_type_id"])

            robot = robot_schema.load(robot_data)
            sa.session.add(robot)
            sa.session.commit()
            return robot_schema.dump(robot), 201
        except IntegrityError:
            sa.session.rollback()
            robots_api.abort(400, "Robot already exists")
        except Exception as e:
            sa.session.rollback()
            robots_api.abort(400, str(e))


@robots_api.route("/robots/<int:id>")
@robots_api.param("id", "The robot identifier")
@robots_api.response(404, "Robot not found")
class RobotsDetailResource(Resource):
    @robots_api.doc("get_robot")
    @robots_api.marshal_with(robots_model)
    def get(self, id):
        robot = Robots.query.get_or_404(id)
        return robot_schema.dump(robot)

    @robots_api.doc("update_robot")
    @robots_api.expect(robots_model)
    @robots_api.marshal_with(robots_model)
    def put(self, id):
        robot = Robots.query.get_or_404(id)
        robot_data = request.json
        try:
            if "robot_type_id" in robot_data:
                RobotType.query.get_or_404(robot_data["robot_type_id"])
                robot.robot_type_id = robot_data["robot_type_id"]

            if "name" in robot_data:
                robot.name = robot_data["name"]

            sa.session.commit()
            return robot_schema.dump(robot)
        except Exception as e:
            sa.session.rollback()
            robots_api.abort(400, str(e))

    @robots_api.doc("delete_robot")
    @robots_api.response(204, "Robot deleted")
    def delete(self, id):
        robot = Robots.query.get_or_404(id)
        try:
            sa.session.delete(robot)
            sa.session.commit()
            return "", 204
        except IntegrityError:
            sa.session.rollback()
            robots_api.abort(
                400, "Cannot delete robot that has associated task executions"
            )
        except Exception as e:
            sa.session.rollback()
            robots_api.abort(400, str(e))


@robots_api.route("/robots/types")
class RobotTypeResource(Resource):
    @robots_api.doc("list_robot_types")
    @robots_api.marshal_list_with(robot_type_model)
    def get(self):
        robot_types = RobotType.query.all()
        return robot_types_schema.dump(robot_types)

    @robots_api.doc("create_robot_type")
    @robots_api.expect(robot_type_model)
    @robots_api.marshal_with(robot_type_model, code=201)
    def post(self):
        robot_type_data = request.json
        try:
            robot_type = robot_type_schema.load(robot_type_data)
            sa.session.add(robot_type)
            sa.session.commit()
            return robot_type_schema.dump(robot_type), 201
        except IntegrityError:
            sa.session.rollback()
            robots_api.abort(400, "Robot type already exists")
        except Exception as e:
            sa.session.rollback()
            robots_api.abort(400, str(e))


@robots_api.route("/robots/types/<int:id>")
@robots_api.param("id", "The robot type identifier")
@robots_api.response(404, "Robot type not found")
class RobotTypeDetailResource(Resource):
    @robots_api.doc("get_robot_type")
    @robots_api.marshal_with(robot_type_model)
    def get(self, id):
        robot_type = RobotType.query.get_or_404(id)
        return robot_type_schema.dump(robot_type)

    @robots_api.doc("update_robot_type")
    @robots_api.expect(robot_type_model)
    @robots_api.marshal_with(robot_type_model)
    def put(self, id):
        robot_type = RobotType.query.get_or_404(id)
        robot_type_data = request.json
        try:
            robot_type.name = robot_type_data["name"]
            sa.session.commit()
            return robot_type_schema.dump(robot_type)
        except IntegrityError:
            sa.session.rollback()
            robots_api.abort(400, "Robot type already exists")
        except Exception as e:
            sa.session.rollback()
            robots_api.abort(400, str(e))

    @robots_api.doc("delete_robot_type")
    @robots_api.response(204, "Robot type deleted")
    def delete(self, id):
        robot_type = RobotType.query.get_or_404(id)
        try:
            sa.session.delete(robot_type)
            sa.session.commit()
            return "", 204
        except IntegrityError:
            sa.session.rollback()
            robots_api.abort(
                400, "Cannot delete robot type that is associated with robots"
            )
        except Exception as e:
            sa.session.rollback()
            robots_api.abort(400, str(e))
