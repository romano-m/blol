from blolapp import app, db_session
from flask import Flask, request, redirect,url_for, abort, render_template, flash, session
from sqlalchemy import func
from models import Post, User
from forms import SignupForm, SigninForm

@app.route('/')
def home():

	posts = Post.query.all()

	return render_template('home.html',
							posts = posts)


@app.route('/add', methods=['POST', 'GET'])
def add_entry():

	if not 'email' in session:
		abort(401)

	if request.method == 'POST':
		p = Post(title = request.form['title'], 
				text = request.form['text'], 
				posted_on = func.now())
		db_session.add(p)
		db_session.commit()
		flash('New entry was successfully posted')
		return redirect(url_for('home'))

	if request.method == 'GET':
		return render_template('add_entry.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():

	form = SignupForm()

	if 'email' in session:
		return redirect(url_for('home'))

	if request.method == 'POST':
		if form.validate() == False:
			return render_template('signup.html', form=form)
		else:
			newuser = User(form.username.data, form.email.data, form.password.data)
			db_session.add(newuser)
			db_session.commit()

			session['email'] = newuser.email

			return redirect(url_for('home'))
	
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