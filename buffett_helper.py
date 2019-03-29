"""
@author: EM

This is a helper file for the application,
it consists of functional utilities needed by the application.
"""

from flask import redirect, url_for, request, session
from functools import wraps

import datetime as dt
import pandas as pd
import pandas_datareader.data as web
import pandas_datareader as pdr
from datetime import datetime, timedelta
import time

from stocky import get_company_name, get_month_chart


def usd(value):
    """
    @author: EM
    Format an amount in usd currency.
    """
    return f"${value:,.2f}"


def prepare_phone_number(value):
    """
    @author: EM
    Format a phone number in UK format.
    """
    value = value.replace(" ", "")
    return f"+44{value[-10:]}"


def login_required(f):
    """
    @author: EM

    Login is required for any route that is visited by the user.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # return redirect(url_for("login"))
        # if session["username"] is None:
        if "username" not in session:
            # return redirect(url_for('login', next=request.url))
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function


def plotter(symbol):
    """
    @author: EM
    Prepare data to be used for plotting to the webpage depending on the symbol supplied.

    """
    # The start date of the data to be fetched from the API
    # The end date is defaulted to today's date
    start = dt.datetime(2016, 1, 1)

    # Currently the data manipulated goes back 3 months from the current date
    n_data = 60  # for 60 days / or 3 months
    # n_data = 30 # for 30 days / or 1 month

    # df = web.DataReader(symbol, "iex", start)
    # df.to_csv("iex.csv")
    df = pd.read_csv("iex.csv")

    df = df.set_index(df.date)

    data = {}
    ldate = []
    lhigh = []
    llow = []
    lopen = []
    lclose = []

    lt = df.tail(n_data).index.values

    for i in lt:
        d = datetime.strptime(i, "%Y-%m-%d")
        d = datetime.strftime(d, "%Y-%m-%d")
        ldate.append(d)

    for k in range(n_data):
        lhigh.append(df.tail(n_data)["high"][k])
        llow.append(df.tail(n_data)["low"][k])
        lopen.append(df.tail(n_data)["open"][k])
        lclose.append(df.tail(n_data)["close"][k])

    data["date"] = ldate
    data["high"] = lhigh
    data["low"] = llow
    data["open"] = lopen
    data["close"] = lclose

    return data


def search_autocomplete():
    """
    @author: EM
    Functionality to return all the symbols that are supported by IEX API.
    """
    symbols = web.get_iex_symbols().symbol.values
    names = web.get_iex_symbols().name.values

    data = {}
    data["symbols"] = symbols.tolist()
    data["names"] = names.tolist()

    values = []

    for q in range(len(symbols)):
        values.append(data["symbols"][q] + " " + data["names"][q])
    return values


def prepare_leaderboard(symbol=None):
    """
    @author: EM
    Functionality to do some arithmetic for the leaderboard display
    """
    data = {}
    if symbol is not None:
        # Edit this line for when the market is closed
        df = web.DataReader(symbol, "iex", dt.date(2019, 3, 11))
        # df = web.DataReader(symbol, "iex", dt.date.today())
        # df = df.head(1)
        open_price = df["open"].values
        close_price = df["close"].values
        data["open_price"] = open_price
        data["close_price"] = close_price

        return data


def get_gainers_losers(symbols, tag):
    """
    @author: EM
    """
    data = []

    for q in symbols:
        d = {}
        d["symbol"] = q
        d["companyName"] = get_company_name(q)
        d["lastPrice"] = get_month_chart(q, 3)[-1]["close"]
        d["change"] = get_month_chart(q, 3)[-1]["change"]
        d["changePercent"] = get_month_chart(q, 3)[-1]["changePercent"]

        if tag == "g":
            if d["change"] > 0:
                data.append(d)
        if tag == "l":
            if d["change"] < 0:
                data.append(d)

    return data


def quote_validate(symbol):
    """
    @author: EM
    Look up and confirm quote for symbol.

    This function is undergoing serious changes and should not be relied on at the moment.
    """

    # Reject symbol if it starts with caret
    if symbol.startswith("^"):
        return None

    # Reject symbol if it contains comma
    if "," in symbol:
        return None

    # Query IEX for quote
    symbols = web.get_iex_symbols().symbol.values.tolist()
    if symbol in symbols:
        return symbol.upper()
    else:
        return None

def prepare_authcode(numcode, numphone):
	"""
	Authentication code for registering a user.
	"""
	# Initialise values of the auth code and phone number to send to
	auth_code = numcode
	to = numphone

def get_auth_code(username):
    """
    Username represents the username of the currently logged in user.
    """
    if username in session:
        return session["a_code"]
    else:
        return None

def prepare_export(content):
    pass

# enter_auth_code(username)

# get_auth_code(usrname)

# auth_user(username)
# then someone can manage the front end to check whether the user has been autherised
# if yes the signup goes through
