from flask import Flask, request, session, redirect,url_for, abort, render_template, flash
from blolapp import app, db_session
from database import get_posts
from models import Post

@app.route('/')
def show_entries():
	return render_template('show_entries.html', posts=get_posts())

@app.route('/add', methods=['POST'])
def add_entry():
	if not session.get('logged_in'):
		abort(401)
	p = Post(title = request.form['title'], text = request.form['text'])
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
	return render_template('login.html', error=error)

@app.route('/logout')
def logout():
	session.pop('logged_in', None)
	flash('You were logged out')
	return redirect(url_for('show_entries'))

#SQLALchemy integration
from blolapp import db_session

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()