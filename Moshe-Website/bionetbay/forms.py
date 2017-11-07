from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, TextField
from wtforms.validators import DataRequired, Email, EqualTo

class UsernamePasswordForm(Form):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

class RegistrationForm(Form):
    username = StringField('Username')
    email = StringField('Email Address', validators=[DataRequired(), Email("This field requires a valid email address")])
    password = PasswordField('New Password', validators=[DataRequired(), EqualTo('confirm', message='Passwords must match!')])
    confirm = PasswordField('Repeat Password')
    # accept_tos = BooleanField('I accept the Terms of Service and Privacy Notice (updated Jan 22, 2015)', validators= [DataRequired()])

class EmailForm(Form):
    email = StringField('Email', validators=[DataRequired(), Email()])

class PasswordForm(Form):
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('confirm', message='Passwords must match!')])
    confirm = PasswordField('Repeat Password')

class ResourceForm(Form):
    name = StringField('Name', validators=[DataRequired()])
    description = TextField('Description')
    link = StringField('Link')

class DatasetForm(Form):
    name = StringField('Name', validators=[DataRequired()])
    description = TextField('Description')
    measurement = StringField('Measurement')
    association = StringField('Association')
    category = StringField('Category', validators=[DataRequired()])
    sub_category = StringField('SubCategory', validators=[DataRequired()])
    resource = StringField('Resource', validators=[DataRequired()])
    number_of_genes = StringField('Number_Of_Genes')
    number_of_samples= StringField('Number_Of_Samples')
    number_of_associations = StringField('Number_Of_Associations')

class FileForm(Form):
    name = StringField('Name', validators=[DataRequired()])
    dataset = StringField('DataSet')
    file_type = StringField('FileType')
    link = StringField('Link', validators=[DataRequired()])
