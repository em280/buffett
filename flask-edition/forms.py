"""
@author: EM
"""

from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length

class SignupForm(Form):
    user_name = StringField("Username", validators=[DataRequired("Please enter your username.")])
    password = PasswordField("Password", validators=[DataRequired("Please provide a password."), Length(min=8, message="Passwords must be 8 characters or more.")])
    submit = SubmitField("Sign up")

class LoginForm(Form):
    user_name = StringField("Username", validators=[DataRequired("Please enter your username.")])
    password = PasswordField("Password", validators=[DataRequired("Please provide a password.")])
    submit = SubmitField("Sign in")
    