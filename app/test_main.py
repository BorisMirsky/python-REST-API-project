from fastapi.testclient import TestClient
from main import * 


client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == "Корень проекта, но фронтенда тут нет"
    print('0k')


def test_get_all_clients(db: Session = Depends(get_db)):
    response = client.get("/api/clients")
    assert response.status_code == 200
    assert response.json() == db.query(Client).all()
    print('0k')

# get balance one client
def test_get_balance_str_bad_client(id, db:Session = Depends(get_db), currency:str | None = None):
    response = client.get("/api/clients/{i}")
    client = db.query(Client).filter(Client.id == id).first()
    if client == None:
        assert JSONResponse(status_code=404, content={ "message": "Пользователь не найден"})
    print('0k')


def test_get_balance_str_bad_client_rub(id, db:Session = Depends(get_db), currency:str | None = None):
    client = db.query(Client).filter(Client.id == id).first()
    content = None
    if client != None:
        assert content == "Клиент: {0}, Баланс в рублях: {1}".format(client_parsed['name'], client_parsed['balance'])
    assert result == {"status":"OK", "code":200, "content": content}
    print('0k')


def test_get_balance_str_bad_client_usd(id, db:Session = Depends(get_db), currency:str | None = None):
    client = db.query(Client).filter(Client.id == id).first()
    content = None
    currency = None
    if client != None and currency:
        assert balance_usd == round( int(client_parsed['balance']) / current_dollar_rate, 3)
        assert content == "Клиент: {0}, Баланс в usd: {1}".format(client_parsed['name'], balance_usd)
    assert result == {"status":"OK", "code":200, "content": content}
    print('0k')

# change balance
def test_edit_client_bad_client(data = Body(), db: Session = Depends(get_db)):
    response = client.get("/api/clients/{i}")
    content = ""
    client = db.query(Client).filter(Client.id == id).first()
    if client == None:
        assert JSONResponse(status_code=404, content={ "message": "Пользователь не найден"})
    print('0k')

def test_edit_client_bad_amount(data = Body(), db: Session = Depends(get_db)):
    response = client.get("/api/clients/{i}")
    content = ""
    client = db.query(Client).filter(Client.id == id).first()
    if int(data["incoming_amount"]) <= 0:            
        assert JSONResponse(status_code=404, content={ "message": "Cумма должна быть больше нуля"})
    print('0k')

def test_edit_client_comment_processing(data = Body(), db: Session = Depends(get_db)):
    response = client.get("/api/clients/{i}")
    client = db.query(Client).filter(Client.id == id).first()
    comments_ = ""
    if 'comments' in data:
        assert comments_ == data['comments']
    print('0k')

def test_edit_client_not_enough_money(data = Body(), db: Session = Depends(get_db)):
    content, status_code = "", ""
    client = db.query(Client).filter(Client.id == data["id"]).first()
    if current_balance <= int(data["outgoing_amount"]):
        assert status_code == 404
        assert content=={ "message": "Недостаточно денег на счёте"}
    print('0k')


# money transfer between clients
def test_money_transfer_bad_client_from(data = Body(), db: Session = Depends(get_db)):
    response = client.get("/api/clients/transfer")
    content, status_code = "", ""
    client_from = db.query(Client).filter(Client.id == data["id_client_from"]).first()  # от кого перевод
    if client_from == None:
        assert JSONResponse(status_code=404, content={ "message": "Пользователь-отправитель не найден"})
    print('0k')

def test_money_transfer_bad_client_to(data = Body(), db: Session = Depends(get_db)):
    response = client.get("/api/clients/transfer")
    content, status_code = "", ""
    client_to = db.query(Client).filter(Client.id == data["id_client_to"]).first()  # от кого перевод
    if client_to == None:
        assert JSONResponse(status_code=404, content={ "message": "Пользователь-получатель не найден"})
    print('0k')

def test_money_transfer_not_enough_money(data = Body(), db: Session = Depends(get_db)):
    response = client.get("/api/clients/transfer")
    content, status_code = "", ""
    client_from = db.query(Client).filter(Client.id == data["id_client_from"]).first()  # от кого перевод
    client_from_parsed = row2dict(client_from)
    client_from_current_balance = int(client_from_parsed['balance'])
    if client_from_current_balance <= int(data["transfer_amount"]):
        assert status_code == 404
        assert content=={ "message": "Недостаточно денег на счёте"}
    print('0k')



















