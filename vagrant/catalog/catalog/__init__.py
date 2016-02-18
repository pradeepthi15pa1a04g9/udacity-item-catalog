from flask import Flask
app = Flask(__name__, instance_relative_config=True)

app.config.from_object('catalog.config')
app.config.from_pyfile('config.py')

# Allow logging
if app.config.get('ENABLE_LOGGING'):
    print "Logging active"
    from .logging_config import start_logging
    start_logging(app)

from . import views