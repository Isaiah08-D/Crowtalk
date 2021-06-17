from forms import BanForm
from flask import session, redirect, render_template
from manage import INIT
import os

postsDB, userDB, modActivity, postsDBdict = INIT.postsDB, INIT.userDB, INIT.modActivity, INIT.postsDBdict
app = INIT.app

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

@app.route('/mod-activity')
def mod_activity():
	return render_template('mod-activity.html', login=session.get('login'), modActivity=modActivity)

@app.route('/ban/u=<user>', methods=['GET', 'POST'])
def ban(user):
	form = BanForm()

	if form.validate_on_submit():
		period = form.period.data

		userDB[user]['status'] = 'banned'
		modActivity.insert(0, session.get('login')[1] + ' banned ' + user + ' until ' + period + '.')
	message = session.get('message')
	session['message'] = None

	return render_template('banned.html', login=session.get('login'), message=message, form=form)

@app.route('/banned')
def banned():
	return render_template('banned.html', login=session.get('login'))