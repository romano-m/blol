from flask.ext.wtf import Form
from wtforms import TextField, TextAreaField, SubmitField, validators, ValidationError, PasswordField, TextAreaField
from wtforms.validators import Required, EqualTo, Email, Length
from models import Base, User

#Passer plus tard sur du wtforms - sqlalchemy

#formulaire de création de compte 
class SignupForm(Form):
	username = TextField("username", 
						[Required("Please enter your username."),
						Length(max=64, message='Your username should be shorter')])

	email = TextField("Email", 
						[Required("Please enter your email."), 
						Email("Invalid email address."),
						Length(max=120, message='Your email should be shorter')])

	password = PasswordField('Password', 
						[Required(), 
						EqualTo('confirm', message='Passwords must match'),
						Length(max=64, message='Your password should be shorter')])

	confirm = PasswordField('Repeat Password')

	submit = SubmitField("Create account")

	def __init__(self, *args, **kwargs):
		Form.__init__(self, *args, **kwargs)

	def validate(self):
		if not Form.validate(self):
			return False

		user = User.query.filter_by(email = self.email.data.lower()).first()
		if user:
			self.email.errors.append("That email is already taken")
			return False
		else:
			return True

#formulaire de sign in
class SigninForm(Form):
	email = TextField("Email", 
						[Required("Please enter your email."), 
						Email("Invalid email address.")])

	password = PasswordField('Password',
	[validators.Required("Please enter your password.")])

	submit = SubmitField("Sign In")

	def __init__(self, *args, **kwargs):
		Form.__init__(self, *args, **kwargs)

	def validate(self):
		if not Form.validate(self):
			return False

		user = User.query.filter_by(email = self.email.data.lower()).first()
		if user and user.check_password(self.password.data):
			return True
		else:
			self.email.errors.append("Invalid e-mail or password")
			return False

#formulaire d'ajout de posts
class AddPost(Form):
	title = TextField("Title", 
						[Required("Please type a title."),
						Length(max=50, message='Your title cannot exceed 50 characters')])

	text = TextAreaField("Text", 
						[Required("Please type some text."),
						Length(max=140, message='Yout text cannot exceed 140 characters')])

	submit = SubmitField("Post")

	def __init__(self, *args, **kwargs):
		Form.__init__(self, *args, **kwargs)

	def validate(self):
		if not Form.validate(self):
			return False