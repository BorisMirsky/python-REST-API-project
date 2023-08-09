"""
Автоматическое заполнение нашей БД искусственными данными:
- Функция 'добавление денег' curl_request('plus').
- Функция 'снятие денег' curl_request('minus').
- Функция 'перевод денег между клиентами сервиса' curl_request_transfer().

"""

from create_database_postgresql import number_of_clients
import random
import requests

def generate_id(stop):
    result = random.choice([x for x in range(1, stop + 1, 1)])
    return result

def generate_amount(low, up):
    amount = random.randint(low, up)
    return amount

def generate_comment(length):
    a = ord('а')
    letters = ''.join([chr(i) for i in range(a, a+32)])   
    result = ''.join(random.choice(letters) for i in range(length))
    return result

def generate_id_for_transfer(stop):
    result_1 = random.choice([x for x in range(1, stop + 1, 1)])
    result_2 = random.choice([x for x in range(1, stop + 1, 1)])
    if result_1 == result_2 == 1:
        result_1 = 2
    elif result_1 == result_2 != 1:
        result_1 = result_1 - 1
    return (result_1, result_2)

  
# Снятие денег либо пополнение счёта клиентов сервиса 'извне'
def change_balance_request(sign):
    url, amount_ = "", ""
    id_ = generate_id(10)
    amount = generate_amount(10000, 50000)
    comments = generate_comment(10)
    if sign== 'plus':
        url = 'http://127.0.0.1:8000/api/clients/accrual'
        amount = 'incoming_amount'
    elif sign== 'minus':
        url = 'http://127.0.0.1:8000/api/clients/writeoff'
        amount = 'outgoing_amount'
    headers = {"Content-type": "application/json"}
    json_data = {
        'id': id_,
        'amount': amount,
        'comments': comments
        }
    response = requests.put(url, headers=headers, json=json_data)


# Перевод денег между клиентами сервиса
def transfer_request():
    url = "http://127.0.0.1:8000/api/clients/transfer"
    comments = generate_comment(20)
    amount = generate_amount(100, 500)
    id_from = generate_id_for_transfer(10)[0]
    id_to = generate_id_for_transfer(10)[1]
    headers = {"Content-type": "application/json"}
    json_data = {
        'id_client_from': id_from,
        'id_client_to': id_to,        
        'transfer_amount': amount,
        'comments': comments
        }
    response = requests.put(url, headers=headers, json=json_data)

    
for i in range(1, 30, 1):
    change_balance_request('plus')
    change_balance_request('minus')
    transfer_request()


print('done')
    







