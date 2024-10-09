from flask import Flask, render_template
from flask_session import Session
from flask_mysqldb import MySQL
from flask_cors import CORS
from app.routes.auth_routes import auth_bp
from app.routes.templates_routes import templates_bp

mysql = MySQL()

def create_app():
    app = Flask(__name__, static_folder='static', template_folder='templates')

    # Configuration for MySQL
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = 'password'
    app.config['MYSQL_DB'] = 'todo_db'

    # Secret key for JWT
    app.config['SECRET_KEY'] = 'care_insights_secret_12121212'

    # Session
    app.config['SESSION_TYPE'] = 'filesystem'
    Session(app)

    mysql.init_app(app)
    CORS(app)

    # Register Blueprints
    app.register_blueprint(templates_bp)
    app.register_blueprint(auth_bp)

    return app
