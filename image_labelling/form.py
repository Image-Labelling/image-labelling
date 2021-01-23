from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, BooleanField, SelectField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField("Keep me logged in")
    display = ['email', 'password']


class UserForm(FlaskForm):
    """Form for creating users."""
    email = StringField(label='Email', validators=[DataRequired()])
    username = StringField(label='Username', validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired()])

    display = ['email', 'username', 'password']


class LabelForm(FlaskForm):
    """Form for creating new labels."""
    parent = StringField(label="Parent label")
    name = StringField(label="Label", validators=[DataRequired()])
    language = SelectField(label="Language", choices=["English", "Polish"])

    display = ['parent', 'name', 'language']
