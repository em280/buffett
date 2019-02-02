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
def index():
    """
    @author EM
    The homepage of the application.
    """
    # List all users
    users = User.query.all()
    tesla = jsonify(get_month_chart("TSLA", 1))

    return render_template('index.html',
                           tesla=tesla, users=users)


@app.route("/search", methods=["GET"])
def search():
    """
    @author SH
    Functionality for the search function.
    """
    symbol = request.args.get("name")
    current_price = get_current_share_quote(symbol)['latestPrice']
  
    chart = chartjs.chart(symbol, "Line", 640, 480)
    data = get_month_chart(symbol, 3)
    labels = []
    ds = []
    for rows in data:
        labels.append(rows['date'])
        ds.append(rows['close'])
    
    chart.set_labels(labels)
    chart.add_dataset(ds)
    chart.set_params(fillColor = "rgba(220,220,220,0.5)", strokeColor = "rgba(220,220,220,0.8)", highlightFill = "rgba(220,220,220,0.75)", highlightStroke = "rgba(220,220,220,1)",)
    company_chart = chart.make_chart_full_html()
    return render_template("search.html", company_chart=company_chart, current_price=current_price)


@app.route("/dashboard")
def dashboard():
    """
    @author EM
    Functionality for the user dashboard/portfolio function.
    """
    # List all users
    users = User.query.all()
    

@app.route("/buy")
def buy():
    """
    @author 
    Functionality for the user buy function.
    """
    return render_template("index.html", message="You have bought some shares.")


@app.route("/sell")
def sell():
    """
    @author 
    Functionality for the user sell function.
    """
    # Enable selling of shares
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
    user = User().add_user("bob")
    return "A user has been registered."

def main():
    # Create a database with tables
    # This method will only be called at the beginning of the program
    # to initiate the database and never again.
    db.create_all()


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
