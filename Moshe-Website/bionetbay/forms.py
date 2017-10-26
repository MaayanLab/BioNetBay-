from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email

class UsernamePasswordForm(Form):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

class RegistrationForm(Form):
    username = StringField('Username')
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    password = PasswordField('New Password', validators=[DataRequired()])
    confirm = PasswordField('Repeat Password')
    # accept_tos = BooleanField('I accept the Terms of Service and Privacy Notice (updated Jan 22, 2015)', validators= [DataRequired()])
