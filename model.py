


from sqlalchemy import Column, Integer, String, Float, DateTime
from database import Base
from sqlalchemy.orm import relationship
import sqlite3
from datetime import datetime
Base = declarative_base()
class User(Base):
    __tablename__="User"
    
    username:Column(String,UNIQUE=True,index=  True)
    email:Column(String,UNIQUE=True,index=  True)
    hash_password: Column(String)

    
class Category(Base):
    __table__="Category"
   
    name:Column(String,nullable=False)
    user = relationship('User', back_populates='categories')
    expenses = relationship('Expense', back_populates='category')
class Expense(Base):
    __tablename__="Expense"  
    
    amount:Column(Float)
    category: Column(String)
    description:Column(String)
    date:Column(DateTime,default=datetime.now)
    user = relationship('User', back_populates='expenses')
    category = relationship('Category', back_populates='expenses')






 



    