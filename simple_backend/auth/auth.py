import hashlib
import hmac
import jwt
import datetime
from flask import Blueprint, request, jsonify, current_app
from database.db import query_db, insert_db

auth_bp = Blueprint("auth", __name__)

SECRET = "jwt-secret-key"


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def check_password(password: str, hashed: str) -> bool:
    return hmac.compare_digest(hash_password(password), hashed)


def generate_token(user_id: int, username: str) -> str:
    payload = {
        "user_id":  user_id,
        "username": username,
        "exp":      datetime.datetime.utcnow() + datetime.timedelta(hours=24),
    }
    return jwt.encode(payload, SECRET, algorithm="HS256")


def verify_token(token: str) -> dict:
    try:
        return jwt.decode(token, SECRET, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def authenticate(username: str, password: str):
    user = query_db(
        current_app,
        "SELECT * FROM users WHERE username = ?",
        (username,), one=True,
    )
    if not user:
        return None
    if not check_password(password, user[3]):
        return None
    return user


@auth_bp.route("/register", methods=["POST"])
def register():
    data     = request.get_json() or {}
    username = data.get("username", "").strip()
    email    = data.get("email", "").strip()
    password = data.get("password", "")

    if not username or not email or not password:
        return jsonify({"error": "username, email and password are required"}), 400

    existing = query_db(
        current_app,
        "SELECT id FROM users WHERE username = ? OR email = ?",
        (username, email), one=True,
    )
    if existing:
        return jsonify({"error": "Username or email already exists"}), 409

    user_id = insert_db(
        current_app,
        "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
        (username, email, hash_password(password)),
    )
    token = generate_token(user_id, username)
    return jsonify({"message": "Registered successfully", "token": token}), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data     = request.get_json() or {}
    username = data.get("username", "")
    password = data.get("password", "")

    user = authenticate(username, password)
    if not user:
        return jsonify({"error": "Invalid credentials"}), 401

    token = generate_token(user[0], user[1])
    return jsonify({"message": "Login successful", "token": token}), 200


@auth_bp.route("/logout", methods=["POST"])
def logout():
    # Stateless JWT — client discards token
    return jsonify({"message": "Logged out"}), 200


@auth_bp.route("/verify", methods=["GET"])
def verify():
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    payload = verify_token(token)
    if not payload:
        return jsonify({"error": "Invalid or expired token"}), 401
    return jsonify({"valid": True, "user_id": payload["user_id"]}), 200
