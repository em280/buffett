from flask import Flask, flash, render_template, request, jsonify, redirect, url_for, session, send_file

from stocky import * # Import all the functions
from models import * # Import all the models
from buffet_helper import * # Import all the helper functions
from forms import SignupForm, LoginForm, BuyForm, SellForm, SearchForm # Import for form functionality
from passlib.hash import sha256_crypt

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

########
import datetime as dt
# import matplotlib.pyplot as plt
# from matplotlib import style
import pandas as pd
import pandas_datareader.data as web

import pandas_datareader as pdr
from datetime import datetime
######

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


#################### The rest of the application ####################
@app.route("/")
@app.route("/index")
#@loginRequire
def index():
    """
    @author: SH
    The homepage of the application.
    """

    searchForm = SearchForm()
    # Obtain data about current user // this will be implemented properly in sprint 2
    user = User.query.first()
    amt = usd(user.cash)
    symbol = "MSFT"
    current_price = usd(get_current_share_quote(symbol)['latestPrice'])

    # obtaining graph information
    graphdata = plotter(symbol)

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
            # info["company_name"] = get_company_info(stock.symbol)["companyName"]
            stock_info.append(info)
            index = index + 1


    data["symbol"] = symbol.upper()
    data["amount"] = amt
    data["current_price"] = current_price
    data["stock_info"] = stock_info

    stocks = Portfolio.query.all()

    company_in = get_company_info(symbol)

    data['exchange'] = company_in['exchange']
    data['industry'] = company_in['industry']
    data['description'] = company_in['description']
    data['sector'] = company_in['sector']

    company_info = get_company_info(symbol)

    quotes = search_autocomplete()

    return render_template('index.html', data=data, stocks=stocks, searchForm=searchForm, graphdata=graphdata, quotes=quotes)


@app.route("/search", methods=["GET", "POST"])
def search():
    """
    @author: SH
    Functionality for the search function.
    """

    searchForm = SearchForm()

    symbol = None
    if searchForm.validate_on_submit():
        symbol = searchForm.search.data.upper()

    users = User.query.all()
    user = User.query.first()
    amt = usd(user.cash)

    if symbol is None:
        flash('Please make sure you have provided the right symbol')
        return redirect(url_for("index"))

    # Edit this accordingly for symbols longer than 4 characters
    if len(symbol) > 4:
        flash('You were successfully logged in')
        return redirect(url_for("index"))

    # obtaining graph information
    graphdata = plotter(symbol)

    current_price = get_current_share_quote(symbol)['latestPrice'] # This line needs to be corrected

    data = {}
    data["symbol"] = symbol.upper()
    data["amount"] = amt
    data["current_price"] = current_price

    company_in = get_company_info(symbol)

    data['exchange'] = company_in['exchange']
    data['industry'] = company_in['industry']
    data['description'] = company_in['description']
    data['sector'] = company_in['sector']

    return render_template('index.html', searchForm=searchForm, data=data, users=users, user=user, graphdata=graphdata)


@app.route("/dashboard")
def dashboard():
    """
    @author: EM
    Functionality for the user dashboard/portfolio function.
    """

    searchForm = SearchForm()

    info = {}
    stocks = Portfolio.query.all()

    user = User.query.first()
    amt = usd(user.cash)
    info["user_cash"] = amt
    grand_total = user.cash

    for item in stocks:
        company_info = get_company_info(item.symbol)
        # company_name = company_info["companyName"]
        current_price = get_current_share_quote(item.symbol)['latestPrice']

        # record the name and current price of this stock
        # info[item.symbol] = company_name
        info[item.symbol+"price"] = usd(current_price)
        info[item.symbol+"total"] = current_price * item.quantity

        if len(stocks) == len(stocks):
            for k, value in info.items():
                if k == item.symbol+"total":
                    grand_total = float(grand_total) + float(value)
            info["g_total"] = usd(grand_total)
        info[item.symbol+"total"] = usd(current_price * item.quantity)

    return render_template("portfolio.html", stocks=stocks, info=info, searchForm=searchForm)


