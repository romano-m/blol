from blolapp import app, db_session
from flask import Flask, request, redirect,url_for, abort, render_template, flash, session
from sqlalchemy import func
from models import Post, User
from forms import SignupForm, SigninForm, AddPost

@app.route('/', methods=['POST', 'GET'])
def home():

	posts = Post.query.order_by('posted_on desc').all()
	form = AddPost()

	if request.method == 'GET':
		if 'email' in session:
			user_in_session = User.query.filter_by(email = session['email']).first()
			user_in_session_username = user_in_session.username
			return render_template('home.html',
								posts = posts,
								user_in_session_username = user_in_session_username,
								form=form)
		else:
			return render_template('home.html',
								posts = posts,
								form = form)

	if request.method == 'POST':
		if form.validate() == False:
			return render_template('add_entry',
									form=form)

		else:
			user_in_session = User.query.filter_by(email = session['email']).first()
			user_in_session_username = user_in_session.username
			post = Post(form.title.data, 
					form.text.data, 
					posted_on = func.now(),
					user_id = user_in_session.id)
			db_session.add(post)
			db_session.commit()
			flash('New entry was successfully posted')
			return redirect(url_for('home'))


@app.route('/add', methods=['POST', 'GET'])
def add_entry():

	if not 'email' in session:
		abort(401)

	user_in_session = User.query.filter_by(email = session['email']).first()
	form = AddPost()

	if request.method == 'POST':
		if form.validate() == False:
			return render_template('add_entry',
									form=form)

		else:
			post = Post(form.title.data, 
					form.text.data, 
					posted_on = func.now(),
					user_id = user_in_session.id)
			db_session.add(post)
			db_session.commit()
			flash('New entry was successfully posted')
			return redirect(url_for('home'))

	if request.method == 'GET':
		return render_template('add_entry.html',
								form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():

	form = SignupForm()

	if 'email' in session:
		return redirect(url_for('home'))

	if request.method == 'POST':
		if form.validate() == False:
			return render_template('signup.html', 
									form=form)
		else:
			newuser = User(form.username.data, form.email.data, form.password.data)
			db_session.add(newuser)
			db_session.commit()

			session['email'] = newuser.email

			return redirect(url_for('home'))
	
	elif request.method == 'GET':
		return render_template('signup.html',
								form=form)

@app.route('/profile')
def profile():

	if 'email' not in session:
		return redirect(url_for('signin'))

	user_in_session = User.query.filter_by(email = session['email']).first()
	user_in_session_username = user_in_session.username
	user_in_session_id = user_in_session.id
	user_in_session_posts = Post.query.filter_by(user_id = user_in_session_id).order_by('posted_on desc').all()

	if user_in_session is None:
		return redirect(url_for('signin'))
	else:
		return render_template('profile.html',
								user_in_session_username= user_in_session_username,
								user_in_session_posts=user_in_session_posts)


@app.route('/signin', methods=['GET', 'POST'])
def signin():

	form = SigninForm()

	if 'email' in session:
		return redirect(url_for('home'))

	if request.method == 'POST':
		if form.validate()==False:
			return render_template('signin.html', form=form)
		else:
			session['email'] = form.email.data
			return redirect(url_for('home'))

	elif request.method == 'GET':
			return render_template('signin.html', form=form)

@app.route('/signout')
def signout():

	if 'email' not in session:
		return redirect(url_for('signin'))

	session.pop('email', None)
	return redirect(url_for('home'))

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()