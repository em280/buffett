import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import DateTime
from sqlalchemy.sql import func

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)

    def add_user(self, name):
        usr = User(username=name, password="passhash")
        db.session.add(usr)
        db.session.commit()

    def remove_user(self, id):
        """
        @author EM
        Remove the user from the game.
        """
        usr = User.query.get(int(id))
        if not usr:
            return False
        # usr = User.query.get(int(id))
        db.session.delete(usr)
        db.session.commit()

    def __repr__(self):
        return f"User('{self.username}')"

# class Portfolio(db.Model):
#     __tablename__ = "portfolio"
#     # foreign key relates to user table primary key
#     id = db.Column(db.Integer, primary_key=True)
#     users_id = db.Column(db.Integer, db.ForeignKey("user.id"))
#     users = db.relationship("User", back_populates="portfolio")
#     symbol = db.Column(db.String, nullable=False)
#     quantity = db.Column(db.Integer, nullable=False)
#     transaction_type = db.Column(db.Integer, nullable=False)

# class History(db.Model):
#     __tablename__ = "history"
#     id = db.Column(db.Integer, primary_key=True)
#     transaction_date = db.Column(DateTime(timezone=True), server_default=func.now())
#     quantity = db.Column(db.Integer, nullable=False)
#     users_id = db.Column(db.Integer, db.ForeignKey("user.id"))
#     users = db.relationship("User", back_populates="history")
#     symbol = db.Column(db.String, nullable=False)
#     transaction_type = db.Column(db.Integer, unique=False)
