from . import app

@app.route('/')
@app.route('/catalog/')
def index():
    return 'This page shows all tags and items.'

# Views for viewing data in web page form

@app.route('/catalog/tags/view/<tag>/')
def viewTag(tag):
    return 'This page shows the items in the category: %s.' % tag

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

@app.route('/catalog/tags/edit/<tag>/')
def editTag(tag):
    return "This page lets you edit the existing tag: %s." % tag

@app.route('/catalog/items/edit/<item_name>-<int:item_id>/')
def editItem(item_name, item_id):
    return 'This page lets you edit the existing item called "%s" with the id %s.' % (item_name, item_id)

# Views for deleting existing entities

@app.route('/catalog/tags/delete/<tag>/')
def deleteTag(tag):
    return "This page lets you delete the existing tag: %s." % tag

@app.route('/catalog/items/delete/<item_name>-<int:item_id>/')
def deleteItem(item_name, item_id):
    return 'This page lets you delete the existing item called "%s" with the id %s.' % (item_name, item_id)