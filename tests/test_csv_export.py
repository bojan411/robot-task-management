def test_csv_export__succeeds(client, robot_task_execution):
    response = client.get("/robot_task_executions/csv")
    assert response.status_code == 200
    assert response.content_type == "text/csv"
    assert (
        b"Execution ID,Robot ID,Robot Name,Robot type,Robot task ID,Robot task name,Robot task type"
        in response.data
    )
