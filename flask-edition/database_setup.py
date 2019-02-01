import sys 
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.sql import func
from sqlalchemy import DateTime


Base = declarative_base()

class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    
class Portfolio(Base):
    __tablename__ = "portfolio"
    # foreign key relates to user table primary key
    id = Column(Integer, primary_key=True)
    users_id = Column(Integer, ForeignKey("users.id"))
    users = relationship("Users", back_populates="portfolio")
    symbol = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    transaction_type = Column(Integer, nullable=False)
    
class History(Base):
    __tablename__ = "history"
    id = Column(Integer, primary_key=True)
    transaction_date = Column(DateTime(timezone=True), server_default=func.now())
    quantity = Column(Integer, nullable=False)
    users_id = Column(Integer, ForeignKey("users.id"))
    users = relationship("Users", back_populates="history")
    symbol = Column(String, nullable=False)
    transaction_type = Column(Integer, unique=False)
    
    


engine = create_engine("sqlite:///stock_db.db")

Base.metadata.create_all(engine)