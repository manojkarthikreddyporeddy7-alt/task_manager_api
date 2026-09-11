from flask import Flask, request
from flask_restful import Api, Resource
from database import init_db, get_db_connection
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity


app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = "my-secret-key"

jwt = JWTManager(app)

api = Api(app)

init_db()


class HelloResource(Resource):
    def get(self):
        return {
            "message": "Hello from Task Manager API"
        }, 200


class RegisterResource(Resource):
    def post(self):
        data = request.get_json()

        if not data:
            return {
                "message": "Request body is required"
            }, 400

        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return {
                "message": "Username and password are required"
            }, 400

        hashed_password = generate_password_hash(password)

        connection = get_db_connection()

        existing_user = connection.execute(
            "SELECT * FROM users WHERE username = ?",
            (username,)
        ).fetchone()

        if existing_user:
            connection.close()

            return {
                "message": "Username already exists"
            }, 409

        connection.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, hashed_password)
        )

        connection.commit()
        connection.close()

        return {
            "message": "User registered successfully",
            "username": username
        }, 201


class LoginResource(Resource):
    def post(self):
        data = request.get_json()

        if not data:
            return {
                "message": "Request body is required"
            }, 400

        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return {
                "message": "Username and password are required"
            }, 400

        connection = get_db_connection()

        user = connection.execute(
            "SELECT * FROM users WHERE username = ?",
            (username,)
        ).fetchone()

        connection.close()

        if user is None:
            return {
                "message": "Invalid username or password"
            }, 401

        if not check_password_hash(user["password"], password):
            return {
                "message": "Invalid username or password"
            }, 401

        access_token = create_access_token(
            identity=str(user["id"])
        )

        return {
            "message": "Login successful",
            "access_token": access_token
        }, 200


class TaskResource(Resource):

    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()

        connection = get_db_connection()

        tasks = connection.execute(
            "SELECT * FROM tasks WHERE user_id = ?",
            (user_id,)
        ).fetchall()

        connection.close()

        task_list = []

        for task in tasks:
            task_list.append({
                "id": task["id"],
                "title": task["title"],
                "description": task["description"],
                "completed": bool(task["completed"])
            })

        return {
            "tasks": task_list
        }, 200

    @jwt_required()
    def post(self):
        data = request.get_json()

        if not data:
            return {
                "message": "Request body is required"
            }, 400

        title = data.get("title")
        description = data.get("description")

        if not title:
            return {
                "message": "Title is required"
            }, 400

        user_id = get_jwt_identity()

        connection = get_db_connection()

        cursor = connection.execute(
            """
            INSERT INTO tasks (user_id, title, description)
            VALUES (?, ?, ?)
            """,
            (user_id, title, description)
        )

        connection.commit()

        task_id = cursor.lastrowid

        connection.close()

        return {
            "message": "Task created successfully",
            "task_id": task_id,
            "title": title,
            "description": description
        }, 201


class SingleTaskResource(Resource):

    @jwt_required()
    def get(self, task_id):
        user_id = get_jwt_identity()

        connection = get_db_connection()

        task = connection.execute(
            "SELECT * FROM tasks WHERE id = ? AND user_id = ?",
            (task_id, user_id)
        ).fetchone()

        connection.close()

        if task is None:
            return {
                "message": "Task not found"
            }, 404

        return {
            "id": task["id"],
            "title": task["title"],
            "description": task["description"],
            "completed": bool(task["completed"])
        }, 200

    @jwt_required()
    def put(self, task_id):
        data = request.get_json()

        if not data:
            return {
                "message": "Request body is required"
            }, 400

        title = data.get("title")
        description = data.get("description")
        completed = data.get("completed", False)

        if not title:
            return {
                "message": "Title is required"
            }, 400

        if not isinstance(completed, bool):
            return {
                "message": "Completed must be true or false"
            }, 400

        user_id = get_jwt_identity()

        connection = get_db_connection()

        task = connection.execute(
            "SELECT * FROM tasks WHERE id = ? AND user_id = ?",
            (task_id, user_id)
        ).fetchone()

        if task is None:
            connection.close()

            return {
                "message": "Task not found"
            }, 404

        connection.execute(
            """
            UPDATE tasks
            SET title = ?, description = ?, completed = ?
            WHERE id = ? AND user_id = ?
            """,
            (
                title,
                description,
                int(completed),
                task_id,
                user_id
            )
        )

        connection.commit()
        connection.close()

        return {
            "message": "Task updated successfully",
            "id": task_id,
            "title": title,
            "description": description,
            "completed": completed
        }, 200

    @jwt_required()
    def delete(self, task_id):
        user_id = get_jwt_identity()

        connection = get_db_connection()

        task = connection.execute(
            "SELECT * FROM tasks WHERE id = ? AND user_id = ?",
            (task_id, user_id)
        ).fetchone()

        if task is None:
            connection.close()

            return {
                "message": "Task not found"
            }, 404

        connection.execute(
            "DELETE FROM tasks WHERE id = ? AND user_id = ?",
            (task_id, user_id)
        )

        connection.commit()
        connection.close()

        return {
            "message": "Task deleted successfully",
            "id": task_id
        }, 200


api.add_resource(HelloResource, "/hello")
api.add_resource(RegisterResource, "/register")
api.add_resource(LoginResource, "/login")
api.add_resource(TaskResource, "/tasks")
api.add_resource(SingleTaskResource, "/tasks/<int:task_id>")


@app.route("/")
def home():
    return {
        "message": "Task Manager API is running"
    }, 200


if __name__ == "__main__":
    app.run(debug=True)