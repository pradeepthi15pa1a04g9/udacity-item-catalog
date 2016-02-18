import os
from flask import Flask
app = Flask(__name__, instance_relative_config=True)

# Load default configuration
app.config.from_object('catalog.config.default')

# Load the configuration from the instance folder
app.config.from_pyfile('config.py')

# If the CATALOG_APP_CONFIG_FILE environment variable 
# is set, load this config file as well.
# Variables defined here will override those in the 
# default configuration
env_config_file = os.getenv('CATALOG_APP_CONFIG_FILE')
if env_config_file:
	app.config.from_envvar(env_config_file)


# Allow logging
if app.config.get('ENABLE_LOGGING'):
    print "Logging active"
    from .logging_config import start_logging
    start_logging(app)

from . import views