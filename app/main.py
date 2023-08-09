# backend of project

from model import *
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker
from fastapi import Depends, FastAPI, Body, Request, Query
from fastapi.responses import JSONResponse, FileResponse
from datetime import datetime
from pydantic import create_model
from dollar import dollar_rate



app = FastAPI()

# сессия подключения к бд
SessionLocal = sessionmaker(autoflush=False, bind=engine)

# определяем зависимость
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Преобразование запроса в словарь
def row2dict(row):
    d = {}
    for column in row.__table__.columns:
        d[column.name] = str(getattr(row, column.name))
    return d


current_dollar_rate = dollar_rate()

datetime_formated = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# --------------------- Operations with balance ---------------------------------

@app.get("/")
def root():
    return "Корень проекта, но фронтенда тут нет" 

# get balance of all clients
@app.get("/api/clients")
def get_all_clients(db: Session = Depends(get_db)):
    return db.query(Client).all()


# get balance of one client
@app.get("/api/clients/{id}")  
def get_balance_str(id, db:Session = Depends(get_db), currency:str | None = None ):       
    content = ""
    client = db.query(Client).filter(Client.id == id).first()
    if client==None:  
        return JSONResponse(status_code=404, content={ "message": "Пользователь не найден"})
    client_parsed = row2dict(client)
    # '?currency=usd'
    if currency:
        balance_usd = round( int(client_parsed['balance']) / current_dollar_rate, 3)
        content = "Клиент: {0}, Баланс в usd: {1}".format(client_parsed['name'], balance_usd)
    else:
        content = "Клиент: {0}, Баланс в рублях: {1}".format(client_parsed['name'], client_parsed['balance'])
    result = {"status":"OK", "code":200, "content": content}
    return result


# change balance +
@app.put("/api/clients/accrual")
def edit_client(data = Body(), db: Session = Depends(get_db)):
    transaction = Transaction()
    content = ""
    client = db.query(Client).filter(Client.id == data["id"]).first()
    # Обработка ситуации 'клиент по id не найден'
    if client == None:
        return JSONResponse(status_code=404, content={ "message": "Пользователь не найден"})
    client_parsed = row2dict(client)
    current_balance = int(client_parsed['balance'])
    # Обработка ситуации 'введённая сумма <0'
    if int(data["incoming_amount"]) <= 0:            
        return JSONResponse(status_code=404, content={ "message": "Cумма должна быть больше нуля"})
    client.balance = current_balance + int(data["incoming_amount"])
    # Обработка ситуации 'комментария нет'
    comments_ = ""
    if 'comments' in data:
        comments_ = data['comments']
    transaction = Transaction(client_id = data["id"], amount_receipts = data["incoming_amount"],
                              datetime = datetime_formated, comments = comments_)
    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    db.refresh(client)
    content = "Клиент: {0}, Баланс в рублях: {1}, Комментарий: {2}".format(client_parsed['name'],
                                                                           client.balance, comments_)
    result = {"status":"OK", "code":200, "content": content}
    return result


# change balance -
@app.put("/api/clients/writeoff")
def edit_client(data  = Body(), db: Session = Depends(get_db)):
    transaction = Transaction()
    content, status_code = "", ""
    client = db.query(Client).filter(Client.id == data["id"]).first()
    if client == None:
        return JSONResponse(status_code=404, content={ "message": "Пользователь не найден"})
    client_parsed = row2dict(client)
    current_balance = int(client_parsed['balance'])
    comments_ = ""
    if 'comments' in data:
        comments_ = data['comments']
    if int(data["outgoing_amount"]) <= 0:
        return JSONResponse(status_code=404, content={ "message": "Cумма должна быть больше нуля"})
    elif current_balance <= int(data["outgoing_amount"]):
        transaction = Transaction(client_id = data["id"],
                              amount_withdrawal = data["outgoing_amount"],
                              datetime = datetime_formated,
                              comments = "Недостаточно денег на счёте")
        status_code = 404
        content={ "message": "Недостаточно денег на счёте"}
    else:
        status_code = 200
        client.balance = current_balance - int(data["outgoing_amount"])
        transaction = Transaction(client_id = data["id"],
                              amount_withdrawal = data["outgoing_amount"],
                              datetime = datetime_formated,
                              comments = comments_)
        content = "Клиент: {0}, Баланс в рублях: {1}, Комментарий: {2}".format(client_parsed['name'],
                                                                               client.balance, comments_)
    db.add(transaction)
    db.commit() 
    db.refresh(client)
    db.refresh(transaction)
    result = {"status_code":status_code, "content":content}   
    return result

