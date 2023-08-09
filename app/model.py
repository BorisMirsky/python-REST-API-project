from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import  Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import DeclarativeBase


from fastapi import FastAPI


"""
"postgresql://postgres:password@localhost/clientsdb"

postgres - имя пользователя на сервере PostgreSQL
password - пароль
localhost - адрес сервера
clientsdb - имя базы данных на сервере
"""

engine = create_engine("postgresql://postgres:password@localhost/clientsdb")
 
Base = declarative_base()

class Client(Base):
    __tablename__ = "clients" 
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    balance = Column(Integer)
    transactions = relationship("Transaction", back_populates="client")

class Transaction(Base):
    __tablename__ = "transactions" 
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"))
    amount_receipts = Column(Integer)
    amount_withdrawal = Column(Integer)
    id_client_from = Column(Integer)
    id_client_to = Column(Integer)
    datetime = Column(String)
    comments = Column(String)
    client = relationship("Client", back_populates="transactions")


SessionLocal = sessionmaker(autoflush=False, bind=engine)









