import psycopg2
import datetime
from datetime import timedelta
import random
from russian_names import RussianNames
import time



# число клиентов сервиса, они же записи в главной таблице Clients нашей БД
number_of_clients = 10

class Clients:
    def __init__(self):
        self.name = ""
        
    def create_db(self):
        conn = psycopg2.connect(dbname="postgres", user="postgres", password="password", host="127.0.0.1")
        cursor = conn.cursor()
        conn.autocommit = True
        cursor.execute("CREATE DATABASE clientsdb")
        cursor.close()
        conn.close()

    def create_table_clients(self):
        conn = psycopg2.connect(dbname="clientsdb",
                            user="postgres",
                            password="password",
                            host="127.0.0.1")
        cursor = conn.cursor()
        #id SERIAL INTEGER NOT NULL,
        cursor.execute("""CREATE TABLE clients (
                    id SERIAL,
                    name TEXT,
                    balance INTEGER,
                    PRIMARY KEY (id)
                   )""")
        conn.commit()
        cursor.close()
        conn.close()


    def create_table_transactions(self):
        conn = psycopg2.connect(dbname="clientsdb",
                            user="postgres",
                            password="password",
                            host="127.0.0.1")
        cursor = conn.cursor()
            #id SERIAL INTEGER NOT NULL,
        cursor.execute("""CREATE TABLE transactions (
                    id SERIAL,
                    client_id INTEGER,
                    amount_receipts INTEGER,
                    amount_withdrawal INTEGER,
                    id_client_from INTEGER,
                    id_client_to INTEGER,
                    datetime TEXT,
                    comments TEXT,
                    PRIMARY KEY (id),
                    FOREIGN KEY(client_id) REFERENCES clients (id)
                   )""")
        conn.commit()
        cursor.close()
        conn.close()


    def insert_data_to_clients_table(self, _name, _balance):
        conn = psycopg2.connect(dbname="clientsdb",
                            user="postgres",
                            password="password",
                            host="127.0.0.1")
        cursor = conn.cursor()
        data = (_name, _balance)
        cursor.execute("INSERT INTO clients (name, balance) VALUES (%s, %s)", data)
        conn.commit()
        cursor.close()
        conn.close()

    # ФИО
    def generate_name(self):
        name = RussianNames().get_person()
        splitted = name.split(' ')          # ИОФ --> ФИО
        self.name = splitted[2] + ' ' + splitted[0] + ' ' + splitted[1]
        return self.name

    # Собираем результат
    def main(self):
        self.create_db()
        self.create_table_clients()
        self.create_table_transactions()
        for i in range(1, number_of_clients ,1):
            self.generate_name()
            self.insert_data_to_clients_table(self.name, 0) 
        print('done')     


my_var = Clients()

# последнюю строку держать закоментированной
#my_var.main()





