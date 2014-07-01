#SQLALchemy integration
from blolapp import Base, db_session
from sqlalchemy import create_engine
from models import Post
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
	posts = db_session.query(Post).all()
	return posts