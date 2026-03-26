from flask import Blueprint, request, jsonify, current_app
from database.db import query_db, insert_db
from auth.auth import verify_token, hash_password

user_bp = Blueprint("user", __name__)


def get_user_from_token(request):
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    return verify_token(token)


def get_user(user_id: int):
    return query_db(
        current_app,
        "SELECT id, username, email, created_at FROM users WHERE id = ?",
        (user_id,), one=True,
    )


def get_all_users():
    return query_db(
        current_app,
        "SELECT id, username, email, created_at FROM users",
    )


def update_user(user_id: int, email: str):
    insert_db(
        current_app,
        "UPDATE users SET email = ? WHERE id = ?",
        (email, user_id),
    )


def delete_user(user_id: int):
    insert_db(
        current_app,
        "DELETE FROM users WHERE id = ?",
        (user_id,),
    )


@user_bp.route("/profile", methods=["GET"])
def get_profile():
    payload = get_user_from_token(request)
    if not payload:
        return jsonify({"error": "Unauthorized"}), 401

    user = get_user(payload["user_id"])
    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify({
        "id":         user[0],
        "username":   user[1],
        "email":      user[2],
        "created_at": user[3],
    }), 200


@user_bp.route("/profile", methods=["PUT"])
def update_profile():
    payload = get_user_from_token(request)
    if not payload:
        return jsonify({"error": "Unauthorized"}), 401

    data  = request.get_json() or {}
    email = data.get("email", "").strip()
    if not email:
        return jsonify({"error": "email is required"}), 400

    update_user(payload["user_id"], email)
    return jsonify({"message": "Profile updated"}), 200


@user_bp.route("/all", methods=["GET"])
def list_users():
    users = get_all_users()
    return jsonify([
        {"id": u[0], "username": u[1], "email": u[2], "created_at": u[3]}
        for u in users
    ]), 200


@user_bp.route("/<int:user_id>", methods=["DELETE"])
def remove_user(user_id):
    payload = get_user_from_token(request)
    if not payload:
        return jsonify({"error": "Unauthorized"}), 401
    delete_user(user_id)
    return jsonify({"message": f"User {user_id} deleted"}), 200
