from flask import render_template, abort, request, session, redirect, url_for
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound
from sqlalchemy.exc import IntegrityError

from . import app

from .forms import TagForm, ItemForm, DeleteForm

# Imports for dealing with database / models
from .database import db_session
from .models import Item, Tag

# Basic web views

@app.route('/')
@app.route('/catalog/')
def index():
    """View to provide a main index page for our site"""
    tags = db_session.query(Tag).all()
    items = db_session.query(Item).all()
    return render_template('catalog.html', tags=tags, items=items)

# Views for viewing data in web page form

@app.route('/catalog/tags/view/<tag_name>/')
def viewTag(tag_name):
    """View to allow users to view tag information and associated
    items."""
    try:
        tag = db_session.query(Tag).filter_by(name=tag_name).one()
    except (MultipleResultsFound, NoResultFound):
        # If there's more or less than one tag with that name,
        # throw a 404
        abort(404) 
    return render_template('viewtag.html', tag=tag)

@app.route('/catalog/items/view/<item_name>-<int:item_id>/')
def viewItem(item_name, item_id):
    """View to allow users to view information about individual
    items."""
    try:
        item = db_session.query(Item).filter_by(name=item_name,
                                                id=item_id).one()
    except (MultipleResultsFound, NoResultFound):
        # If there are more or less than one item with that name and id
        # throw a 404
        abort(404)
    return render_template('viewitem.html', item=item)


# Views for creating new data entities

@app.route('/catalog/tags/new/', methods=['GET', 'POST'])
def newTag():
    """View to provide a form for creating new tags, and to respond
    POST requests from this form."""

    form = TagForm(request.form, meta={'csrf_context': session})
    
    if request.method == 'POST' and form.validate():
        try:
            new_tag = Tag(name=form.tag_name.data)
            db_session.add(new_tag)
            db_session.commit()
            return redirect(url_for('index'))
        except IntegrityError:
            # If user tries to create a tag with an existing name,
            # roll back and add a form error
            db_session.rollback()
            form.tag_name.errors.append(
                'A tag already exists with that name.')

    return render_template('tagform.html', form=form, action="newTag")

@app.route('/catalog/items/new/', methods=['GET', 'POST'])
def newItem():
    """View to provide a form for creating new items, and to respond
    POST requests from this form."""

    form = ItemForm(request.form, meta={'csrf_context': session})
    
    # Get all tags from database
    tags = db_session.query(Tag).all()
    # Fill multiselect with these tags
    form.tags.choices = [(unicode(g.id), g.name) for g in tags]
    
    if request.method == 'POST' and form.validate():
        
        # Get list of the ids of the selected tags.
        item_tag_ids = map(int, form.tags.data)
        
        # Use this to get a list of these as Tag objects.
        item_tags = db_session.query(Tag)                           \
                              .filter(Tag.id.in_(item_tag_ids))     \
                              .all()
        
        # Create new item using this information.
        new_item = Item(name = form.name.data,
                        description=form.description.data,
                        tags=item_tags)
        db_session.add(new_item)
        db_session.commit()

        return redirect(url_for('index'))

    return render_template('itemform.html', form=form, action='newItem')


# Views for editing existing entities

@app.route('/catalog/tags/edit/<tag_name>/', methods=['GET', 'POST'])
def editTag(tag_name):
    """View to provide a form for editing existing tags, and to
    respond POST requests from this form."""
    # Get tag for editing
    try:
        tag = db_session.query(Tag).filter_by(name=tag_name).one()
    except (MultipleResultsFound, NoResultFound):
        # If there are more or less than one tags with this name,
        # throw a 404.
        abort(404)

    form = TagForm(request.form, meta={'csrf_context': session})
    
    if request.method == 'POST' and form.validate():
        try:
            tag.name = form.tag_name.data
            db_session.commit()
            return redirect(url_for('viewTag', tag_name = tag.name))
        except IntegrityError:
            # If user tries to edit a tag to have the name of another existing
            # tag, roll back and add a form error
            db_session.rollback()
            form.tag_name.errors.append(
                'A tag already exists with that name.')

    elif request.method == 'GET':
        # For GET request, pre-fill details of edited tag
        form.tag_name.data = tag.name

    return render_template('tagform.html',
                           form=form,
                           action="editTag",
                           tag=tag)


@app.route('/catalog/items/edit/<item_name>-<int:item_id>/',
           methods=['GET', 'POST'])
def editItem(item_name, item_id):
    """View to provide a form for editing existing items, and to
    respond POST requests from this form."""
    try:
        item = db_session.query(Item).filter_by(name=item_name,
                                                id=item_id).one()
    except (MultipleResultsFound, NoResultFound):
        # If there is more or less than one item with that name and id,
        # throw a 404
        abort(404)

    form = ItemForm(request.form, meta={'csrf_context': session})

    # Get list of all tags, and add to multiselect
    tags = db_session.query(Tag).all()
    form.tags.choices = [(unicode(g.id), g.name) for g in tags]

    if request.method == 'POST' and form.validate():

        # Get list of tags selected in the form.
        new_tag_ids = map(int, form.tags.data)
        new_tags = db_session.query(Tag).filter(Tag.id.in_(new_tag_ids)).all()
        
        # Edit item.
        item.tags = new_tags
        item.name = form.name.data
        item.description = form.description.data
        db_session.commit()

        return redirect(url_for('viewItem',
                                item_name = item.name,
                                item_id = item.id))
    
    elif request.method == 'GET':
        # For GET requests, pre-fill details of edited item
        form.name.data = item.name
        form.description.data = item.description
        form.tags.data = [unicode(g.id) for g in tags if g in item.tags]
    
    return render_template('itemform.html',
                            form=form,
                            action='editItem',
                            item=item)

# Views for deleting existing entities

@app.route('/catalog/tags/delete/<tag_name>/', methods=['GET', 'POST'])
def deleteTag(tag_name):
    """View to provide a form for deleting existing tags, and to
    respond POST requests from this form."""
    
    try:
        tag = db_session.query(Tag).filter_by(name=tag_name).one()
    except (MultipleResultsFound, NoResultFound):
        # If there are more or less than one tags with this name,
        # throw a 404.
        abort(404)

    form = DeleteForm(request.form, meta={'csrf_context': session})

    if request.method == 'POST' and form.validate():
        db_session.delete(tag)
        db_session.commit()
        return redirect(url_for('index'))

    return render_template('deleteform.html',
                            form=form,
                            action='deleteTag',
                            deleted=tag)

@app.route('/catalog/items/delete/<item_name>-<int:item_id>/',
           methods=['GET', 'POST'])
def deleteItem(item_name, item_id):
    """View to provide a form for deleting existing items, and to
    respond POST requests from this form."""
    try:
        item = db_session.query(Item).filter_by(name=item_name,
                                                id=item_id).one()
    except (MultipleResultsFound, NoResultFound):
        # If there are more or less than one items with this name and id,
        # throw a 404.
        abort(404)

    form = DeleteForm(request.form, meta={'csrf_context': session})

    if request.method == 'POST' and form.validate():
        db_session.delete(item)
        db_session.commit()
        return redirect(url_for('index'))

    return render_template('deleteform.html',
                            form=form,
                            action='deleteItem',
                            deleted=item)
