from manage import INIT
from db import postsDB, userDB
from user_tools import logged_in
from flask import session, request, render_template, redirect, url_for, flash
from forms import LoginForm
app = INIT.app
non_login_list = ['/', '/view-questions', '/login']
pages = ['/', '/view-quesions', '/login', '/logout']

# before any request
@app.before_request
def before_request():
	if session.get('login') == None:
		session['login'] = False
	if request.path in pages or '/view-post=' in request.path:
		if session.get('login') == False and request.path not in non_login_list:
			session['message'] = 'You need to login to access that page!'
			return redirect(url_for('login'))
	


# main page
@app.route('/')
def index():
	message = session.get('message')
	session['message'] = None
	return render_template('index.html', logged_in=logged_in, message=message, login=session.get('login'))

# login
@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		# get form data
		username = form.username.data
		password = form.password.data
		# check for valid login
		if username in userDB:
			if userDB[username]['password'] == password:
				session['login'] = True
				return redirect('/')
			else:
				session['message'] = 'Your password is incorrect.'
				return redirect('/login')
		else:
			session['message'] = 'Your password is incorrect.'
			return redirect('/login')
	message = session.get('message')
	session['message'] = None
	return render_template('login.html', form=form, message=message, login=session.get('login'))

@app.route('/create-account')
def create_account():
	form = LoginForm()
	if form.validate_on_submit():
		username = form.username.data
		password = form.password.data

		if username in userDB:
			session['message'] = 'That username is already taken!'

# view a single post
@app.route('/view-post=<post>')
def view_post(post):
	# requires message update!
	return render_template('view_post.html', post=postsDB[post], login=session.get('login'))
app.run('0.0.0.0')