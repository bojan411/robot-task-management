from flask import request, Response
from flask_restx import Namespace, Resource, fields, reqparse
from sqlalchemy.exc import IntegrityError

from robot_task_management.flask_apps import sa
from robot_task_management.models.robots import Robots
from robot_task_management.models.robot_tasks import RobotTasks
from robot_task_management.models.robot_task_executions import RobotTaskExecutions
from robot_task_management.schemas.robot_task_executions import (
    RobotTaskExecutionsSchema,
)
from robot_task_management.util import generate_csv

robot_task_executions_api = Namespace(
    "robot_task_executions", description="Task execution"
)

# Swagger
execution_model = robot_task_executions_api.model(
    "RobotTaskExecutions",
    {
        "id": fields.Integer(
            readonly=True, description="Robots task execution unique identifier"
        ),
        "robot_id": fields.Integer(
            required=True, description="Robot unique identifier"
        ),
        "task_id": fields.Integer(required=True, description="Robots task identifier"),
    },
)

robot_task_execution_schema = RobotTaskExecutionsSchema()
robots_task_executions_schema = RobotTaskExecutionsSchema(many=True)

# Filters
robot_task_executions_filter = reqparse.RequestParser()
robot_task_executions_filter.add_argument(
    "robot_id", type=int, help="Filter by robot ID"
)
robot_task_executions_filter.add_argument(
    "robot_type_id", type=int, help="Filter by robot type ID"
)
robot_task_executions_filter.add_argument(
    "robot_task_id", type=int, help="Filter by robots task ID"
)
robot_task_executions_filter.add_argument(
    "robot_task_type_id", type=int, help="Filter by robots task type ID"
)


@robot_task_executions_api.route("/robot_task_executions")
class RobotTaskExecutionsResource(Resource):
    @robot_task_executions_api.doc("list_executions")
    @robot_task_executions_api.expect(robot_task_executions_filter)
    def get(self):
        query = apply_filters(robot_task_executions_filter)

        robot_task_executions = query.all()

        return robots_task_executions_schema.dump(robot_task_executions)

    @robot_task_executions_api.doc("create_execution")
    @robot_task_executions_api.expect(execution_model)
    @robot_task_executions_api.marshal_with(execution_model, code=201)
    def post(self):
        execution_data = request.json
        try:
            Robots.query.get_or_404(execution_data["robot_id"])
            RobotTasks.query.get_or_404(execution_data["task_id"])

            execution = robot_task_execution_schema.load(execution_data)
            sa.session.add(execution)
            sa.session.commit()
            return robot_task_execution_schema.dump(execution), 201
        except IntegrityError:
            sa.session.rollback()
            robot_task_executions_api.abort(400, "Database integrity error")
        except Exception as e:
            sa.session.rollback()
            robot_task_executions_api.abort(400, str(e))


@robot_task_executions_api.route("/robot_task_executions/csv")
class RobotTaskExecutionsExportResource(Resource):
    @robot_task_executions_api.doc("export_executions")
    @robot_task_executions_api.expect(robot_task_executions_filter)
    def get(self):
        query = apply_filters(robot_task_executions_filter)

        robot_task_executions = query.all()

        csv_data = generate_csv(robot_task_executions)
        return Response(
            csv_data,
            mimetype="text/csv",
            headers={
                "Content-Disposition": "attachment; filename=robot_task_executions.csv"
            },
        )


def apply_filters(robot_task_executions_filter):
    args = robot_task_executions_filter.parse_args()

    query = RobotTaskExecutions.query

    if args.robot_id:
        query = query.filter(RobotTaskExecutions.robot_id == args.robot_id)

    if args.robot_type_id:
        query = query.join(Robots).filter(Robots.robot_type_id == args.robot_type_id)

    if args.robot_task_id:
        query = query.filter(RobotTaskExecutions.task_id == args.task_id)

    if args.robot_task_type_id:
        query = query.join(RobotTasks).filter(
            RobotTasks.task_type_id == args.task_type_id
        )

    return query
