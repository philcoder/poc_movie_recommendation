from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, validators
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    userLogin = StringField('Username', [validators.DataRequired(), validators.Length(min=2, max=15, message='Field must be 2 and 15 characters long')])
    userPassword = PasswordField('Password', [validators.DataRequired(), validators.Length(min=2, max=10)])
    submitLogin = SubmitField('Sign In')

class RegisterLoginForm(FlaskForm):
    registerNameUser = StringField('Full name', [validators.DataRequired(), validators.Length(min=2, max=15, message='Field must be 2 and 15 characters long')])
    registerUserLogin = StringField('Username', [validators.DataRequired(), validators.Length(min=2, max=15, message='Field must be 2 and 15 characters long')])
    registerUserPassword = PasswordField('Password', [validators.DataRequired(), validators.Length(min=2, max=10)])
    submitRegister = SubmitField('Register')