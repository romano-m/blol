from sqlalchemy import Column, Integer, String, SmallInteger, ForeignKey, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from blolapp import Base

ROLE_USER = 0
ROLE_ADMIN = 1


class Post(Base):

	__tablename__ = 'posts'

	id = Column(Integer, primary_key = True)
	title = Column(String(50), nullable = False)
	text = Column(String(140), nullable = False)
	posted_on = Column(DateTime, default=func.now())
	user_id = Column(Integer, ForeignKey('users.id'))
	user = relationship("User", backref = "posts")

	def __init__(self, title, text, posted_on):
		self.title = title
		self.text = text
		self.posted_on = posted_on

	def __repr__(self):
		return '<Post %r>' % (self.text)


class User(Base):

	__tablename__ = 'users'
	__table_args__ = {'extend_existing': True}

	id = Column(Integer, primary_key = True)
	username = Column(String(64), index = True, unique = True)
	email = Column(String(120), index = True, unique = True)
	role = Column(SmallInteger, default = ROLE_USER)

	def __init__(self, username, email, role):
		self.username = username
		self.email = email
		self.role = role

	def __repr__(self):
		return '<User %r>' % (self.username)