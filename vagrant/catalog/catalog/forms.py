from wtforms import Form, StringField, validators
from wtforms.csrf.session import SessionCSRF
from datetime import timedelta
from . import app

class MyBaseForm(Form):
    class Meta:
        csrf = True
        csrf_class = SessionCSRF
        csrf_secret = app.config['CSRF_SECRET_KEY']
        csrf_time_limit = timedelta(minutes=20)

class NewTagForm(MyBaseForm):
    tag_name = StringField('Category Name', [validators.Length(min=3, max=25)])