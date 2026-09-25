# Task Manager REST API

A production-ready RESTful Task Manager API built using Flask, Flask-RESTful, SQLite, JWT authentication, and Docker.

## Features

- User registration
- Secure password hashing
- JWT token authentication
- Create tasks
- View all tasks
- View a single task
- Update tasks
- Delete tasks
- User-based task ownership
- Input validation
- JSON responses
- Proper HTTP status codes
- Docker support
- Pinned dependencies
- Postman API testing

## Technologies Used

- Python 3.14
- Flask
- Flask-RESTful
- Flask-JWT-Extended
- SQLite
- Docker
- Postman
- Git
- GitHub

## Project Structure

task_manager_api/

├── app.py

├── database.py

├── Dockerfile

├── requirements.txt

├── .gitignore

├── README.md

└── Task_Manager_API.postman_collection.json

## Installation

### 1. Clone the repository

git clone https://github.com/manojkarthikreddyporeddy7-alt/task_manager_api.git

### 2. Open the project

cd task_manager_api

### 3. Create a virtual environment

python -m venv venv

### 4. Activate the virtual environment

Windows PowerShell:

.\venv\Scripts\Activate.ps1

### 5. Install dependencies

pip install -r requirements.txt

### 6. Run the application

python app.py

The API will run at:

http://127.0.0.1:5000

## API Endpoints

| Method | Endpoint | Authentication | Description |
|---|---|---|---|
| GET | / | No | Check API status |
| GET | /hello | No | Hello message |
| POST | /register | No | Register a user |
| POST | /login | No | Login and receive JWT |
| GET | /tasks | Yes | Get user's tasks |
| POST | /tasks | Yes | Create a task |
| GET | /tasks/<id> | Yes | Get a single task |
| PUT | /tasks/<id> | Yes | Update a task |
| DELETE | /tasks/<id> | Yes | Delete a task |

## Authentication

First register a user.

POST /register

Example request:

{
    "username": "manoj",
    "password": "test123"
}

Then login.

POST /login

Example request:

{
    "username": "manoj",
    "password": "test123"
}

The login response contains an access token.

Use the token for protected endpoints:

Authorization: Bearer <access_token>

## Create Task

POST /tasks

Requires a valid JWT token.

Example request:

{
    "title": "Learn REST API",
    "description": "Complete Task Manager project"
}

## Get All Tasks

GET /tasks

Requires a valid JWT token.

The API returns tasks belonging to the authenticated user.

## Get Single Task

GET /tasks/2

Requires a valid JWT token.

## Update Task

PUT /tasks/2

Requires a valid JWT token.

Example request:

{
    "title": "Learn REST API",
    "description": "Complete Task Manager project",
    "completed": true
}

The completed field accepts only true or false.

## Delete Task

DELETE /tasks/2

Requires a valid JWT token.

## Validation

The API validates:

- Missing request body
- Missing username
- Missing password
- Duplicate username
- Missing task title
- Invalid completed value
- Invalid username or password
- Non-existing tasks
- Unauthorized task access

## User Ownership

Users can only access their own tasks.

For example:

User 1 → Task 2 → Allowed

User 2 → Task 2 → Not allowed

User 2 → Task 3 → Allowed

The API checks the authenticated user's ID before allowing access to a task.

## Database

The application uses SQLite to store users and tasks.

The database is automatically created when the application starts.

The local database file is excluded from Git using .gitignore.

## Docker

The project includes a Dockerfile for running the API inside a Docker container.

### Build Docker Image

docker build -t task-manager-api .

### Run Docker Container

docker run --name task-manager-container -p 5000:5000 task-manager-api

The API will run at:

http://127.0.0.1:5000

### Stop Docker Container

docker stop task-manager-container

### Remove Docker Container

docker rm task-manager-container

### Docker Verification

The Dockerized API was tested successfully.

The following endpoint was verified:

GET http://127.0.0.1:5000/

Expected response:

{
    "message": "Task Manager API is running"
}

## Requirements

The project dependencies are stored in:

requirements.txt

Install all dependencies using:

pip install -r requirements.txt

The dependencies are pinned to specific versions for consistent installation.

## Testing

The API was tested using Postman and Docker.

The Postman collection contains:

- Home
- Hello
- Register
- Login
- Get All Tasks
- Create Task
- Get Single Task
- Update Task
- Delete Task

## Security

- Passwords are stored using password hashing.
- Protected task endpoints require JWT authentication.
- Users can only access their own tasks.
- Invalid input is rejected with appropriate HTTP status codes.
- Authentication failures return appropriate HTTP status codes.
- JWT secrets should be stored using environment variables in production.

## HTTP Status Codes

| Status Code | Meaning |
|---|---|
| 200 | Request successful |
| 201 | Resource created |
| 400 | Bad request |
| 401 | Authentication required or invalid credentials |
| 404 | Resource not found |
| 409 | Username already exists |

## Clean Checkout

The project can be run from a clean GitHub checkout.

Steps:

1. Clone the repository.
2. Create a virtual environment.
3. Install dependencies using requirements.txt.
4. Run the Flask application.

The project can also be run using Docker:

docker build -t task-manager-api .

docker run --name task-manager-container -p 5000:5000 task-manager-api

## Author

POREDDY MANOJ KARTHIK REDDY

Task Manager REST API - Week 4 Production-Ready Build