@app.route("/buy", methods=["GET", "POST"])
def buy():
    """
    @author: EM
    Functionality for the user buy function.
    """
    buyForm = BuyForm()
    searchForm = SearchForm()

    if buyForm.validate_on_submit():


    # if request.method == "POST":
        # Get form information
        # symbol = request.form["symbol"]
        symbol = buyForm.symbol.data.upper()
        noOfShares = int(buyForm.shares.data)
        # noOfShares = int(request.form["shares"])

        # contact API
        company_info = get_company_info(symbol)
        # company_name = company_info["companyName"]
        current_price = get_current_share_quote(symbol)['latestPrice']

        # graph stuff
        temp = 'tmp.csv'

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
        # data["company_name"] = company_name
        data["noOfShares"] = noOfShares
        data["current_price"] = usd(current_price)
        data["amount"] = usd(user.cash)

        stocks = Portfolio.query.all()
        ptf = Portfolio.query.filter_by(usr_id=int(1)).all()
        if ptf is not None:
            for stock in ptf:
                grand_total = user.cash + (stock.quantity * get_current_share_quote(stock.symbol)['latestPrice'])
                data["grand_total"] = usd(grand_total)

        flash(f"You have bought some shares worth {usd(current_price)}.")

        return render_template('index.html',
                        data=data, searchForm=searchForm, temp=temp, stocks=stocks, message=f"You have bought some shares worth {usd(current_price)}.")

    # the code below is executed if the request method
    # was GET or there was some sort of error
    return render_template("buy.html", buyForm=buyForm, searchForm=searchForm)

    # Just show the index page for now.
    # return redirect(url_for("index"))


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

    sellForm = SellForm()
    searchForm = SearchForm()

    if sellForm.validate_on_submit():
        # Get form information
        symbol = sellForm.symbol.data.upper()
        noOfShares = int(sellForm.shares.data)

        # contact API
        company_info = get_company_info(symbol)
        # company_name = company_info["companyName"]
        current_price = get_current_share_quote(symbol)['latestPrice']

        # graph stuff
        temp = 'tmp.csv'

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
        else:
            # no such stock exist
            pass

        # update history table
        History().add_hist(userid, symbol.upper(), -noOfShares)

        db.session.commit()

        data = {}
        data["symbol"] = symbol.upper()
        # data["company_name"] = company_name
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
                        data=data, sellForm=sellForm, searchForm=searchForm, temp=temp, stocks=stocks, message=f"You have sold some shares worth {usd(current_price)}.")

    return render_template("sell.html", sellForm=sellForm, searchForm=searchForm)

@app.route("/history")
def history():
    """
    @author: EM
    Functionality for the history function.
    """
    searchForm = SearchForm()
    data = {}
    info = {}

    history = History.query.all()
    if history is None:
        # Just show the index page for now.
        return redirect(url_for("index"))

    for item in history:
        company_info = get_company_info(item.symbol)
        # company_name = company_info["companyName"]
        current_price = get_current_share_quote(item.symbol)['latestPrice']

        # record the name and current price of this stock
        # info[item.symbol] = company_name
        info[item.symbol+"price"] = usd(current_price)

    return render_template("history.html", history=history, searchForm=searchForm, info=info, message="This is a record of all your transactions.")

@app.route("/summary")
def summary():
    """
    Functionality for the summary function.
    """
    searchForm = SearchForm()
    # graph stuff
    symbol = "MSFT"
    graphdata = plotter(symbol)
    # Showing open positions for the loggedin user
    stocks = Portfolio.query.all()
    data = {}
    for stock in stocks:
        current_stock = get_company_info(stock.symbol)

        postion = {
            # "company_name": current_stock["companyName"],
            "current_price": get_current_share_quote(stock.symbol)["latestPrice"],
            # "symbol": current_stock["symbol"]
        }

    return render_template("index.html", graphdata=graphdata, searchForm=searchForm, data=stocks, message="This is a summary of your profile.")

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

