import sqlite3

con = sqlite3.connect("payments.db")
cursor = con.cursor()


# Добавления информации о платеже в базу данных Sqlite
def add_payments(data):
    # data1 = {'date': '2024-07-10T04:11:02+03:00',
    #         'order_id': '22583868',
    #         'order_num': '7',
    #          'sum': '50.00',
    #          'customer_phone': '+79199485553',
    #          'customer_email': 'smg_2006@list.ru',
    #          "products_name": "test good",
    #          "payment_init": "manual"
    #          }

    data1 = ('2024-07-10T04:11:02+03:00',
             '22583868',
             '7',
             '50.00',
             '+79199485553',
              'smg_2006@list.ru',
             "test good",
              "manual"
             )

    cursor.execute("INSERT INTO payments (date,order_id,order_num,sum,customer_phone,customer_email,"
                   "products_name,payment_init) VALUES (?,?,?,?,?,?,?,?)", data1)

    # Необходимо из data сделать кортеж в нужном порядке (смотри по аналогии выше)
    # И после VALUES поставить необходимое кол-во вопросов в скобках
    print("== входящие данные ==", data)
    print("== входящие данные Тип ==", type(data))
    con.commit()


# add_payments({1: 1, 2: 2,...})
