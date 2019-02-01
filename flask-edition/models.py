from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import DateTime
from sqlalchemy.sql import func

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.cash}')"

class Portfolio(db.Model):
    __tablename__ = "portfolio"
    # foreign key relates to user table primary key
    id = db.Column(db.Integer, primary_key=True)
    users_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    users = db.relationship("Users", back_populates="portfolio")
    symbol = db.Column(db.String, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    transaction_type = db.Column(db.Integer, nullable=False)

class History(db.Model):
    __tablename__ = "history"
    id = db.Column(db.Integer, primary_key=True)
    transaction_date = db.Column(DateTime(timezone=True), server_default=func.now())
    quantity = db.Column(db.Integer, nullable=False)
    users_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    users = db.relationship("Users", back_populates="history")
    symbol = db.Column(db.String, nullable=False)
    transaction_type = db.Column(db.Integer, unique=False)