@app.route("/plot")
def plotter2():
    """
    @author: EM
    This function does not contribute to the application and therefore should be ignored.
    It it solely for testing purposes.
    """
    start = dt.datetime(2018, 1, 1)

    df = web.DataReader("TSLA", "iex", start)
    df.to_csv("iex.csv")
    # df = pd.read_csv("graph.csv", parse_dates=True, index_col=0)
    df = pd.read_csv("iex.csv")

    df = df.set_index(df.date)

    data = {}
    ldate = []
    lhigh = []
    llow = []
    lopen = []
    lclose = []

    lt = df.tail(30).index.values

    for i in lt:
        d = datetime.strptime(i, "%Y-%m-%d")
        d = datetime.strftime(d, "%Y-%m-%d")
        ldate.append(d)

    for k in range(30):
        lhigh.append(df.tail(30)["high"][k])
        llow.append(df.tail(30)["low"][k])
        lopen.append(df.tail(30)["open"][k])
        lclose.append(df.tail(30)["close"][k])

    data["date"] = ldate
    data["high"] = lhigh
    data["low"] = llow
    data["open"] = lopen
    data["close"] = lclose

    return render_template("test2.html", data=data)

@app.route("/test")
def test():
    """
    @author: EM
    This function does not contribute to the application and therefore should be ignored.
    It it solely for testing purposes.
    """
    # temp = Portfolio.query.all()
    temp = User.query.all()
    # return render_template("test.html", temp=temp)

    start = dt.datetime(2000, 1, 1)
    end = dt.datetime(2016, 12, 31)
    df = web.DataReader("TSLA", "yahoo", start, end)
    df.to_csv("tsla.csv")
    df = pd.read_csv("tsla.csv", parse_dates=True, index_col=0)
    df = pd.read_csv("tsla.csv")
    # # data = df.head(30).to_dict()
    # print(df.tail(30))
    # print(df.tail(30)["Date"])

    # df.Date = pd.to_datetime(df.Date, format="%Y-%m-%d")
    df = df.set_index(df.Date)
    # print(df.tail(30))


    data = {}
    l = []
    lhigh = []
    llow = []
    lopen = []
    lclose = []
    # data["date"] = df.tail(30)["Date"]
    lt = df.tail(30).index.values
    for i in lt:
        # l.append(datetime.strptime(i, "%Y-%m-%d"))
        d = datetime.strptime(i, "%Y-%m-%d")
        d = datetime.strftime(d, "%Y-%m-%d")
        # l.append(d.date())
        l.append(d)
        # print(i, "printer", type(i))
    for k in range(30):
        # print(l[k].date(), type(l[k].date()))
        lhigh.append(df.tail(30)["High"][k])
        llow.append(df.tail(30)["Low"][k])
        lopen.append(df.tail(30)["Open"][k])
        lclose.append(df.tail(30)["Close"][k])
    # data["date"] = df.tail(30).index.values
    data["date"] = l
    # data["date"] = pd.to_datetime(df.tail(30).index.values, format="%Y-%m-%d")
    # data["close"] = df.tail(30)["Close"].values
    data["high"] = lhigh
    data["low"] = llow
    data["open"] = lopen
    data["close"] = lclose

    # return render_template("test.html", data=data)
    return render_template("test2.html", graphdata=data)

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
    # return render_template("test.html", temp=temp, msg="db initialized")
    return "db initialized"


@app.route("/signup", methods=["GET", "POST"])
def signup():
    """
    @author: EM
    """
    form = SignupForm()

    if form.validate_on_submit():
        # Adding a new user to the database
        new_user = User(username=form.user_name.data, password=form.password.data)
        db.session.add(new_user)
        db.session.commit()

        session["user_name"] = new_user.username
        flash('You were successfully logged in')
        return redirect(url_for("index"))
    # Else the form was submitted via get
    return render_template("signup.html", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    """
    @author: EM
    @author: SA
    """
    form = LoginForm()

    if form.validate_on_submit():
        username = form.user_name.data
        password = form.password.data

        user = User.query.filter_by(username=username).first()
        if user is not None:
        # if user is not None and user.check_password(password):
            session["user_name"] = form.user_name.data
            flash('You were successfully logged in')
            return redirect(url_for("index"))
        else:
            redirect(url_for("login"))

    # rendering login page
    return render_template("login.html", form=form)

@app.route("/logout")
def logout():
    """
    @author: EM
    """
    session.pop("user_name", None)
    return redirect(url_for("login"))

@app.route("/leaderboard")
def leaderboard():
    '''
    @author: SH
    '''
    pass

@app.route("/home")
def home():
    '''
    @author: SA
    '''
    return render_template("home.html")

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
