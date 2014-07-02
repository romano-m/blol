from blolapp import app, db_session
from flask import Flask, request, session, redirect,url_for, abort, render_template, flash
from sqlalchemy import func
from models import Post, User
from forms import SignupForm, SigninForm

@app.route('/')
def show_entries():
	return render_template('show_entries.html',
							posts = db_session.query(Post).all())

@app.route('/add', methods=['POST'])
def add_entry():
	if not session.get('logged_in'):
		abort(401)
	p = Post(title = request.form['title'], 
			text = request.form['text'], 
			posted_on = func.now())
	db_session.add(p)
	db_session.commit()
	flash('New entry was successfully posted')
	return redirect(url_for('show_entries'))

@app.route('/login', methods=['GET', 'POST'])
def login():
	error = None
	if request.method == 'POST':
		if request.form['username'] != app.config['USERNAME']:
			error = 'invalid username'
		elif request.form['password'] != app.config['PASSWORD']:
			error = 'invalid password'
		else:
			session['logged_in'] = True
			flash('You were logged in')
			return redirect(url_for('show_entries'))
	return render_template('login.html',
								error=error)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
	form = SignupForm()

	if request.method == 'POST':
		if form.validate() == False:
			return render_template('signup.html', form=form)
		else:
			newuser = User(form.username.data, form.email.data, form.password.data)
			db_session.add(newuser)
			db_session.commit()

			session['email'] = newuser.email

			return redirect(url_for('show_entries'))
	
	elif request.method == 'GET':
		return render_template('signup.html', form=form)

@app.route('/profile')
def profile():
	if 'email' not in session:
		return redirect(url_for('signin'))

	user = User.query.filter_by(email = session['email']).first()

	if user is None:
		return redirect(url_for('signin'))
	else:
		return render_template('profile.html')

@app.route('/signin', methods=['GET', 'POST'])
def signin():
	form = SigninForm()

	if request.method == 'POST':
		if form.validate()==False:
			return render_template('signin.html', form=form)
		else:
			session['email'] = form.email.data
			return redirect(url_for('profile'))

	elif request.method == 'GET':
		if 'email' not in session:
			return render_template('signin.html', form=form)
		else:
			return redirect(url_for('profile'))

@app.route('/signout')
def signout():
	if 'email' not in session:
		return redirect(url_for('signin'))

	session.pop('email', None)
	return redirect(url_for('show_entries'))

@app.route('/logout')
def logout():
	session.pop('logged_in', None)
	flash('You were logged out')
	return redirect(url_for('show_entries'))

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()