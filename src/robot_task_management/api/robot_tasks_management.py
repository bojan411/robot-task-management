from flask import request
from flask_restx import Namespace, Resource, fields
from sqlalchemy.exc import IntegrityError

from robot_task_management.flask_apps import sa
from robot_task_management.models.robot_tasks import RobotTasks
from robot_task_management.models.robot_task_type import RobotTaskType
from robot_task_management.schemas.robot_tasks import RobotTasksSchema
from robot_task_management.schemas.robot_task_type import RobotTaskTypeSchema


robot_tasks_api = Namespace("robot_tasks", description="Robots task management")

# Swagger
task_type_model = robot_tasks_api.model(
    "RobotTaskType",
    {
        "id": fields.Integer(
            readonly=True, description="Robots task type unique identifier"
        ),
        "name": fields.String(
            required=True, description="Robots task type unique name"
        ),
    },
)

task_model = robot_tasks_api.model(
    "RobotTasks",
    {
        "id": fields.Integer(
            readonly=True, description="Robots task unique identifier"
        ),
        "name": fields.String(required=True, description="Robots task unique name"),
        "task_type_id": fields.Integer(
            required=True, description="Robots task type identifier"
        ),
    },
)

robot_task_schema = RobotTasksSchema()
robot_tasks_schema = RobotTasksSchema(many=True)
robot_task_type_schema = RobotTaskTypeSchema()
robot_task_types_schema = RobotTaskTypeSchema(many=True)


@robot_tasks_api.route("/robot_tasks")
class RobotTasksResource(Resource):
    @robot_tasks_api.doc("list_tasks")
    @robot_tasks_api.marshal_list_with(task_model)
    def get(self):
        tasks = RobotTasks.query.all()
        return robot_tasks_schema.dump(tasks)

    @robot_tasks_api.doc("create_task")
    @robot_tasks_api.expect(task_model)
    @robot_tasks_api.marshal_with(task_model, code=201)
    def post(self):
        task_data = request.json
        try:
            RobotTasks.query.get_or_404(task_data["task_type_id"])

            task = robot_task_schema.load(task_data)
            sa.session.add(task)
            sa.session.commit()
            return robot_task_schema.dump(task), 201
        except IntegrityError:
            sa.session.rollback()
            robot_tasks_api.abort(400, "Robot task already exists")
        except Exception as e:
            sa.session.rollback()
            robot_tasks_api.abort(400, str(e))


@robot_tasks_api.route("/robot_tasks/<int:id>")
@robot_tasks_api.param("id", "Robot task unique identifier")
@robot_tasks_api.response(404, "Robot task not found")
class RobotTasksDetailResource(Resource):
    @robot_tasks_api.doc("get_task")
    @robot_tasks_api.marshal_with(task_model)
    def get(self, id):
        task = RobotTasks.query.get_or_404(id)
        return robot_task_schema.dump(task)

    @robot_tasks_api.doc("update_task")
    @robot_tasks_api.expect(task_model)
    @robot_tasks_api.marshal_with(task_model)
    def put(self, id):
        task = RobotTasks.query.get_or_404(id)
        task_data = request.json
        try:
            if "task_type_id" in task_data:
                RobotTasks.query.get_or_404(task_data["task_type_id"])
                task.task_type_id = task_data["task_type_id"]

            if "name" in task_data:
                task.name = task_data["name"]

            sa.session.commit()
            return robot_task_schema.dump(task)
        except Exception as e:
            sa.session.rollback()
            robot_tasks_api.abort(400, str(e))

    @robot_tasks_api.doc("delete_task")
    @robot_tasks_api.response(204, "Robot task deleted")
    def delete(self, id):
        task = RobotTasks.query.get_or_404(id)
        try:
            sa.session.delete(task)
            sa.session.commit()
            return "", 204
        except IntegrityError:
            sa.session.rollback()
            robot_tasks_api.abort(400, "Cannot delete task that has linked executions")
        except Exception as e:
            sa.session.rollback()
            robot_tasks_api.abort(400, str(e))


@robot_tasks_api.route("/robot_tasks/types")
class RobotTaskTypeResource(Resource):
    @robot_tasks_api.doc("list_task_types")
    @robot_tasks_api.marshal_list_with(task_type_model)
    def get(self):
        task_types = RobotTaskType.query.all()
        return robot_task_types_schema.dump(task_types)

    @robot_tasks_api.doc("create_task_type")
    @robot_tasks_api.expect(task_type_model)
    @robot_tasks_api.marshal_with(task_type_model, code=201)
    def post(self):
        task_type_data = request.json
        try:
            task_type = robot_task_type_schema.load(task_type_data)
            sa.session.add(task_type)
            sa.session.commit()
            return robot_task_type_schema.dump(task_type), 201
        except IntegrityError:
            sa.session.rollback()
            robot_tasks_api.abort(400, "Robot task type already exists")
        except Exception as e:
            sa.session.rollback()
            robot_tasks_api.abort(400, str(e))


@robot_tasks_api.route("/robot_tasks/types/<int:id>")
@robot_tasks_api.param("id", "Robot task type unique identifier")
@robot_tasks_api.response(404, "Robot task type not found")
class RobotTaskTypeDetailResource(Resource):
    @robot_tasks_api.doc("get_task_type")
    @robot_tasks_api.marshal_with(task_type_model)
    def get(self, id):
        task_type = RobotTaskType.query.get_or_404(id)
        return robot_task_type_schema.dump(task_type)

    @robot_tasks_api.doc("update_task_type")
    @robot_tasks_api.expect(task_type_model)
    @robot_tasks_api.marshal_with(task_type_model)
    def put(self, id):
        task_type = RobotTaskType.query.get_or_404(id)
        task_type_data = request.json
        try:
            task_type.name = task_type_data["name"]
            sa.session.commit()
            return robot_task_type_schema.dump(task_type)
        except IntegrityError:
            sa.session.rollback()
            robot_tasks_api.abort(400, "Robot task type already exists")
        except Exception as e:
            sa.session.rollback()
            robot_tasks_api.abort(400, str(e))

    @robot_tasks_api.doc("delete_task_type")
    @robot_tasks_api.response(204, "Robot task type deleted")
    def delete(self, id):
        task_type = RobotTaskType.query.get_or_404(id)
        try:
            sa.session.delete(task_type)
            sa.session.commit()
            return "", 204
        except IntegrityError:
            sa.session.rollback()
            robot_tasks_api.abort(
                400, "Cannot delete task type that is associated with tasks"
            )
        except Exception as e:
            sa.session.rollback()
            robot_tasks_api.abort(400, str(e))
