"""
@author: EM
A simple database implementation for the application.
"""

import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import datetime

db = SQLAlchemy()

class User(db.Model):
    """
    A representation of the users table in the database.
    """
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    cash = db.Column(db.Integer, default=10000)
    phone_number = db.Column(db.String(10), nullable=False)

    def add_user(self, name, password):
        usr = User(username=name, password=password)
        db.session.add(usr)
        db.session.commit()

    # use the update method which requires the use of set
    def update_user(self, id, cash):
        usr = User.query.get(id=int(id))
        usr.cash = cash

    def remove_user(self, id):
        """
        Remove the user from the game.
        """
        usr = User.query.get(int(id))
        if not usr:
            return False
        db.session.delete(usr)
        db.session.commit()

    def __repr__(self):
        return f"<User {self.id}, '{self.username}', {self.cash}>"

class Portfolio(db.Model):
    """
    A representation of the portfolio table in the database.
    This is to keep record of what the user has bought and sold.
    """
    __tablename__ = "portfolio"
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    symbol = db.Column(db.String, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    transaction_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    transaction_type = db.Column(db.String, nullable=False)

    __table_args__ = ( db.CheckConstraint(transaction_type.in_(["buy", "sell"])), )


    def add_portfolio_stock(self, userid, symbol, quantity):
        """ Add a user's stock to their portfolio. """
        ptf = Portfolio(userid=int(userid), symbol=symbol, quantity=int(quantity))
        db.session.add(ptf)
        db.session.commit()

    def get_portfolio_stocks(self, id):
        """
        Retrieve a user's stock from the portfolio table.
        """
        usr = User.query.get(int(id))
        if not usr:
            return False
        return Portfolio.query.filter_by(userid=int(id)).all()

    def __repr__(self):
        return f"Portfolio('{self.id}', '{self.symbol}', '{self.quantity}', '{self.transaction_date}', '{self.transaction_type}')"

class History(db.Model):
    __tablename__ = "history"
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, db.ForeignKey("user.id"))
    symbol = db.Column(db.String, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    transaction_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    transaction_type = db.Column(db.String, nullable=False)

    __table_args__ = ( db.CheckConstraint(transaction_type.in_(["buy", "sell"])), )

    def add_hist(self, userid, symbol, quantity, transaction_type):
        hist = History(userid=int(userid), symbol=symbol, quantity=int(quantity), transaction_type=transaction_type)
        db.session.add(hist)
        db.session.commit()

    def __repr__(self):
        return f"<History {self.id}, {self.userid}, '{self.symbol}', {self.quantity}, '{self.transaction_date}', '{self.transaction_type}' >"
