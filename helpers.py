from datetime import datetime
from flask_session import Session
from flask import redirect, render_template, request, session, send_from_directory, get_flashed_messages
from functools import wraps


def login_required(f):  
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function