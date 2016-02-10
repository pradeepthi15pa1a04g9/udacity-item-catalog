from . import app
from flask import render_template, abort

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
    return 'This page shows the item called "%s" with the id %s.' % (item_name, item_id)

# Views for creating new data entities

@app.route('/catalog/tags/new/')
def newTag():
    return "This page lets you create a new tag."

@app.route('/catalog/items/new/')
def newItem():
    return "This page lets you create a new item."

# Views for editing existing entities

@app.route('/catalog/tags/edit/<tag_name>/')
def editTag(tag_name):
    return "This page lets you edit the existing tag: %s." % tag_name

@app.route('/catalog/items/edit/<item_name>-<int:item_id>/')
def editItem(item_name, item_id):
    return 'This page lets you edit the existing item called "%s" with the id %s.' % (item_name, item_id)

# Views for deleting existing entities

@app.route('/catalog/tags/delete/<tag_name>/')
def deleteTag(tag_name):
    return "This page lets you delete the existing tag: %s." % tag_name

@app.route('/catalog/items/delete/<item_name>-<int:item_id>/')
def deleteItem(item_name, item_id):
    return 'This page lets you delete the existing item called "%s" with the id %s.' % (item_name, item_id)

# Mock up objects to make the templates work.
# REMOVE ONCE PROPER DATABASE IN PLACE:
from collections import namedtuple

class Tag(object):

    def __init__(self, name, itemlist):
        self.name = name
        self.itemlist = itemlist # The list in which all the items are stored

    @property
    def items(self):
        return [item for item in self.itemlist if self in item.tags]

class Item(object):

    def __init__(self, name, id):
        self.name = name
        self.id = id
        self.tags = []
    def addTag(self, tag_name):
        if tag_name in tags.keys():
            self.tags.append(tags[tag_name])

items = []

tags = {
    'Cars': Tag('Cars', items),
    'Bikes': Tag('Bikes', items),
    'Boats': Tag('Boats', items),
    'Vehicles': Tag('Vehicles', items),
}

item1 = Item('Ford Focus', 1)
item1.addTag('Cars')
item1.addTag('Vehicles')
items.append(item1)

item2 = Item('Rowing boat', 2)
item2.addTag('Boats')
item2.addTag('Vehicles')
items.append(item2)

item3 = Item('BMX', 3)
item3.addTag('Bikes')
item3.addTag('Vehicles')
items.append(item3)

item4 = Item('Skoda', 4)
item4.addTag('Cars')
item4.addTag('Vehicles')
items.append(item4)

item5 = Item('Rover the Dog', 5)
items.append(item5)