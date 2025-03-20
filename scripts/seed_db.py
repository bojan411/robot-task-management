#!/usr/bin/env python
import sys
import os
import random
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
)

from robot_task_management import create_app
from robot_task_management.flask_apps import sa
from robot_task_management.models.robots import Robots
from robot_task_management.models.robot_type import RobotType
from robot_task_management.models.robot_tasks import RobotTasks
from robot_task_management.models.robot_task_type import RobotTaskType
from robot_task_management.models.robot_task_executions import RobotTaskExecutions


def seed_db():
    print("Seeding database...")

    robot_types = [
        RobotType(name="Transport Robot"),
        RobotType(name="Inspection Robot"),
        RobotType(name="Maintenance Robot"),
        RobotType(name="Security Robot"),
    ]
    sa.session.add_all(robot_types)
    sa.session.commit()
    print(f"Created {len(robot_types)} robot types")

    robots = []
    for i in range(1, 21):
        robot_type = random.choice(robot_types)
        robot = Robots(
            name=f"Robot-{i:03d}",
            robot_type_id=robot_type.id,
            status="active" if random.random() > 0.2 else "inactive",
        )
        robots.append(robot)
    sa.session.add_all(robots)
    sa.session.commit()
    print(f"Created {len(robots)} robots")

    task_types = [
        RobotTaskType(name="Transportation"),
        RobotTaskType(name="Charging"),
        RobotTaskType(name="Parking"),
        RobotTaskType(name="Maintenance"),
    ]
    sa.session.add_all(task_types)
    sa.session.commit()
    print(f"Created {len(task_types)} task types")

    tasks = []
    locations = ["Warehouse A", "Warehouse B", "Production Line", "Office Area"]

    for task_type in task_types:
        for i in range(1, 6):
            if task_type.name == "Transportation":
                name = f"Transport items from {random.choice(locations)} to {random.choice(locations)}"
            elif task_type.name == "Charging":
                name = f"Charge at {random.choice(locations)}"
            elif task_type.name == "Parking":
                name = f"Park at {random.choice(locations)}"
            elif task_type.name == "Maintenance":
                name = f"Perform maintenance at {random.choice(locations)}"

            task = RobotTasks(
                name=name,
                task_type_id=task_type.id,
                priority=random.choice(["low", "medium", "high"]),
            )
            tasks.append(task)
    sa.session.add_all(tasks)
    sa.session.commit()
    print(f"Created {len(tasks)} tasks")

    executions = []
    now = datetime.now(tz=ZoneInfo("UTC"))

    for i in range(100):
        robot = random.choice(robots)
        task = random.choice(tasks)

        days_ago = random.randint(0, 30)
        hours_ago = random.randint(0, 23)
        created_at = now - timedelta(days=days_ago, hours=hours_ago)

        execution = RobotTaskExecutions(
            robot_id=robot.id, task_id=task.id, created_at=created_at
        )
        executions.append(execution)

    sa.session.add_all(executions)
    sa.session.commit()
    print(f"Created {len(executions)} task executions")

    print("Database finished.")


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        if len(sys.argv) > 1 and sys.argv[1] == "--reset":
            print("Resetting database...")
            sa.drop_all()
            sa.create_all()

        seed_db()
