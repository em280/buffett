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
    # tt = json.JSONDecoder().decode(get_month_chart("TSLA", 1))

    # xScale = tt["close"]
    # yScale = tt["date"]

    # # Create a trace
    # trace = go.Scatter(
    #     x=xScale,
    #     y=yScale
    # )

    # data = [trace]
    # graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

    # t = json.dumps(get_month_chart("TSLA", 1),
    #                cls=plotly.utils.PlotlyJSONEncoder)
    # return render_template("live.html", t=t, graphJSON=graphJSON)
