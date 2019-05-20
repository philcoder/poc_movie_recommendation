from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, validators
from wtforms.validators import DataRequired, ValidationError

from app.models import User

class LoginForm(FlaskForm):
    userName = StringField('Username', [validators.DataRequired(), validators.Length(min=2, max=15, message='Field must be 2 and 15 characters long')])
    userPassword = PasswordField('Password', [validators.DataRequired(), validators.Length(min=2, max=10)])
    submitLogin = SubmitField('Sign In')

class RegisterLoginForm(FlaskForm):
    registerName = StringField('Full name', [validators.DataRequired(), validators.Length(min=2, max=15, message='Field must be 2 and 15 characters long')])
    registerUserName = StringField('Username', [validators.DataRequired(), validators.Length(min=2, max=15, message='Field must be 2 and 15 characters long')])
    registerUserPassword = PasswordField('Password', [validators.DataRequired(), validators.Length(min=2, max=10)])
    submitRegister = SubmitField('Register')

    def validate_registerUserName(self, registerUserName):
        user = User.query.filter_by(username=registerUserName.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')