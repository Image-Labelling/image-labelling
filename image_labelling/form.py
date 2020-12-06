from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms.fields import StringField, PasswordField


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    display = ['email', 'password']


class UserForm(FlaskForm):
    """Form for creating users."""
    email = StringField(label='Email', validators=[DataRequired()])
    username = StringField(label='Username', validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired()])

    display = ['email', 'username', 'password']
