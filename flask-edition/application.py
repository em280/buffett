from flask import Flask, render_template, request, jsonify, redirect, url_for

from stocky import * # Import all the functions
from models import * # Import all the models

import csv
import os

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

import json
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
import chartjs
import numpy as np

# The name of this application is app
app = Flask(__name__)

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
def index():
    """ The homepage of the application. """
    # Obtain data about current user // this will be implemented properly in sprint 2
    user = User.query.first()
    amt = usd(user.cash)
    symbol = "MSFT"
    current_price = usd(get_current_share_quote(symbol)['latestPrice']) # This line needs to be corrected
    temp = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=MSFT&apikey=demo&datatype=csv"
    
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
    Functionality for the search function.
    """
    # symbol = request.args.get("name")
    # current_price = get_current_share_quote(symbol)['latestPrice']
  
    # # chart = chartjs.chart(symbol, "Line", 640, 480)
    # chart = chartjs.chart(symbol, "Line", 900, 380)
    # data = get_month_chart(symbol, 3)
    # labels = []
    # ds = []
    # for rows in data:
    #     labels.append(rows['date'])
    #     ds.append(rows['close'])
    
    # chart.set_labels(labels)
    # chart.add_dataset(ds)
    # chart.set_params(fillColor = "rgba(220,220,220,0.5)", strokeColor = "rgba(220,220,220,0.8)", highlightFill = "rgba(220,220,220,0.75)", highlightStroke = "rgba(220,220,220,1)",)
    # company_chart = chart.make_chart_full_html()
    # # return render_template("search.html", company_chart=company_chart, current_price=current_price)
    # return render_template("search.html", symbol=symbol, current_price=current_price)
    # # return render_template("index.html", company_chart=company_chart, current_price=current_price)

    # The below code makes use of alphavantage api for testing purposes
    users = User.query.all()
    user = User.query.first()
    amt = usd(user.cash)
    symbol = request.args.get("name")
    
    symbol = symbol.upper()
    akey = "XKRYNVS020SDNVD8"
    temp = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={akey}&datatype=csv"
    current_price = get_current_share_quote(symbol)['latestPrice'] # This line needs to be corrected

    data = {}
    data["symbol"] = symbol.upper()
    data["amount"] = amt
    data["current_price"] = current_price
    

    return render_template('index.html',
                           temp=temp, data=data, users=users, current_price=f"${current_price:,.2f}", user=user)



@app.route("/dashboard")
def dashboard():
    """
    Functionality for the user dashboard/portfolio function.
    """
    # Just show the index page for now.
    return redirect(url_for("index"))
    

@app.route("/buy", methods=["GET", "POST"])
def buy():
    """ Functionality for the user buy function. """
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
        noOfShares = int(request.form["shares"]) * -1

        # Query database
        userid = 1
        user = User.query.get(userid)

        # contact API
        company_info = get_company_info(symbol)
        company_name = company_info["companyName"]
        current_price = get_current_share_quote(symbol)['latestPrice']

        stocks = Portfolio.query.all()
        ptf = Portfolio.query.filter_by(usr_id=int(1)).all()
        for stock in ptf:
            if stock.symbol == symbol:
                # some arithmetic
                total_cost = (float(noOfShares) * current_price)

                # update cash for user in the database
                user.cash = usercash + total_cost
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

        return render_template("index.html", data=data, temp=temp, message="You have sold one of your shares.")

    # Just show the index page for now.
    return redirect(url_for("index"))

@app.route("/history")
def history():
    """ Functionality for the history function. """
    data = {}
    
    
    history = History.query.all()
    if history is None:
        # Just show the index page for now.
        return redirect(url_for("index"))

    info = []

    for item in history:
        company_info = get_company_info(item.symbol)
        company_name = company_info["companyName"]
        current_price = get_current_share_quote(item.symbol)['latestPrice']

        data["symbol"] = item.symbol.upper()
        info.append(item.symbol)
        
        info.append(company_name)
        info.append(item.quantity)
        info.append(usd(current_price))
        info.append(item.transaction_date)

        data["company_name"] = company_name
        data["current_price"] = usd(current_price)

    return render_template("index.html", data=data, history=history, temp=temp, message="This is a record of all your transactions.")

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

@app.route("/initdb")
def main():
    # Create a database with tables
    # This method will only be called at the beginning of the program
    # to initiate the database and never again.
    db.create_all()
    return "db initialized"

def usd(value):
    """ Format an amount in usd currency. """
    return f"${value:,.2f}"


if __name__ == "__main__":
    """
    This is the main entry of the program.

    Debug has been set to true for development purposes.
    This program can now be executed by typing "python application.py" or "python3 application.py"
    provided you are in the current directory of application.py
    """
    with app.app_context():
        main()
    app.run(debug=True)
