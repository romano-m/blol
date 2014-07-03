from sqlalchemy import Column, Integer, String, SmallInteger, ForeignKey, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from blolapp import Base
from werkzeug import generate_password_hash, check_password_hash


class Post(Base):

	__tablename__ = 'posts'

	id = Column(Integer, primary_key = True)
	title = Column(String(50), nullable = False)
	text = Column(String(140), nullable = False)
	posted_on = Column(DateTime, default=func.now())
	user_id = Column(Integer, ForeignKey('users.id'))
	user = relationship("User", backref = "posts")

	def __init__(self, title, text, posted_on, user_id):
		self.title = title
		self.text = text
		self.posted_on = posted_on
		self.user_id = user_id

	def __repr__(self):
		return '<Post %r>' % (self.text)



class User(Base):

	__tablename__ = 'users'
	# __table_args__ = {'extend_existing': True}

	id = Column(Integer, primary_key = True)
	username = Column(String(64), index = True, unique = True)
	email = Column(String(120), index = True, unique = True)
	pwdhash = Column(String(54))

	def __init__(self, username, email, password):
		self.username = username
		self.email = email
		self.set_password(password)

	def set_password(self, password):
		self.pwdhash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.pwdhash, password)

	def is_authenticated(self):
		return True

	def is_active(self):
		return True

	def is_anonymous(self):
		return False

	def get_id(self):
		return unicode(self.id)

	def __repr__(self):
		return '<User %r>' % (self.username)