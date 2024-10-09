from flask import Blueprint, redirect, render_template, session, url_for
from app.utils import login_required

templates_bp = Blueprint('templates_bp', __name__)

@templates_bp.route('/', methods=['GET'])
@login_required
def home_page():
    return render_template('index.html', user_name = session["user_name"])

@templates_bp.route('/signup', methods=['GET'])
def signup_page():
    if session["user_id"]:
            return redirect(url_for('templates_bp.home_page'))
    return render_template('signup.html')

@templates_bp.route('/login', methods=['GET'])
def login_page():
    if session["user_id"]:
        return redirect(url_for('templates_bp.home_page'))
    return render_template('login.html')
