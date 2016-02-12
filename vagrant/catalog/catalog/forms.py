from wtforms import (Form, StringField, SelectMultipleField, TextAreaField,
                     validators)
from wtforms.csrf.session import SessionCSRF
from datetime import timedelta
from . import app

class MyBaseForm(Form):
    """Base form, provides configuration necessary for WTForms CSRF prevention
    features"""
    class Meta:
        csrf = True
        csrf_class = SessionCSRF
        csrf_secret = app.config['CSRF_SECRET_KEY']
        csrf_time_limit = timedelta(minutes=20)

class TagForm(MyBaseForm):
    tag_name = StringField('Category Name',
                           [validators.Length(min=3, max=25)])

class ItemForm(MyBaseForm):
	name = StringField('Item Name',
                        [validators.Length(min=3, max=25)])
	description = TextAreaField('Item Description',
                                [validators.Length(max=200)])
	tags = SelectMultipleField('Categories')

class DeleteForm(MyBaseForm):
    pass
