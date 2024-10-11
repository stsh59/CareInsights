from functools import wraps
from flask import redirect, url_for, session


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:  # Check if user is logged in
            return redirect(url_for("templates_bp.login_page"))
        return f(*args, **kwargs)

    return decorated_function
