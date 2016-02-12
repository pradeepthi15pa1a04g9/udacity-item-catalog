udacity-item-catalog
=============
Forked from: udacity/rdb-fullstack

JSON API endpoints
-------------
- /catalog.json'
    + Shows information on all tags and all items, referenced from 'Items' and 'Tags' keys
- /catalog/items.json
    + Shows only the 'Items' portion of the information in /catalog.json
- /catalog/tags.json1
    + Shows only the 'Tags' portion of the information in /catalog.json
- /catalog/tags/view/<tag_name>.json
    + Shows information for the tag with name <tag_name>
- /catalog/items/view/<item_name>-<int:item_id>.json
    + Shows information for the tag with the specified name and id