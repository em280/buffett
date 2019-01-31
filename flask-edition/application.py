from flask import Flask, render_template, request, jsonify

from stocky import get_month_chart
from stocky import get_current_share_quote

import json
import plotly
import plotly.plotly as py
import plotly.graph_objs as go

import numpy as np

# The name of this application is app
app = Flask(__name__)


@app.route("/")
def index():
    """
    @author EM
    The homepage of the application.
    """
    # temp = get_month_chart("TSLA", 1)
    # return render_template("index.html", temp=temp)
    temp = jsonify(get_month_chart("TSLA", 1))

    return render_template('index.html',
                           temp=temp)


@app.route("/search", methods=["GET"])
def search():
    """
    @author EM
    Functionality for the search function.
    """
    symbol = request.args.get("name")
    current_price = get_current_share_quote(symbol)['latestPrice']

    return render_template("search.html", symbol=symbol, current_price=current_price)


@app.route("/live")
def show():
    """
    @author EM
    Functionality for the search function.
    """
    return json.dumps(get_month_chart("TSLA", 1))

if __name__ == "__main__":
    """
    @author EM
    This is the main entry of the program.

    Debug has been set to true for development purposes.
    This program can now be executed by typing "python application.py" or "python3 application.py"
    provided you are in the current directory of application.py
    """
    app.run(debug=True)
