from flask import Flask, render_template, request, jsonify

from stocky import get_month_chart
from stocky import get_current_share_quote
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



@app.route("/")
@app.route("/index")
def index():
    """
    @author EM
    The homepage of the application.
    """
    # List all users
    users = User.query.all()
    user = User.query.first()
    amt = user.cash
    # tesla = jsonify(get_month_chart("TSLA", 1))
    symbol = "MSFT"
    current_price = get_current_share_quote(symbol)['latestPrice'] # This line needs to be corrected
    temp = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=MSFT&apikey=demo&datatype=csv"

    return render_template('index.html',
                           temp=temp, symbol=symbol, users=users, current_price=f"${current_price:,.2f}", amt=f"${amt:,.2f}")


@app.route("/search", methods=["GET"])
def search():
    """
    @author SH
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
    symbol = request.args.get("name")
    current_price = get_current_share_quote(symbol)['latestPrice'] # This line needs to be corrected
    symbol = symbol.upper()
    akey = "XKRYNVS020SDNVD8"
    temp = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={akey}&datatype=csv"
    data = [symbol]

    return render_template('index.html',
                           temp=temp, data=data, symbol=symbol, users=users, current_price=f"£{current_price:,.2f}", user=user)



@app.route("/dashboard")
def dashboard():
    """
    @author EM
    Functionality for the user dashboard/portfolio function.
    """
    # List all stocks owned by the user
    user_stocks = Portfolio.query.all()
    return render_template("index.html", user_stocks=user_stocks)
    

@app.route("/buy", methods=["GET"])
def buy():
    """
    @author EM
    Functionality for the user buy function.
    """
    symbol = request.args.get("symbol")
    # symbol = "MSFT"
    current_price = get_current_share_quote(symbol)['latestPrice']
    noOfShares = 1
    # userid of 3 is used as an example
    userid = 1
    Portfolio().add_portfolio_stock(userid, symbol)
    # update cash/value balance of the user
    user = User.query.get(userid)
    user.cash = user.cash - (current_price * noOfShares)
    db.session.commit()
    # User().update_user(userid, user.cash)
    # update portfolio display instead
    name = ""
    data = []
    data.append(symbol)
    data.append(name)
    data.append(shares)
    data.append(current_price)
    data.append(user.cash)
    # return render_template("index.html", data=data, message=f"You have bought some shares worth £{current_price:,.2f}.")
    return render_template('index.html',
                           temp=temp, data=data, symbol=symbol, users=users, current_price=f"${current_price:,.2f}", amt=f"${amt:,.2f}", message=f"You have bought some shares worth £{current_price:,.2f}.")


@app.route("/sell")
def sell():
    """
    @author 
    Functionality for the user sell function.
    """
    # Enable selling of shares
    # Remove stock from user's portfolio
    # You can use DELETE or log the sale as a negative quantity
    # Update cash/value of user [the stock is sold at its current price]
    # return success or failure message

    # Get stock information
    stock_symbol = "MSFT"
    remove_portfolio_stock(stock_symbol)
    # update user's cash balance
    userid = 3
    User().update_user(userid, 100)
    return render_template("index.html", message="You have sold one of your shares.")

@app.route("/history")
def history():
    """
    @author EM
    Functionality for the history function.
    """
    return render_template("index.html", message="This is a record of all your transactions.")

@app.route("/summary")
def summary():
    """
    @author EM
    Functionality for the summary function.
    """
    return render_template("index.html", message="This is a summary of your profile.")

@app.route("/register")
def register():
    """
    @author EM
    Functionality for the user register function.
    """
    # Register a user
    user = User().add_user("bob") # bob alan alice dw er ty
    return "A user has been registered."

@app.route("/unregister")
def unregister():
    """
    @author EM
    Functionality for the user unregister function.
    """
    # Unregister a user based on their id
    User().remove_user(2)
    return "A user has been unregistered." # Update this function for when user was not removed

@app.route("/test")
def test():
    temp = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=MSFT&apikey=demo&datatype=csv"
    # temp = 9999
    return render_template("test.html", temp=temp)

@app.route("/initdb")
def main():
    # Create a database with tables
    # This method will only be called at the beginning of the program
    # to initiate the database and never again.
    db.create_all()
    return "db initialized"


if __name__ == "__main__":
    """
    @author EM
    This is the main entry of the program.

    Debug has been set to true for development purposes.
    This program can now be executed by typing "python application.py" or "python3 application.py"
    provided you are in the current directory of application.py
    """
    with app.app_context():
        main()
    app.run(debug=True)
