from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

# create our little application
app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
app.config.from_pyfile('config.py')

from blolapp import views, models