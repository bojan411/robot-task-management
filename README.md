# Robot Task Management System

A Flask REST API for managing robots and their tasks.

## Features

- Robot management (CRUD)
- Robot task management (CRUD)
- Robot task execution tracking and history
- CSV export of task execution history
- Filtering capabilities for robot task executions
- Filtering capabilities for robot task executions CSV export

## Database Schema

- **Robot Types**: Defines different types of robots
- **Robots**: Individual robots with a specific type
- **Robot Task Types**: Defines different types of tasks
- **Robot Tasks**: Individual robot tasks with a specific type
- **Robot Task Executions**: Records of robot tasks executed by robots

## Getting Started

### Prerequisites

- Docker
- Docker Compose

### Environment Configuration

1. Copy the example environment file:
```
cp .env.sample .env
```

2. Edit the `.env` file to customize your configuration

### Running the Application

1. Clone the repository
2. Navigate to the project directory
3. Run the application with Docker Compose:

```
docker-compose up -d
```

4. Access the API documentation at http://localhost:5000/docs

### Seeding the Database

To populate the database with sample data for development or testing:

```
make seed-db
```

To reset the database and seed it with fresh data:

```
make reset-db
```

### Development Setup

If you want to develop locally:

1. Install Poetry (dependency management tool):

```
curl -sSL https://install.python-poetry.org | python3 -
```

2. Install dependencies:
```
poetry install
```

3. Activate the virtual environment:
```
eval $(poetry env activate)
```

4. Run the application:
```
flask run
```

## API Endpoints

### Robots

- `GET /robots/` - List all robots
- `POST /robots/` - Create a new robot
- `GET /robots/{id}` - Get a specific robot
- `PUT /robots/{id}` - Update a robot
- `DELETE /robots/{id}` - Delete a robot

### Robot Types

- `GET /robots/types/` - List all robot types
- `POST /robots/types/` - Create a new robot type
- `GET /robots/types/{id}` - Get a specific robot type
- `PUT /robots/types/{id}` - Update a robot type
- `DELETE /robots/types/{id}` - Delete a robot type

### Robot Tasks

- `GET /robot_tasks/` - List all robot tasks
- `POST /robot_tasks/` - Create a new robot task
- `GET /robot_tasks/{id}` - Get a specific robot task
- `PUT /robot_tasks/{id}` - Update a robot task
- `DELETE /robot_tasks/{id}` - Delete a robot task

### Robot Task Types

- `GET /robot_tasks/types/` - List all robot task types
- `POST /robot_tasks/types/` - Create a new robot task type
- `GET /robot_tasks/types/{id}` - Get a specific robot task type
- `PUT /robot_tasks/types/{id}` - Update a robot task type
- `DELETE /robot_tasks/types/{id}` - Delete a robot task type

### Robot Task Executions

- `GET /robot_task_executions/` - List all robot task executions
- `POST /robot_task_executions/` - Create a new task execution

## Filtering Robot Task Executions

You can filter robot task executions by:
- Robot ID
- Robot Type ID
- Task ID
- Task Type ID

Example: `GET /robot_task_executions/?robot_type_id=1&task_type_id=2`

## CSV Export

To export task executions as CSV visit `/robot_task_executions/csv` endpoint

You can filter exported data the same way as robot task executions by:
- Robot ID
- Robot Type ID
- Task ID
- Task Type ID

Example: `GET /robot_task_executions/csv?robot_type_id=1&task_type_id=2`