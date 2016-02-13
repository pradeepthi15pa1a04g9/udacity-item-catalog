from functools import wraps
from flask import session, url_for, redirect

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('showLogin'))
        return f(*args, **kwargs)
    return decorated_function