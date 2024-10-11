from flask import (
    Blueprint,
    request,
    jsonify,
    flash,
    session,
    url_for,
    redirect,
)
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
        flash("All fields are required.", "error")
        return redirect(url_for("templates_bp.signup_page"))

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    existing_user = cursor.fetchone()
    if existing_user:
        flash("User with this email address already exists", "error")
        return redirect(url_for("templates_bp.signup_page"))

    # Hash the password using bcrypt
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    user_id = str(uuid.uuid4())

    cursor.execute(
        "INSERT INTO users (id, name, email, password) VALUES (%s, %s, %s, %s)",
        (user_id, name, email, hashed_password.decode("utf-8")),
    )
    mysql.connection.commit()
    cursor.close()

    return redirect(url_for("templates_bp.login_page"))


@auth_bp.route("/login", methods=["POST"])
def login():
    email = request.form.get("email")
    password = request.form.get("password")

    if not email or not password:
        flash("Email and password is required.", "error")
        return redirect(url_for("templates_bp.login_page"))

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cursor.fetchone()
    cursor.close()

    if not user:
        flash("Invalid email, User with this email doesn't exist!", "error")
        return redirect(url_for("templates_bp.login_page"))

    if not bcrypt.checkpw(password.encode("utf-8"), user[3].encode("utf-8")):
        flash("The password you entered is incorrect!", "error")
        return redirect(url_for("templates_bp.login_page"))

    user_data = {"id": user[0], "name": user[1], "email": user[2]}

    session["user_id"] = user_data["id"]
    session["user_name"] = user_data["name"]
    session["user_email"] = user_data["email"]

    return redirect(url_for("templates_bp.home_page"))


@auth_bp.route("/me", methods=["GET"])
def get_me():
    user_id = session.get("user_id")
    user_name = session.get("user_name")
    user_email = session.get("user_email")

    if not user_id:
        return jsonify({"success": False, "error": "User is not logged in"}), 401

    user = {"id": user_id, "name": user_name, "email": user_email}

    return jsonify({"success": True, "user": user}), 200


@auth_bp.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect(url_for("templates_bp.login_page"))
