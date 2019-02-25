from flask import Flask, render_template, request, jsonify, redirect, url_for, session

from stocky import * # Import all the functions
from models import * # Import all the models
from buffet_helper import * # Import all the helper functions
from forms import SignupForm, LoginForm # Import for form functionality

import csv
import os

# importing tools for sessions
from flask_session import Session
from tempfile import mkdtemp
# end import for sessions

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

import json
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
# import chartjs
import numpy as np

# The name of this application is app
app = Flask(__name__)

# Protecting the form against CSRF security exploit (this exploit is called Cross-Site Request Forgery)
app.secret_key = "development-key"

# begin configuration of application for sessions
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
# end configuration for sessions

# Relevant variables for database access, implementation and access
# The program shall make use of simple SQLLite for testing and development purposes
# PostgreSQL or MySQL shall be used for production
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database_test.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

# Globals
temp = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=MSFT&apikey=demo&datatype=csv"


@app.route("/")
@app.route("/index")
#@loginRequire
def index():
    """
    @author: SA - loginRequire implemented.
    @author: SH
    The homepage of the application.
    """
    # Obtain data about current user // this will be implemented properly in sprint 2
    user = User.query.first()
    amt = usd(user.cash)
    symbol = "MSFT"
    current_price = usd(get_current_share_quote(symbol)['latestPrice']) # This line needs to be corrected
    temp = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=MSFT&apikey=demo&datatype=csv"
    tmp = "https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=MSFT&interval=5min&apikey=demo"

    data = {}
    stock_info = []
    info = {}

    ptf = Portfolio.query.filter_by(usr_id=int(1)).all()
    if ptf is not None:
        index = 0
        for stock in ptf:
            total_share_price = stock.quantity * get_current_share_quote(stock.symbol)['latestPrice']
            grand_total = user.cash + total_share_price
            info["grand_total"] = usd(grand_total)
            info["total_share_price"] = usd(total_share_price)
            info["company_name"] = get_company_info(stock.symbol)["companyName"]
            stock_info.append(info)
            index = index + 1


    data["symbol"] = symbol.upper()
    data["amount"] = amt
    data["current_price"] = current_price
    data["stock_info"] = stock_info

    stocks = Portfolio.query.all()

    return render_template('index.html', temp=temp, data=data, stocks=stocks)


@app.route("/search", methods=["GET"])
def search():
    """
    @author: SH
    Functionality for the search function.
    """
    # The below code makes use of alphavantage api for testing purposes
    users = User.query.all()
    user = User.query.first()
    amt = usd(user.cash)
    symbol = request.args.get("name")


    symbol = symbol.upper()
    akey = "XKRYNVS020SDNVD8"

    f = open("users.csv")
    reader = csv.reader(f)
    for timestamp, close in reader:
        filetmp = {"timestamp": timestamp, "close": close}

    # file = open('tmp.csv','r')
    # temp = file
    current_price = get_current_share_quote(symbol)['latestPrice'] # This line needs to be corrected

    data = {}
    data["symbol"] = symbol.upper()
    data["amount"] = amt
    data["current_price"] = current_price

    return render_template('index.html',
                           temp=filetmp, data=data, users=users, user=user)

@app.route("/dashboard")
def dashboard():
    """
    @author: EM
    Functionality for the user dashboard/portfolio function.
    """
    # Just show the index page for now.
    # return redirect(url_for("index"))

    info = {}
    stocks = Portfolio.query.all()

    user = User.query.first()
    amt = usd(user.cash)
    info["user_cash"] = amt
    grand_total = user.cash

    for item in stocks:
        company_info = get_company_info(item.symbol)
        company_name = company_info["companyName"]
        current_price = get_current_share_quote(item.symbol)['latestPrice']

        # record the name and current price of this stock
        info[item.symbol] = company_name
        info[item.symbol+"price"] = usd(current_price)
        info[item.symbol+"total"] = current_price * item.quantity

        if len(stocks) == len(stocks):
            for k, value in info.items():
                if k == item.symbol+"total":
                    grand_total = float(grand_total) + float(value)
            info["g_total"] = usd(grand_total)
        info[item.symbol+"total"] = usd(current_price * item.quantity)

    return render_template("portfolio.html", stocks=stocks, info=info)


