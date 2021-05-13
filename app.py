from manage import INIT
from user_tools import logged_in
from flask import session, request, render_template, redirect, url_for
app = INIT.app
non_login_list = ['/', '/view-questions', '/login']
pages = ['/', '/view-quesions', '/login', '/logout']
@app.before_request
def before_request():
	if request.path in pages or '/question=' in request.path:
		if logged_in() == False and request.path not in non_login_list:
			session['message'] = 'You need to login to access that page!'
			return redirect(url_for('login'))

@app.route('/')
def index():
	return render_template('index.html', logged_in=logged_in)



@app.route('/login')
def login():
	return render_template('login.html')

app.run('0.0.0.0')