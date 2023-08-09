
Выполненное "Тестовое для веб-разработчика на Python"
https://yandex.ru/q/pythontalk/12749745666/



**Как пользоваться**

1. Создание виртуального окружения.
Предполагаем, что Python >=3.5 и библиотека virtualenv уже установлены. Затем надо склонировать проект в локальную папку. Перейти в папку проекта и создать виртуальное окружение 'python -m venv my_virt'. Зайти в my_virt\Scripts и запустить виртуальное окружение командой activate. Находясь в виртуальном окружении вызвать команду 'pip install -r requirments.txt'.

2. Запуск локального сервера.
Перейти в папку проекта 'app', выполнить в терминале команду 'uvicorn main:app --reload'

3. Создание БД.
3.1 Файл database/create_database_postgresql.py - запускается вручную f5 либо через терминал. Количество клиентов по умолчанию number_of_clients = 10. **Кроме момента использования последнюю строку лучше держать держать закоментированной.**
3.2 Предполагается, что сервер PostgreSQL установлен локально. В файле database/model.py есть строка создания движка БД, её надо **заполнить в соответствии с данными своей локальной машины.**
3.3 Файл database/create_database_postgresql.py создаёт БД из двух таблиц. В первой 'Clients' заполнено только поле Имя, вторая 'Transactions' пустая.

4. Заполнение БД.
Заполнить БД можно двумя способами:
4.1 Автоматически, запустив файл database/data_filling.py.
В методах (начисление, списание и перевод) выставляются параметры и запускаются f5 либо из cli.
Параметры 'количество операций' и 'переводимые суммы' выставлены по дефолту, но можно поправить, 'комментарии' - набор знаков.
4.2 По одной записи из командной строки, для контроля работы программы.
Из командной строки запускаем методы 'put'.
  - добавление денег на счёт
  curl -X PUT -H "Content-Type: application/json" "http://127.0.0.1:8000/api/clients/accrual" -d "{\"incoming_amount\": \"10000\", \"id\":\"1\", \"comments\": \"hohoho\"}"
  - снятие денег со счёта
  curl -X PUT -H "Content-Type: application/json" "http://127.0.0.1:8000/api/clients/writeoff" -d "{\"outgoing_amount\": \"333\", \"id\":\"11\", \"comments\": \"hehehe\"}"
  - перевод денег между клиентами сервиса
  curl -X PUT -H "Content-Type: application/json" "http://127.0.0.1:8000/api/clients/transfer" -d "{\"id_client_from\": \"1\", \"id_client_to\": \"4\", \"transfer_amount\": \"500\", \"comments\": \"for you, bro\"}"
                                                                 
Данные пишутся:
- изменение баланса в таблицу Clients 
- каждая операция, включая неудачные - в таблицу Transactions

5. Другие возможности
5.1. Просмотр данных
  - get (all users)
  curl -X GET -H "Content-Type: application/json" "http://127.0.0.1:8000/api/clients" 
  - get (one user current balance rub (default))
  curl -X GET -H "Content-Type: application/json" "http://127.0.0.1:8000/api/clients/1"
  - get (one user current balance usd)
  curl -X GET -H "Content-Type: application/json" "http://127.0.0.1:8000/api/clients/1?currency=usd" 
  - get (all users all transactions)
  curl -X GET -H "Content-Type: application/json" "http://127.0.0.1:8000/api/transactions"
  - get (one user all transactions)
  curl -X GET -H "Content-Type: application/json" "http://127.0.0.1:8000/api/transactions/3" 
5.2. Создание нового клиента                                                          
  - post (create new client)
  curl -X POST -H "Content-Type: application/json" "http://127.0.0.1:8000/api/clients" -d "{\"name\": \"New Dude\", \"balance\": \"999\"}"   
5.3 Метод delete не определён по соображениям безопасности. 


6. Сделаны дополнительные задания
- Онлайн перевод текущего рублёвого баланса в usd по актуальному курсу
- Получение списка транзакций по конкретному клиенту.


7. Не сделано:
1. docker и docker-compose
2. "Если есть потребность, можно подключить, можно подключить кеши (Redis) и/или очереди (RabbitMQ, Kafka)" - не было потребности.  