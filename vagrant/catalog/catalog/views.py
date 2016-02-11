from flask import render_template, abort, request, session
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound

from . import app

from .forms import TagForm, ItemForm

# Imports for dealing with database / models
from .database import db_session
from .models import Item as dbItem, Tag as dbTag

# View for basic index page

@app.route('/')
@app.route('/catalog/')
def index():
    tags = db_session.query(dbTag).all()
    items = db_session.query(dbItem).all()
    return render_template('catalog.html', tags=tags, items=items)

# Views for viewing data in web page form

@app.route('/catalog/tags/view/<tag_name>/')
def viewTag(tag_name):
    try:
        tag = db_session.query(dbTag).filter_by(name=tag_name).one()
    except (MultipleResultsFound, NoResultFound):
        abort(404)
    return render_template('viewtag.html', tag=tag)

@app.route('/catalog/items/view/<item_name>-<int:item_id>/')
def viewItem(item_name, item_id):
    try:
        item = db_session.query(dbItem).filter_by(name=item_name, id=item_id).one()
    except (MultipleResultsFound, NoResultFound):
        abort(404)
    return render_template('viewitem.html', item=item, item_id=item_id)


# Views for creating new data entities

@app.route('/catalog/tags/new/', methods=['GET', 'POST'])
def newTag():
    form = TagForm(request.form, meta={'csrf_context': session})
    if request.method == 'POST' and form.validate():
        return "No code for handling posted forms yet. Here is the request data:<br><br><pre>%s</pre>" % request.values
    return render_template('tagform.html', form=form, action="newTag")

@app.route('/catalog/items/new/', methods=['GET', 'POST'])
def newItem():
    form = ItemForm(request.form, meta={'csrf_context': session})
    tags = db_session.query(dbTag).all()
    form.tags.choices = [(unicode(g.id), g.name) for g in tags]
    if request.method == 'POST' and form.validate():
        return "No code for handling posted forms yet. Here is the request data:<br><br><pre>%s</pre>" % request.values
    return render_template('itemform.html', form=form, action='newItem')

# Views for editing existing entities

@app.route('/catalog/tags/edit/<tag_name>/', methods=['GET', 'POST'])
def editTag(tag_name):
    # Get tag for editing
    try:
        tag = db_session.query(dbTag).filter_by(name=tag_name).one()
    except (MultipleResultsFound, NoResultFound):
        abort(404)

    form = TagForm(request.form, meta={'csrf_context': session})
    
    if request.method == 'POST' and form.validate():
        return "No code for handling posted forms yet. Here is the request data:<br><br><pre>%s</pre>" % request.values
    elif request.method == 'GET':
        # Prefill details of edited tag
        form.tag_name.data = tag.name
    return render_template('tagform.html', form=form, action="editTag", tag_name=tag_name)    # TODO: Change to input tag rather than tag name?

@app.route('/catalog/items/edit/<item_name>-<int:item_id>/', methods=['GET', 'POST'])
def editItem(item_name, item_id):
    try:
        item = db_session.query(dbItem).filter_by(name=item_name, id=item_id).one()
    except (MultipleResultsFound, NoResultFound):
        abort(404)

    form = ItemForm(request.form, meta={'csrf_context': session})
    tags = db_session.query(dbTag).all()
    form.tags.choices = [(unicode(g.id), g.name) for g in tags]
    
    # Prefill details of edited item
    form.name.data = item.name
    form.description.data = item.description
    form.tags.data = [unicode(g.id) for g in tags if g in item.tags]

    if request.method == 'POST' and form.validate():
        return "No code for handling posted forms yet. Here is the request data:<br><br><pre>%s</pre>" % request.values
    return render_template('itemform.html', form=form, action='editItem', item_name=item_name, item_id=item_id)

# Views for deleting existing entities

@app.route('/catalog/tags/delete/<tag_name>/')
def deleteTag(tag_name):
    return "This page lets you delete the existing tag: %s." % tag_name

@app.route('/catalog/items/delete/<item_name>-<int:item_id>/')
def deleteItem(item_name, item_id):
    return 'This page lets you delete the existing item called "%s" with the id %s.' % (item_name, item_id)

