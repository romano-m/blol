from flask.ext.wtf import Form
from wtforms import TextField, TextAreaField, SubmitField, validators, ValidationError, PasswordField, TextAreaField
from wtforms.validators import Required, EqualTo, Email
from models import Base, User

class SignupForm(Form):
	username = TextField("username", [Required("Please enter your username.")])
	email = TextField("Email", [Required("Please enter your email."), Email("Invalid email address.")])
	password = PasswordField('Password', [Required(), EqualTo('confirm', message='Passwords must match')])
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

class SigninForm(Form):
	email = TextField("Email", [Required("Please enter your email."), Email("Invalid email address.")])
	password = PasswordField('Password', [validators.Required("Please enter your password.")])
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

class AddPost(Form):
	title = TextField("Title", [validators.Required("Please type a title.")])
	text = TextAreaField("Text", [validators.Required("Please type some text.")])
	submit = SubmitField("Post")

	def __init__(self, *args, **kwargs):
		Form.__init__(self, *args, **kwargs)

	def validate(self):
		if not Form.validate(self):
			return False