from flask import Blueprint, request, jsonify, flash, session, url_for, redirect
import bcrypt
import uuid
from app.db import mysql

auth_bp = Blueprint("auth_bp", __name__, url_prefix="/api/auth")


@auth_bp.route("/signup", methods=["POST"])
def signup():
    name = request.form.get("name")
    email = request.form.get("email")
    password = request.form.get("password")

    if not name or not email or not password:
        return jsonify({"success": False, "message": "All fields are required."}), 400

    # Password complexity check
    if len(password) < 8:
        return jsonify({"success": False, "message": "Password must be at least 8 characters long."}), 400

    with mysql.connection.cursor() as cursor:
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        existing_user = cursor.fetchone()
        if existing_user:
            return jsonify({"success": False, "message": "User with this email already exists."}), 409

        # Hash the password
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

        user_id = str(uuid.uuid4())
        cursor.execute(
            "INSERT INTO users (id, name, email, password) VALUES (%s, %s, %s, %s)",
            (user_id, name, email, hashed_password),
        )
        mysql.connection.commit()

    return jsonify({"success": True, "message": "User registered successfully."}), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    email = request.form.get("email")
    password = request.form.get("password")

    if not email or not password:
        return jsonify({"success": False, "message": "Email and password are required."}), 400

    with mysql.connection.cursor() as cursor:
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()

    if not user:
        return jsonify({"success": False, "message": "Invalid email or password."}), 401

    if not bcrypt.checkpw(password.encode("utf-8"), user[3].encode("utf-8")):
        return jsonify({"success": False, "message": "Invalid email or password."}), 401

    session.permanent = True  # Set session expiration policy if needed
    session["user_id"] = user[0]
    session["user_name"] = user[1]
    session["user_email"] = user[2]

    return jsonify({"success": True, "message": "Logged in successfully."}), 200


@auth_bp.route("/me", methods=["GET"])
def get_me():
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"success": False, "error": "User is not logged in"}), 401

    user = {
        "id": user_id,
        "name": session.get("user_name"),
        "email": session.get("user_email"),
    }
    return jsonify({"success": True, "user": user}), 200


@auth_bp.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"success": True, "message": "Logged out successfully."}), 200
