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

Third-party code
--------------
- The lines in the `Item` model creating the automatically populated and updated `created_on` and `updated_on` columns relies heavily on this Stackoverflow answer:
    + http://stackoverflow.com/a/12155686
- The Atom feed borrows from the following examples:
    + http://flask.pocoo.org/snippets/10/
    + http://werkzeug.pocoo.org/docs/0.11/contrib/atom/