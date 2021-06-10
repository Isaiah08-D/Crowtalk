from wtforms import StringField, SubmitField, PasswordField
import os
from wtforms.validators import Required
from flask_wtf import FlaskForm

class LoginForm(FlaskForm):
	username = StringField('Username: ', validators=[Required()])
	password = PasswordField('Password: ', validators=[Required()])
	submit = SubmitField('Login')
