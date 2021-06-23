from manage import INIT
from flask import session, request, render_template, redirect, url_for
import os
from forms import LoginForm, PostForm, CommentForm

app = INIT.app
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
non_login_list = ['/', '/posts', '/login']
pages = ['/', '/posts', '/login', '/logout']

postsDB, userDB, modActivity, postsDBdict, bans = INIT.postsDB, INIT.userDB, INIT.modActivity, INIT.postsDBdict, INIT.bans


# before any request
@app.before_request
def before_request():
	if session.get('login') == None or session.get('login') == False:
		session['login'] = False
	else:
		if session.get('login')[1] in bans or request.path == '/banned':
			return redirect('/banned')
	if request.path in pages or '/view-post=' in request.path or 'make-me-mod/k=' in request.path or 'comment/p=' in request.path:
		if session.get('login') == False and request.path not in non_login_list:
			session['message'] = 'You need to login to access that page!'
			return redirect(url_for('login'))

# create the create-account and login routes
import accounts
# create all routes for mods
import mods
# create all routes for posting and viewing posts
import posting

# main page
@app.route('/')
def index():
	message = session.get('message')
	session['message'] = None
	return render_template('index.html', message=message, login=session.get('login'))

app.run('0.0.0.0', debug=True)