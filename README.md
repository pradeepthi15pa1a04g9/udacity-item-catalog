udacity-item-catalog
=============
Forked from: udacity/rdb-fullstack

JSON API endpoints
-------------
- /catalog.json
    + Shows information on all tags and all items, referenced from 'Items' and 'Tags' keys
- /catalog/items.json
    + Shows only the 'Items' portion of the information in /catalog.json
- /catalog/tags.json
    + Shows only the 'Tags' portion of the information in /catalog.json
- /catalog/tags/view/\<tag_name>.json
    + Shows information for the tag with name <tag_name>
- /catalog/items/view/\<item_name>-\<int:item_id>.json
    + Shows information for the tag with the specified name and id

Atom Feed
--------------
An atom feed of the latest items can be accessed at /catalog/recent.atom .

Logging
--------------
Creation, deletion and editing of tags and items is recorded in a log file, configured by default as `catalog.log` in /vagrant/catalog/ .

Third-party code
--------------
- The lines in the `Item` model creating the automatically populated and updated `created_on` and `updated_on` columns relies heavily on this Stackoverflow answer:
    + http://stackoverflow.com/a/12155686
- The Atom feed borrows from the following examples:
    + http://flask.pocoo.org/snippets/10/
    + http://werkzeug.pocoo.org/docs/0.11/contrib/atom/
- The logging feature was created with help from the following tutorials and examples:
    + http://flask.pocoo.org/docs/0.10/quickstart/#logging
    + https://gist.github.com/ibeex/3257877
    + https://docs.python.org/2/howto/logging.html
- The Oauth code takes Udacity code samples as a starting point, but modifed these to use WTForms CSRF features and add other functionality:
    + https://github.com/udacity/ud330/blob/master/Lesson2/step5/project.py
    + https://github.com/udacity/ud330/blob/master/Lesson2/step4/templates/login.html
