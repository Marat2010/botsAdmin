"""Выполнить только один раз при запуске проекта, для создания базы данных!!!"""
import sqlite3

con = sqlite3.connect("payments.db")
cursor = con.cursor()

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

