# Task Manager REST API

A RESTful Task Manager API built using Flask, Flask-RESTful, SQLite, and JWT authentication.

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

## Technologies Used

- Python
- Flask
- Flask-RESTful
- Flask-JWT-Extended
- SQLite
- Postman

## Project Structure

task_manager_api/
├── app.py
├── database.py
├── .gitignore
└── README.md

## Installation

### 1. Clone the repository

git clone <your-github-repository-url>

### 2. Open the project

cd task_manager_api

### 3. Create a virtual environment

python -m venv venv

### 4. Activate the virtual environment

Windows PowerShell:

.\venv\Scripts\Activate.ps1

### 5. Install dependencies

pip install Flask Flask-RESTful Flask-JWT-Extended

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

Example request:

{
    "title": "Learn REST API",
    "description": "Complete Week 3 Task Manager project"
}

## Get All Tasks

GET /tasks

Requires a valid JWT token.

## Get Single Task

GET /tasks/2

Requires a valid JWT token.

## Update Task

PUT /tasks/2

Example request:

{
    "title": "Learn REST API",
    "description": "Complete Week 3 Task Manager project",
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

## Testing

The API was tested using Postman.

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

## HTTP Status Codes

| Status Code | Meaning |
|---|---|
| 200 | Request successful |
| 201 | Resource created |
| 400 | Bad request |
| 401 | Authentication required or invalid credentials |
| 404 | Resource not found |
| 409 | Username already exists |

## Author

Task Manager REST API - Week 3 Project