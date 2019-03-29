"""
@author: EM
@author: SA

This is a helper file for forms and form validation.
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, BooleanField, TextField
from wtforms.validators import DataRequired, Length, EqualTo

class PhoneForm(FlaskForm):
    country_code = IntegerField('Country Code', validators=[DataRequired()])
    number       = TextField('Number', validators=[DataRequired()])

class SignupForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired("Please enter your username."), Length(min=4, max=25)])
    password = PasswordField("Password", validators=[DataRequired("Please provide a password."), Length(min=8, message="Passwords must be 8 characters or more."), EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField("Confirm Password")
    phone_number = StringField("Phone Number", validators=[DataRequired("Please enter your phone number.")])
    accept_tac = BooleanField("I accept the Terms and conditions", validators=[DataRequired()])
    submit = SubmitField("Sign up")

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired("Please enter your username.")])
    password = PasswordField("Password", validators=[DataRequired("Please provide a password.")])
    submit = SubmitField("Sign in")

class BuyForm(FlaskForm):
    symbol = StringField("Symbol", validators=[DataRequired("Please enter a valid symbol.")])
    shares = IntegerField("Shares", validators=[DataRequired("Please provide a number greater than zero of shares to buy.")])
    submit = SubmitField("Buy")

class SellForm(FlaskForm):
    symbol = StringField("Symbol", validators=[DataRequired("Please enter a valid symbol.")])
    shares = IntegerField("Shares", validators=[DataRequired("Please provide a number greater than zero of shares to sell.")])
    submit = SubmitField("Sell")

class SearchForm(FlaskForm):
    search = StringField("Search", validators=[DataRequired("Please enter a valid symbol.")])

class UnregisterForm(FlaskForm):
    password = PasswordField("Password", validators=[DataRequired("Please provide a password."), Length(min=8, message="Passwords must be 8 characters or more."), EqualTo('confirm', message='Passwords must match')])    
    confirm = PasswordField("Confirm Password")
    submit = SubmitField("Unregister")