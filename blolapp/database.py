import sqlite3
from flask import g
from blolapp import app

def connect_db():
	"""Connects to the specific database."""
	rv = sqlite3.connect(app.config['DATABASE'])
	rv.row_factory = sqlite3.Row
	return rv

# def init_db():
# 	with app.app_context():
# 		db = get_db()
# 		with app.open_resource('schema.sql', mode ='r') as f:
# 			db.cursor().executescript(f.read())
# 		db.commit()

def get_db():
	"""Opens a new database connection if there is none yet for the current application context."""
	if not hasattr(g, 'sqlite_db'):
		g.sqlite_db = connect_db()
	return g.sqlite_db

def get_entries():
	"""returns entries from db"""
	db = get_db()
	cur = db.execute('select title, text from entries order by id desc ')
	entries = cur.fetchall()
	return entries

#SQLALchemy integration
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine('sqlite:////tmp/test.db', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
										autoflush=False,
										bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
	# import all modules here that might define models so that
	# they will be registered properly on the metadata.  Otherwise
	# you will have to import them first before calling init_db()
	import blolapp.models
	Base.metadata.create_all(bind = engine)

def get_entries():
	"""returns entries from db"""
	db = get_db()
	entries = Entry.query.all()
	return entries