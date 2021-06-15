from manage import INIT
from flask import session, request, render_template, redirect, url_for
import os
from forms import LoginForm, PostForm, CommentForm
app = INIT.app
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
non_login_list = ['/', '/posts', '/login']
pages = ['/', '/posts', '/login', '/logout']
postsDB, userDB, modActivity, postsDBdict = INIT.postsDB, INIT.userDB, INIT.modActivity, INIT.postsDBdict
# before any request
@app.before_request
def before_request():
	if session.get('login') == None:
		session['login'] = False
	if request.path in pages or '/view-post=' in request.path or 'make-me-mod/k=' in request.path or 'comment/p=' in request.path:
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
				session['login'] = (True, username, userDB[username]['status'])
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

# create an account
@app.route('/create-account', methods=['GET', 'POST'])
def create_account():
	form = LoginForm()
	if form.validate_on_submit():
		#get form data
		username = form.username.data
		password = form.password.data
		# If the username is already taken
		if username in userDB:
			session['message'] = 'That username is already taken!'
			return redirect('/create-account')
		# otherwise, create the account
		userDB[username] = {'password': password, 'posts':[], 'caws': 0, 'status': 'normal', 'position':'user'}
		# let the computer know that you're logged in
		session['login'] = (True, username, userDB[username]['status'])
		session['message'] = 'Logged in!'

	message = session.get('message')
	session['message'] = None

	return render_template('create-account.html', form=form, message=message, login=session.get('login'))

@app.route('/make-me-mod/k=<modkey>')
def make_me_mod(modkey):
	real_key = os.getenv('MOD_KEY')
	if modkey == real_key:
		userDB[session.get('login')[1]]['position'] = 'mod'
		modActivity.append(session.get('login')[1] + ' became a mod.')
		session['login'][2] = 'mod'
		session['message'] = 'Congrats! You\'re now a mod!'
		return redirect('/')
	session['message'] = 'That key is not correct.'
	return redirect('/')


# post	
@app.route('/post', methods=['GET','POST'])
def post():
	form = PostForm()

	if form.validate_on_submit():
		# get form data
		title = form.title.data
		body = form.body.data
		# add the post to the database
		postsDB.insert(0, {'title': title, 'author': session.get('login')[1], 'content': body, 'comments': []})
		userDB[session.get('login')[1]]['posts'].append({'title': title, 'author': session.get('login')[1], 'content': body, 'comments': []})
		postsDBdict[title] = {'title': title, 'author': session.get('login')[1], 'content': body, 'comments': []}
		
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

	return render_template('view-post.html', post=postsDBdict[post], login=session.get('login'), message=message)


@app.route('/comment/p=<post>', methods=['GET', 'POST'])
def comment(post):
	form = CommentForm()

	if form.validate_on_submit():
		comment = form.comment.data

		postsDBdict[post]['comments'].append([session.get('login')[1], comment])
		return redirect('/view-post='+post)

	message = session.get('message')
	session['message'] = None
	return render_template('comment.html', login=session.get('login'), message=message, post=postsDBdict[post], form=form)


# user profile
@app.route('/user=<username>')
def user(username):
	message = session.get('message')
	session['message'] = None

	if username not in userDB:
		return render_template('error.html', error='User not found.', login=session.get('login'), message=message)
	return render_template('user.html', username=username, userinfo=userDB[username], message=message, login=session.get('login'))

app.run('0.0.0.0', debug=True)