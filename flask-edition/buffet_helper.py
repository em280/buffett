"""
@author: EM
"""

from flask import redirect
from functools import wraps

import datetime as dt
import pandas as pd
import pandas_datareader.data as web
import pandas_datareader as pdr
from datetime import datetime

def usd(value):
    """
    @author: EM
    Format an amount in usd currency.
    """
    return f"${value:,.2f}"

def login_require(f):
    @wraps(f)
    def decorated_function(*args,**kwargs):
        """
        @author: SA
        Login is required to progress to next page.
        """
        return redirect("/login")
    return decorated_function

def plotter(symbol):
    start = dt.datetime(2018, 1, 1)

    df = web.DataReader(symbol, "iex", start)
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

    return data
