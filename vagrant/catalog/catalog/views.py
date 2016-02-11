from flask import render_template, abort, request, session

from . import app
from .forms import TagForm, ItemForm

@app.route('/')
@app.route('/catalog/')
def index():
    return render_template('catalog.html', tags=tags.values(), items=items)

# Views for viewing data in web page form

@app.route('/catalog/tags/view/<tag_name>/')
def viewTag(tag_name):
    try:
        tag = tags[tag_name]
    except KeyError:
        abort(404)
    return render_template('viewtag.html', tag=tag)

@app.route('/catalog/items/view/<item_name>-<int:item_id>/')
def viewItem(item_name, item_id):
    if item_name in itemindex and itemindex[item_name].id == item_id:
        item = itemindex[item_name]
        return render_template('viewitem.html', item=item, item_id=item_id)
    else:
        abort(404)

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
    form.tags.choices = [(g, g) for g in tags]
    if request.method == 'POST' and form.validate():
        return "No code for handling posted forms yet. Here is the request data:<br><br><pre>%s</pre>" % request.values
    return render_template('itemform.html', form=form, action='newItem')

# Views for editing existing entities

@app.route('/catalog/tags/edit/<tag_name>/', methods=['GET', 'POST'])
def editTag(tag_name):
    form = TagForm(request.form, meta={'csrf_context': session})
    try:
        # Prefill details of edited tag
        form.tag_name.data = tags[tag_name].name
    except KeyError:
        abort(404)
    if request.method == 'POST' and form.validate():
        return "No code for handling posted forms yet. Here is the request data:<br><br><pre>%s</pre>" % request.values
    return render_template('tagform.html', form=form, action="editTag", tag_name=tag_name)    

@app.route('/catalog/items/edit/<item_name>-<int:item_id>/', methods=['GET', 'POST'])
def editItem(item_name, item_id):
    item = itemindex[item_name]
    form = ItemForm(request.form, meta={'csrf_context': session})
    form.tags.choices = [(g, g) for g in tags]
    
    # Prefill details of edited item
    form.name.data = item.name
    #form.description.data = item.description
    form.tags.data = [g.name for g in tags.values() if g in item.tags]

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

# Mock up objects to make the templates work.
# REMOVE ONCE PROPER DATABASE IN PLACE:

class Tag(object):

    def __init__(self, name, itemlist):
        self.name = name
        self.itemlist = itemlist # The list in which all the items are stored

    @property
    def items(self):
        return [item for item in self.itemlist if self in item.tags]

class Item(object):

    def __init__(self, name, id, itemlist, itemindex):
        self.name = name
        self.id = id
        self.tags = []
        self.itemlist = itemlist
        self.itemindex = itemindex
        self.itemlist.append(self)
        self.itemindex[self.name] = self

    def addTag(self, tag_name):
        if tag_name in tags.keys():
            self.tags.append(tags[tag_name])

items = []

itemindex = dict()

tags = {
    'Cars': Tag('Cars', items),
    'Bikes': Tag('Bikes', items),
    'Boats': Tag('Boats', items),
    'Vehicles': Tag('Vehicles', items),
}

item1 = Item('Ford Focus', 1, items, itemindex)
item1.addTag('Cars')
item1.addTag('Vehicles')
item1.description = "A really reliable car."

item2 = Item('Rowing boat', 2, items, itemindex)
item2.addTag('Boats')
item2.addTag('Vehicles')

item3 = Item('BMX', 3, items, itemindex)
item3.addTag('Bikes')
item3.addTag('Vehicles')

item4 = Item('Skoda', 4, items, itemindex)
item4.addTag('Cars')
item4.addTag('Vehicles')

item5 = Item('Rover the Dog', 5, items, itemindex)
item5.description = "A very good dog."