from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

# create our little application
app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
app.config.from_pyfile('config.py')

#creates sqlalchemy engine and binds base metadata
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from config import DATABASE

Base = declarative_base()

engine = create_engine('sqlite:///' + DATABASE, convert_unicode=True)
Base.metadata.bind = engine
db_session = scoped_session(sessionmaker(autocommit=False,
										autoflush=False,
										bind=engine))

Base.query = db_session.query_property()

#imports Login Manager
from flask.ext.login import LoginManager

lm = LoginManager()
lm.init_app(app)

from blolapp import views, models, forms