from wtforms import StringField, SubmitField, PasswordField
import os
from wtforms.validators import Required
from flask_wtf import FlaskForm

class LoginForm(FlaskForm):
	username = StringField('Username: ', validators=[Required()])
	password = PasswordField('Password: ', validators=[Required()])
	submit = SubmitField('Login')

class PostForm(FlaskForm):
	title = StringField('Title: ', validators=[Required()])
	body = StringField('Post: ', validators=[Required()])
	submit = SubmitField('Post')

class CommentForm(FlaskForm):
	comment = StringField('Text: ', validators=[Required()])
	submit = SubmitField('Comment')

class BanForm(FlaskForm):
	period = StringField('What date will this user be unbanned? ')
	submit = SubmitField('Ban')