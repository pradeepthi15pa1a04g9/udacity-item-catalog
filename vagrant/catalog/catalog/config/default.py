"""Sample configuration file. Needs to be overridden by a configuration file
in ../instance/config.py"""

import os

SECRET_KEY = 'development key'
CSRF_SECRET_KEY = b'development csrf key'

# Non-standard, specific to this app
ENABLE_LOGGING = True

CATALOG_LOGFILE = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        '..',
        'catalog.log'))

# Default sqlite database

DB_FILE = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        '..',
        'catalog.db'))

DB_URL = ''