from wtforms import Form, StringField, validators

class NewTagForm(Form):
    tag_name = StringField('Category Name', [validators.Length(min=3, max=25)])