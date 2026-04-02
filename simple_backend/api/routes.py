from flask import Blueprint, request, jsonify, current_app
from database.db import query_db, insert_db
from auth.auth import verify_token

api_bp = Blueprint("api", __name__)


def get_token_payload(request):
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    return verify_token(token)


def create_task(user_id: int, title: str, description: str = ""):
    return insert_db(
        current_app,
        "INSERT INTO tasks (user_id, title, description) VALUES (?, ?, ?)",
        (user_id, title, description),
    )


def get_tasks(user_id: int):
    return query_db(
        current_app,
        "SELECT id, title, description, status, created_at FROM tasks WHERE user_id = ?",
        (user_id,),
    )


def get_task(task_id: int, user_id: int):
    return query_db(
        current_app,
        "SELECT id, title, description, status, created_at FROM tasks WHERE id = ? AND user_id = ?",
        (task_id, user_id), one=True,
    )


def update_task(task_id: int, user_id: int, status: str):
    insert_db(
        current_app,
        "UPDATE tasks SET status = ? WHERE id = ? AND user_id = ?",
        (status, task_id, user_id),
    )


def delete_task(task_id: int, user_id: int):
    insert_db(
        current_app,
        "DELETE FROM tasks WHERE id = ? AND user_id = ?",
        (task_id, user_id),
    )


@api_bp.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "ok", "service": "simple-backend"}), 200


@api_bp.route("/tasks", methods=["GET"])
def list_tasks():
    payload = get_token_payload(request)
    if not payload:
        return jsonify({"error": "Unauthorized"}), 401

    tasks = get_tasks(payload["user_id"])
    return jsonify([
        {
            "id":          t[0],
            "title":       t[1],
            "description": t[2],
            "status":      t[3],
        }
        for t in tasks
    ]), 200


@api_bp.route("/tasks", methods=["POST"])
def add_task():
    payload = get_token_payload(request)
    if not payload:
        return jsonify({"error": "Unauthorized"}), 401

    data  = request.get_json() or {}
    title = data.get("title", "").strip()
    if not title:
        return jsonify({"error": "title is required"}), 400

    task_id = create_task(payload["user_id"], title, data.get("description", ""))
    return jsonify({"message": "Task created", "task_id": task_id}), 201


@api_bp.route("/tasks/<int:task_id>", methods=["PUT"])
def modify_task(task_id):
    payload = get_token_payload(request)
    if not payload:
        return jsonify({"error": "Unauthorized"}), 401

    data   = request.get_json() or {}
    status = data.get("status", "").strip()
    if status not in ("pending", "in_progress", "done"):
        return jsonify({"error": "status must be pending / in_progress / done"}), 400

    update_task(task_id, payload["user_id"], status)
    return jsonify({"message": "Task updated"}), 200


@api_bp.route("/tasks/<int:task_id>", methods=["DELETE"])
def remove_task(task_id):
    payload = get_token_payload(request)
    if not payload:
        return jsonify({"error": "Unauthorized"}), 401

    delete_task(task_id, payload["user_id"])
    return jsonify({"message": "Task deleted"}), 200