# Перевод денег между клиентами
@app.put("/api/clients/transfer")
def money_transfer(data  = Body(), db: Session = Depends(get_db)):
    transaction_from, transaction_to = Transaction(), Transaction()
    content, status_code = "", ""
    # запрос
    client_from = db.query(Client).filter(Client.id == data["id_client_from"]).first()
    # error "Пользователь не найден" processing
    if client_from == None:
        return JSONResponse(status_code=404, content={ "message": "Пользователь-отправитель не найден"})
    client_to = db.query(Client).filter(Client.id == data["id_client_to"]).first()
    if client_to == None:
        return JSONResponse(status_code=404, content={ "message": "Пользователь-получатель не найден"})
    # parsed response
    client_from_parsed = row2dict(client_from)
    client_from_current_balance = int(client_from_parsed['balance'])
    client_to_parsed = row2dict(client_to)
    client_to_current_balance = int(client_to_parsed['balance'])
    # Обработка ситуации 'комментария нет'
    comments_ = ""
    if 'comments' in data:
        comments_ = data['comments']
    # error "Недостаточно денег на счёте" processing
    if int(data["transfer_amount"]) <= 0:
        return JSONResponse(status_code=404, content={ "message": "Cумма должна быть больше нуля"})
    elif client_from_current_balance <= int(data["transfer_amount"]):
        transaction_from = Transaction(client_id = data["id_client_from"],
                              amount_withdrawal = data["transfer_amount"],
                              datetime = datetime_formated,
                              id_client_to = data["id_client_to"],
                              comments = "Недостаточно денег на счёте")
        transaction_to = Transaction(client_id = data["id_client_to"],
                              amount_receipts = data["transfer_amount"],
                              datetime = datetime_formated,
                              id_client_from = data["id_client_from"],
                              comments = "Недостаточно денег на счёте")
        status_code=404
        content={ "message": "Недостаточно денег на счёте"}
    else:
        status_code = 200
        # change balance
        client_from.balance = client_from_current_balance - int(data["transfer_amount"])
        client_to.balance = client_to_current_balance + int(data["transfer_amount"])
        # Перевод денег между клиентами сервиса это ДВЕ транзакции и ДВЕ записи в таблицу
        transaction_from = Transaction(client_id = data["id_client_from"],
                              amount_withdrawal = data["transfer_amount"],
                              datetime = datetime_formated,
                              id_client_to = data["id_client_to"],
                              comments = comments_)
        transaction_to = Transaction(client_id = data["id_client_to"],
                              amount_receipts = data["transfer_amount"],
                              datetime = datetime_formated,
                              id_client_from = data["id_client_from"],
                              comments = comments_)
        content = "Клиент: {0}, Сумма перевода: {1}, Перевод от: {2}, Комментарий: {3}".format(
                                                                           client_to_parsed['name'],
                                                                           data["transfer_amount"],
                                                                           client_from_parsed['name'],
                                                                               comments_)
    db.add(transaction_from)
    db.add(transaction_to)
    db.commit() 
    db.refresh(client_from)
    db.refresh(client_to)
    db.refresh(transaction_from)
    db.refresh(transaction_to)
    result = {"status":"OK", "code":200, "content": content}
    return result


#-------------------------   transactions   -------------------------------------------------------
# get all transactions of all clients
@app.get("/api/transactions")
def get_all_transactions(db: Session = Depends(get_db)):
    return db.query(Transaction).all()


# get all transactions of one client
@app.get("/api/transactions/{id}")
def get_transactions(id, db: Session = Depends(get_db)):
    result = []
    transactions = db.query(Transaction).filter(Transaction.client_id == id).all()
    if transactions==[]:  
        result = JSONResponse(status_code=404, content={ "message": "Пользователь не найден"})
    for row in transactions:
        one_transaction_parsed = row2dict(row)
        one_transaction_parsed_result = "id клиента: {0}, Cумма списания: {1}, Cумма зачисления: {2}, Oт кого: {3}, Kому: {4}, Дата: {5}, Kомментарий: {6} ".format(one_transaction_parsed['client_id'],
                       one_transaction_parsed['amount_withdrawal'], one_transaction_parsed['amount_receipts'],
                       one_transaction_parsed['id_client_from'], one_transaction_parsed['id_client_to'],
                       one_transaction_parsed['datetime'], one_transaction_parsed['comments'])
        result.append(one_transaction_parsed_result)
    return result 


#-------------------------- new client ---------------------------------------------
@app.post("/api/newclient")
def create_person(data  = Body(), db: Session = Depends(get_db)):
    new_client = Client()
    new_client.name = data["name"]
    new_client.balance = data["balance"]
    db.add(new_client)
    db.commit() 
    db.refresh(new_client)
    return new_client