@app.route("/buy", methods=["GET", "POST"])
def buy():
    """
    @author: EM
    Functionality for the user buy function.
    """
    if request.method == "POST":
        # Get form information
        symbol = request.form["symbol"]
        noOfShares = int(request.form["shares"])

        # contact API
        company_info = get_company_info(symbol)
        company_name = company_info["companyName"]
        current_price = get_current_share_quote(symbol)['latestPrice']

        # some arithmetic
        total_cost = (float(noOfShares) * current_price)

        # Query database
        userid = 1
        user = User.query.get(userid)
        usercash = user.cash

        if usercash > total_cost:
            # update cash for user in the database
            user.cash = usercash - total_cost
            # update portfolio table
            Portfolio().add_portfolio_stock(userid, symbol.upper(), noOfShares)

            # update history table
            History().add_hist(userid, symbol.upper(), noOfShares)

            db.session.commit()

        data = {}
        data["symbol"] = symbol.upper()
        data["company_name"] = company_name
        data["noOfShares"] = noOfShares
        data["current_price"] = usd(current_price)
        data["amount"] = usd(user.cash)

        stocks = Portfolio.query.all()
        ptf = Portfolio.query.filter_by(usr_id=int(1)).all()
        if ptf is not None:
            for stock in ptf:
                grand_total = user.cash + (stock.quantity * get_current_share_quote(stock.symbol)['latestPrice'])
                data["grand_total"] = usd(grand_total)

        return render_template('index.html',
                        data=data, temp=temp, stocks=stocks, message=f"You have bought some shares worth {usd(current_price)}.")

    # the code below is executed if the request method
    # was GET or there was some sort of error

    # Just show the index page for now.
    return redirect(url_for("index"))


@app.route("/sell", methods=["GET", "POST"])
def sell():
    """
    @author: EM
    Functionality for the user sell function.
    """
    # Enable selling of shares
    # Remove stock from user's portfolio // or // add a new row with a negative value for the number of shares
    # You can use DELETE or log the sale as a negative quantity
    # Update cash/value of user [the stock is sold at its current price]
    # return success or failure message

    if request.method == "POST":
        # Get form information
        symbol = request.form["symbol"]
        noOfShares = int(request.form["shares"])

        # contact API
        company_info = get_company_info(symbol)
        company_name = company_info["companyName"]
        current_price = get_current_share_quote(symbol)['latestPrice']

        # some arithmetic
        total_cost = (float(noOfShares) * current_price)

        # Query database
        userid = 1
        user = User.query.get(userid)
        # Not necessary to check for users balance
        # update cash for user in the database
        user.cash = user.cash + total_cost

        # update portfolio table
        # if number of shares is 2 or more then update row else delete row
        portf = Portfolio.query.get(userid)
        if portf is not None:
            if portf.quantity >= 2:
                Portfolio.quantity = portf.quantity - noOfShares
                db.session.commit()
            else:
                db.session.delete(portf)
                db.session.commit()
            # Portfolio().add_portfolio_stock(userid, symbol.upper(), -noOfShares)
        else:
            # no such stock exist
            pass

        # update history table
        History().add_hist(userid, symbol.upper(), -noOfShares)

        db.session.commit()

        data = {}
        data["symbol"] = symbol.upper()
        data["company_name"] = company_name
        data["noOfShares"] = noOfShares
        data["current_price"] = usd(current_price)
        data["amount"] = usd(user.cash)

        stocks = Portfolio.query.all()
        ptf = Portfolio.query.filter_by(usr_id=int(1)).all()
        if ptf is not None:
            for stock in ptf:
                grand_total = user.cash + (stock.quantity * get_current_share_quote(stock.symbol)['latestPrice'])
                data["grand_total"] = usd(grand_total)

        return render_template('index.html',
                        data=data, temp=temp, stocks=stocks, message=f"You have sold some shares worth {usd(current_price)}.")


        # return render_template("index.html", data=data, temp=temp, message="You have sold one of your shares.")

    # Just show the index page for now.
    return redirect(url_for("index"))

