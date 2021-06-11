from manage import INIT
from db import postsDB, userDB
from flask import session, request, render_template, redirect, url_for
import os
from forms import LoginForm, PostForm
app = INIT.app
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
non_login_list = ['/', '/posts', '/login']
pages = ['/', '/posts', '/login', '/logout']

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
	return render_template('index.html', message=message, login=session.get('login'))

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
				session['login'] = [True, username]
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

@app.route('/create-account', methods=['GET', 'POST'])
def create_account():
	form = LoginForm()
	if form.validate_on_submit():
		username = form.username.data
		password = form.password.data

		if username in userDB:
			session['message'] = 'That username is already taken!'
			return redirect('/create-account')
		userDB[username] = {'password': password, 'posts':[], 'caws': 0}
		session['login'] = (True, username)
		session['message'] = 'Logged in!'

	message = session.get('message')
	session['message'] = None
	return render_template('login.html', form=form, message=message, login=session.get('login'))
	return render_template('create_account.html', form=form)
		
@app.route('/post', methods=['GET','POST'])
def post():
	form = PostForm()

	if form.validate_on_submit():
		title = form.title.data
		body = form.body.data

		postsDB[title] = {'title': title, 'author': session.get('login')[1], 'content': body}
		print(session.get('login'))
		userDB[session.get('login')[1]]['posts'].append({'title': title, 'author': session.get('login')[1], 'content': body})
		session['message'] = 'You posted ' + title
		return redirect('/view-post='+title)


	message = session.get('message')
	session['message'] = None
	return render_template('post.html', form=form, login=session.get('login'), message=message)

@app.route('/posts')
def posts():
	message = session.get('message')
	session['message'] = None
	return render_template('posts.html', posts=postsDB, message=message, login=session.get('login'))

@app.route('/logout')
def logout():
	session['login'] = False
	session['message'] = 'Logged out!'
	message = session.get('message')
	session['message'] = None
	return render_template('index.html', login=session.get('login'), message=message)

# view a single post
@app.route('/view-post=<post>')
def view_post(post):
	message = session.get('message')
	session['message'] = None

	return render_template('view-post.html', post=postsDB[post], login=session.get('login'), message=message)

# user profile
@app.route('/user=<username>')
def user(username):
	message = session.get('message')
	session['message'] = None

	if username not in userDB:
		return render_template('error.html', error='User not found.', login=session.get('login'), message=message)
	return render_template('user.html', username=username, userinfo=userDB[username], message=message, login=session.get('login'))
app.run('0.0.0.0')