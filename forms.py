from wtforms import Form
from wtforms import StringField, SubmitField, PasswordField
import os
from wtforms.validators import Required

class LoginForm(Form):
	email = StringField('Email: ', validators=[Required()])
	password = PasswordField('Password: ', validators=[Required()])
	submit = SubmitField('Login')