@app.route("/history")
def history():
    """
    @author: EM
    Functionality for the history function.
    """
    data = {}
    info = {}

    history = History.query.all()
    if history is None:
        # Just show the index page for now.
        return redirect(url_for("index"))

    for item in history:
        company_info = get_company_info(item.symbol)
        company_name = company_info["companyName"]
        current_price = get_current_share_quote(item.symbol)['latestPrice']

        # record the name and current price of this stock
        info[item.symbol] = company_name
        info[item.symbol+"price"] = usd(current_price)

    return render_template("history.html", history=history, info=info, message="This is a record of all your transactions.")

@app.route("/summary")
def summary():
    """ Functionality for the summary function. """
    # Showing open positions for the loggedin user
    stocks = Portfolio.query.all()
    data = {}
    for stock in stocks:
        current_stock = get_company_info(stock.symbol)

        postion = {
            "company_name": current_stock["companyName"],
            "current_price": get_current_share_quote(stock.symbol)["latestPrice"],
            "symbol": current_stock["symbol"]
        }

    return render_template("index.html", temp=temp, data=stocks, message="This is a summary of your profile.")

@app.route("/register")
def register():
    """ Functionality for the user register function. """
    # Register some stub users
    f = open("users.csv")
    reader = csv.reader(f)
    for name, passcode in reader:
        user = User(username=name, password=passcode)
        db.session.add(user)
        print("A stub user has been added.")
    db.session.commit()

    # testing
    temp = User.query.all()
    return render_template("test.html", temp=temp)

@app.route("/unregister")
def unregister():
    """
    Functionality for the user unregister function.
    """
    # Unregister a user based on their id
    User().remove_user(2)
    return "A user has been unregistered." # Update this function for when user was not removed

@app.route("/test")
def test():
    # temp = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=MSFT&apikey=demo&datatype=csv"
    # temp = 9999
    temp = Portfolio.query.all()
    # temp = User.query.all()
    return render_template("test.html", temp=temp)
    # tmp = requests.get("https://api.iextrading.com/1.0/stock/MSFT/chart/1d/")
    # return render_template("tchart.html", tmp=tmp.json())

@app.route("/initdb")
def main():
    # Create a database with tables
    # This method will only be called at the beginning of the program
    # to initiate the database and never again.
    db.create_all()

    # Register some stub users
    f = open("users.csv")
    reader = csv.reader(f)
    for name, passcode in reader:
        user = User(username=name, password=passcode)
        db.session.add(user)
        print("A stub user has been added.")
    db.session.commit()
    # return "db initialized"
    # testing
    temp = User.query.all()
    return render_template("test.html", temp=temp, msg="db initialized")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    """
    @author: EM
    """
    form = SignupForm()

    if request.method == "POST":
        if form.validate() == False:
            return render_template("signup.html", form=form)
        else:
            # Adding a new user to the database
            new_user = User(username=form.user_name.data, password=form.password.data)
            db.session.add(new_user)
            db.session.commit()
            # User().add_user()

            session["user_name"] = new_user.user_name
            return redirect(url_for("index"))
    # Else the form was submitted via get
    return render_template("signup.html", form=form)

@app.route("/login")
def login():
    """
    @author: EM
    """
    form = LoginForm()

    if request.method == "POST":
        if form.validate() == False:
            return render_template("login.html", form=form)
        else:
            username = form.user_name.data
            password = form.password.data

            user = User.query.filter_by(username=username).first()
            if user is not None and user.check_password(password):
                session["user_name"] = form.user_name.data
                return redirect(url_for("index"))
            else:
                redirect(url_for("login"))

    elif request.method == "GET":
        # rendering login page
        return render_template("login.html", form=form)

@app.route("/logout")
def logout():
    """
    @author: EM
    """
    session.pop("user_name", None)
    return redirect(url_for("login"))


if __name__ == "__main__":
    """
    @author: EM
    This is the main entry of the program.

    Debug has been set to true for development purposes.
    This program can now be executed by typing "python application.py" or "python3 application.py"
    provided you are in the current directory of application.py
    """
    with app.app_context():
        main()  # Calling the main function to initialise the database
    app.run(debug=True)
