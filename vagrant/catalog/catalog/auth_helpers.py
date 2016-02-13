from functools import wraps
from flask import session, url_for, redirect, url_for, request
from urlparse import urlparse, urljoin

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('showLogin', next=make_url_relative(request.url)))
        return f(*args, **kwargs)
    return decorated_function

def make_url_relative(url_or_path):
    result = urlparse(url_or_path).path
    if not result:
        result = '/'
    return result