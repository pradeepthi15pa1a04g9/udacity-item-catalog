from functools import wraps
from flask import session, url_for, redirect, url_for, request, abort
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound
from urlparse import urlparse, urljoin

from models import User, Tag, Item


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('showLogin', next=make_url_relative(request.url)))
        return f(*args, **kwargs)
    return decorated_function

def activated_user_required(login_session, db_session):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            logged_in_user_id = login_session['user_id']
            logged_in_user = db_session.query(User).filter_by(id=logged_in_user_id).one()

            # Check if user is activated and throw 403 if not
            if logged_in_user.activated:
                return f(*args, **kwargs)
            else:
                abort(403)

        return decorated_function
    return decorator

def make_url_relative(url_or_path):
    result = urlparse(url_or_path).path
    if not result:
        result = '/'
    return result

def owner_only(login_session, db_session, object_class):
    """Decorator to protect edit and delete views from non-owners of the relevant object.
    Applied after login_required decorator, as assumes user is logged in."""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            logged_in_user_id = login_session['user_id']
            
            # Check if admin, in which case let through
            logged_in_user = db_session.query(User).filter_by(id=logged_in_user_id).one()
            if logged_in_user.admin:
                return f(*args, **kwargs)

            # Extract from url parameters approprate arguments for database query
            params = dict()
            if 'item_id' in kwargs:
                params['id'] = kwargs['item_id']
                params['name'] = kwargs['item_name']
            else:
                params['name'] = kwargs['tag_name']

            try: # Try and find an item matching these parameters
                item_or_tag = db_session.query(object_class).filter_by(**params).one()
            except (NoResultFound, MultipleResultsFound):
                # If item not found, or too many found, throw 404
                abort(404)

            if item_or_tag.user_id != logged_in_user_id:
                abort(403)

            return f(*args, **kwargs)
        return decorated_function
    return decorator

def admin_only(login_session, db_session):
    """Decorator to protect admin pages from non-admins. Assumes user is logged in."""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            logged_in_user_id = login_session['user_id']
            
            # Check if admin, in which case let through
            logged_in_user = db_session.query(User).filter_by(id=logged_in_user_id).one()
            if logged_in_user.admin:
                return f(*args, **kwargs)
            else:
                abort(403)

        return decorated_function
    return decorator