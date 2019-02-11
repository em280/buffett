import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

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

    def add_user(self, name):
        usr = User(username=name, password="passhash")
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
        # usr = User.query.get(int(id))
        db.session.delete(usr)
        db.session.commit()

    def __repr__(self):
        return f"<User {self.id}, '{self.username}', {self.cash}>"

class Portfolio(db.Model):
    """
    A representation of the portfolio table in the database.
    """
    __tablename__ = "portfolio"
    id = db.Column(db.Integer, primary_key=True)
    usr_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    symbol = db.Column(db.String, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    transaction_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def add_portfolio_stock(self, usr_id, symbol, quantity):
        """ Add a user's stock to their portfolio. """
        ptf = Portfolio(usr_id=int(usr_id), symbol=symbol, quantity=int(quantity))
        db.session.add(ptf)
        db.session.commit()

    # maybe update the portfolio as well

    def get_portfolio_stocks(self, id):
        """
        Retrieve a user's stock from the portfolio table.
        """
        usr = User.query.get(int(id))
        if not usr:
            return False
        return Portfolio.query.filter_by(usr_id=int(id)).all()

    def remove_portfolio_stock(self, symbol):
        """
        Remove a user's stock from the portfolio table.
        """
        ptf = Portfolio.query.get(symbol)
        if not ptf:
            return False
        db.session.delete(ptf)
        db.session.commit()

    def __repr__(self):
        return f"Portfolio('{self.id}', '{self.symbol}', '{self.quantity}')"

class History(db.Model):
    __tablename__ = "history"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    symbol = db.Column(db.String, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    # transaction_type = db.Column(db.Integer, unique=False)
    transaction_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def add_hist(self, usrid, symbol, quantity):
        hist = History(user_id=usrid, symbol=symbol, quantity=int(quantity))
        db.session.add(hist)
        db.session.commit()
