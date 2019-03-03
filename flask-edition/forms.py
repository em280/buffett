"""
@author: EM

This is a helper file for forms and form validation.
"""

from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length

class SignupForm(Form):
    user_name = StringField("Username", validators=[DataRequired("Please enter your username.")])
    password = PasswordField("Password", validators=[DataRequired("Please provide a password."), Length(min=8, message="Passwords must be 8 characters or more.")])
    submit = SubmitField("Sign up")

class LoginForm(Form):
    user_name = StringField("Username", validators=[DataRequired("Please enter your username.")])
    password = PasswordField("Password", validators=[DataRequired("Please provide a password.")])
    submit = SubmitField("Sign in")

class BuyForm(Form):
    symbol = StringField("Symbol", validators=[DataRequired("Please enter a valid symbol.")])
    shares = IntegerField("Shares", validators=[DataRequired("Please provide the number of shares to buy."), Length(max=2, message="Number of shares must be 2 digits or less.")])
    
