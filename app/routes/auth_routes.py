from flask import Blueprint, request, jsonify, current_app, render_template, session, url_for, redirect
import bcrypt
import uuid
from app.db import mysql
from datetime import datetime, timedelta

auth_bp = Blueprint('auth_bp', __name__, url_prefix='/api/auth')

@auth_bp.route('/signup', methods=['POST'])
def signup():
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')

    if not name or not email or not password:
        return jsonify({'success': False, 'error': 'All fields are required'}), 400

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    existing_user = cursor.fetchone()
    if existing_user:
        return jsonify({'success': False, 'error': 'User with this email address already exists'}), 400

    # Hash the password using bcrypt
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    user_id = str(uuid.uuid4())

    cursor.execute(
        "INSERT INTO users (id, name, email, password) VALUES (%s, %s, %s, %s)",
        (user_id, name, email, hashed_password.decode('utf-8'))
    )
    mysql.connection.commit()
    cursor.close()

    return jsonify({'success': True, 'message': 'User registered successfully'}), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')

    if not email or not password:
        return render_template('login.html', error='Email and password are required.')

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cursor.fetchone()
    cursor.close()

    if not user or not bcrypt.checkpw(password.encode('utf-8'), user[3].encode('utf-8')):
        return render_template('login.html', error='Invalid email or password.')

    user_data = {
        'id': user[0],
        'name': user[1],
        'email': user[2]
    }

    session['user_id'] = user_data['id']
    session['user_name'] = user_data['name']
    session['user_email'] = user_data['email']

    return redirect(url_for('templates_bp.home_page'))

@auth_bp.route('/me', methods=['GET'])
def get_me():
    user_id = session.get('user_id')
    user_name = session.get('user_name')
    user_email = session.get('user_email')

    if not user_id:
        return jsonify({'success': False, 'error': 'User is not logged in'}), 401

    user = {
        'id': user_id,
        'name': user_name,
        'email': user_email
    }

    return jsonify({'success': True, 'user': user}), 200

@auth_bp.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    session.pop('user_name', None)
    session.pop('user_email', None)

    return render_template('login.html')
