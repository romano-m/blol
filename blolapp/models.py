from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from database import Base

ROLE_USER = 0
ROLE_ADMIN = 1

class User(db.Model):

	__tablename__ = 'users'

	id = db.Column(db.Integer, primary_key = True)
	username = db.Column(db.String(64), index = True, unique = True)
	email = db.Column(db.String(120), index = True, unique = True)
	role = db.Column(db.SmallInteger, default = ROLE_USER)
	posts = db.relationship('Post', backref = 'author', lazy = 'dynamic')

	def __init__(self, username = None, email = None, role = None):
		self.username = username
		self.email = email
		self.role = role
		self.posts = posts

	def __repr__(self):
		return '<User %r>' % (self.name)

class Entry(db.Model):

	__tablename__ = 'entries'

	id = db.Column(db.Integer, primary_key = True)
	text = db.Column(db.String(140))
	timestamp = db.Column(db.DateTime)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

	# def __init__(self, text, timestamp = None, user_id):
	# 	self.text = text
	# 	if timestamp is None:
	# 		timestamp = datetime.utcnow()
	# 	self.user_id = user_id

	def __repr__(self):
		return '<Entry %r>' % (self.text)