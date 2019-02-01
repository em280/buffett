from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    cash = db.Column(db.Integer, default=1000)

    def __repr__(self):
        return f"User('{self.username}', '{self.cash}')"
