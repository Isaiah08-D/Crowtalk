from forms import LoginForm
from flask import session, redirect, render_template
from manage import INIT

postsDB, userDB, modActivity, postsDBdict = INIT.postsDB, INIT.userDB, INIT.modActivity, INIT.postsDBdict
app = INIT.app

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
				if userDB[username]['status'] == 'user':
					session['login'] = [True, username, userDB[username]['status']]
					return redirect('/')
				else:
					session['login'] = ['mod', username, userDB[username]['status']]
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

# logout
@app.route('/logout')
def logout():
	session['login'] = False
	session['message'] = 'Logged out!'
	message = session.get('message')
	session['message'] = None
	return render_template('index.html', login=session.get('login'), message=message)

# user profile
@app.route('/user=<username>')
def user(username):
	message = session.get('message')
	session['message'] = None

	if username not in userDB:
		return render_template('error.html', error='User not found.', login=session.get('login'), message=message)
	return render_template('user.html', username=username, userinfo=userDB[username], message=message, login=session.get('login'))