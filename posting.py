from forms import PostForm, CommentForm
from flask import session, redirect, render_template
from manage import INIT
import random

postsDB, userDB, modActivity, postsDBdict = INIT.postsDB, INIT.userDB, INIT.modActivity, INIT.postsDBdict
app = INIT.app

# post	
@app.route('/post', methods=['GET','POST'])
def post():
	form = PostForm()

	if form.validate_on_submit():
		# get form data
		title = form.title.data
		body = form.body.data
		post_id = str(random.randrange(1000000000, 9999999999))
		# add the post to the database
		postsDB.insert(0, {'title': title, 'author': session.get('login')[1], 'content': body, 'comments': [], 'id':post_id})
		userDB[session.get('login')[1]]['posts'].append({'title': title, 'author': session.get('login')[1], 'content': body, 'comments': [], 'id': post_id})
		postsDBdict[title + '-' + post_id] = {'title': title, 'author': session.get('login')[1], 'content': body, 'comments': [], 'id': post_id}
		
		session['message'] = 'You posted ' + title
		return redirect('/view-post='+title+'-'+post_id)


	message = session.get('message')
	session['message'] = None
	return render_template('post.html', form=form, login=session.get('login'), message=message)

@app.route('/posts')
def posts():
	message = session.get('message')
	session['message'] = None
	return render_template('posts.html', posts=postsDB, message=message, login=session.get('login'))

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
