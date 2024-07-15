import os
import logging
import sqlite3
from sqlite3 import OperationalError, ProgrammingError

from dotenv import load_dotenv

# Загрузка переменных среды из .env файла
load_dotenv("../.env")
# Логирование в файл
# logging.basicConfig(level=logging.INFO, filemode="w")
LOG_FILE = os.getenv("LOG_PRODAMUS")

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s [%(levelname)s] [%(module)s] [%(funcName)s]: %(message)s',
                    handlers=[logging.FileHandler(LOG_FILE, mode='w'), stream_handler])

# logging.basicConfig(level=logging.INFO, filename=LOG_FILE, filemode="w",
#                     format="[%(asctime)s] [%(levelname)s] %(message)s")

DB_SQLITE_NAME = os.getenv("DB_SQLITE_NAME")  # Имя файла БД Sqlite

# con = sqlite3.connect(f"./DB_Sqlite/{DB_SQLITE_NAME}")
con = sqlite3.connect(f"./{DB_SQLITE_NAME}")
cursor = con.cursor()


# Добавления информации о платеже в базу данных Sqlite
def add_payments(data_dict):

    data = data_to_dataDB(data_dict)  # Переводим словарь данных в кортеж, для последующего занесения в БД

    try:
        cursor.execute("INSERT INTO payments (date,order_id,order_num,sum,customer_phone,customer_email,"
                   "products_name,payment_init) VALUES (?,?,?,?,?,?,?,?)", data)
        logging.info(f"=== Данные внесены. Файл БД Sqlite: {os.path.abspath(DB_SQLITE_NAME)} ===")

    except OperationalError as e:
        logging.warning(f" =! Нет Файла БД Sqlite !=: {e}")
        logging.warning(f"=! Данные НЕ внесены.!!! Создаем БД !=\n")
        create_DB()
        logging.info(f"=== Создан Файл БД Sqlite: {os.path.abspath(DB_SQLITE_NAME)} ===")
        logging.info("=== Повторяем последнюю операцию!!! ===\n")
        add_payments(data)

    except ProgrammingError as e:
        logging.error(f"=!!! Неверное количество предоставленных данных !!!=: {e}")

    except Exception as e:
        logging.error(f" =!!! Ошибка !!!=: {e}")

    con.commit()


# Переводим словарь данных в кортеж, для последующего занесения в БД
def data_to_dataDB(data):
    if isinstance(data, dict):
        try:
            dataDB = (data['date'],
                      data['order_id'],
                      data['order_num'],
                      data['sum'],
                      data['customer_phone'],
                      data['customer_email'],
                      data['products'][0]['name'],
                      data['payment_init'],
                      )
        except KeyError as e:
            logging.error(f"=!!! Нет необходимого ключа !!!=: {e}")

    else:
        dataDB = data
    return dataDB


def create_DB():
    # Создаем таблицу "payments", оплативших клиентов
    # Данные берутся из пришедшего json, которые определяются в словаре "data" в файле "payment_link.py"
    cursor.execute("""CREATE TABLE payments
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT,
                    order_id TEXT,
                    order_num TEXT,
                    sum TEXT,
                    customer_phone TEXT,
                    customer_email TEXT,
                    products_name TEXT,
                    payment_init TEXT)
                    """)


if __name__ == '__main__':
    pass

    # =========== Для тестов==================
    # data1 = {'date': '2024-07-10T04:11:02+03:00',
    #         'order_id': '22583868',
    #         'order_num': '7',
    #          'sum': '50.00',
    #          'customer_phone': '+79199485553',
    #          'customer_email': 'smg_2006@list.ru',
    #          "products_name": "test good",
    #          "payment_init": "manual"
    #          }
    # ===============================

    # data2 = ('2024-07-10T04:11:02+03:00',
    #          '22583868',
    #          '7',
    #          '50.00',
    #          '+79199485553',
    #           'smg_2006@list.ru',
    #          "test good",
    #         1222222
    #          )
    # ===============================

    # create_DB()
    # add_payments(data2)

