# depreciated

from flask import Flask, render_template, request
from models import User

import csv
import os

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
db.init_app(app)

def main():
    fl = open("starter_db.csv")
    reader = csv.reader(fl)
    for username, password in reader:
        user = User(username=username, password=password)
        db.session.commit()
    db.session.commit()

if __name__ == "__main__":
    with app.app_context():
        main()
