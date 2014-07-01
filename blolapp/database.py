# import sqlite3
# from flask import g
# from blolapp import app

# def connect_db():
# 	"""Connects to the specific database."""
# 	rv = sqlite3.connect(app.config['DATABASE'])
# 	rv.row_factory = sqlite3.Row
# 	return rv

# def init_db():
# 	with app.app_context():
# 		db = get_db()
# 		with app.open_resource('schema.sql', mode ='r') as f:
# 			db.cursor().executescript(f.read())
# 		db.commit()

# def get_db():
# 	"""Opens a new database connection if there is none yet for the current application context."""
# 	if not hasattr(g, 'sqlite_db'):
# 		g.sqlite_db = connect_db()
# 	return g.sqlite_db

# def get_posts():
# 	"""returns entries from db"""
# 	db = get_db()
# 	cur = db.execute('select title, text from entries order by id desc ')
# 	entries = cur.fetchall()
# 	return entries

#SQLALchemy integration
from blolapp import Base
from sqlalchemy import create_engine
from models import Post, User
from config import DATABASE

def init_db():
	# import all modules here that might define models so that
	# they will be registered properly on the metadata.  Otherwise
	# you will have to import them first before calling init_db()
	import models
	engine = create_engine('sqlite:///'+ DATABASE)
	Base.metadata.create_all(bind = engine)

def get_posts():
	"""returns entries from db"""
	entries = Post.query.all()
	return entries