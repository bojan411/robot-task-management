import csv
import io


def generate_csv(robot_task_executions):
    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow(
        [
            "Execution ID",
            "Robot ID",
            "Robot name",
            "Robot type",
            "Robot task ID",
            "Robot task name",
            "Robot task type",
        ]
    )

    for execution in robot_task_executions:
        writer.writerow(
            [
                execution.id,
                execution.robot_id,
                execution.robot.name if execution.robot else "Unknown",
                execution.robot.robot_type.name
                if execution.robot and execution.robot.robot_type
                else "Unknown",
                execution.task_id,
                execution.task.name if execution.task else "Unknown",
                execution.task.task_type.name
                if execution.task and execution.task.task_type
                else "Unknown",
            ]
        )

    return output.getvalue()
