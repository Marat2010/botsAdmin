"""
  Реализация принятия уведомления об успешной оплате.
  Поднимаем сервер на aiohttp (так как устанавливается вместе с Aiogram3)
  Он принимает POST запрос от продамуса, перешедшего на этот сервер
по ссылке URL_NOTIFICATION.
 Этот URL мы передавали при формировании ссылки для оплаты в
 файле payment_link.py
"""
import os
from aiohttp import web
import prodamuspy
from dotenv import load_dotenv

# Загрузка переменных среды из .env файла
load_dotenv("../.env")

# Переменные окружения "взяты" из payment_link.py (В будущем лучше
# организовать через settings Pydantic, а не ".env")
SECRET_KEY_PAYMENT = os.getenv("SECRET_KEY_PAYMENT")  # Секретный ключ для оплаты
URL_NOTIFICATION = os.getenv("URL_SUCCESS")  # URL для уведомления об оплате
# URL_RETURN = os.getenv("URL_RETURN")  # Пока не используем!!!
# URL_SUCCESS = os.getenv("URL_SUCCESS")  # Пока не используем!!!

routes = web.RouteTableDef()  # для маршрутов, страниц, путей


@routes.get('/')  # Тестовая home страница
async def hello(request):
    print("Проверка доступности сервера!\n", request.__dir__())
    return web.Response(text="Проверка доступности сервера на Aiohttp!")


@routes.post('/payment')  # Маршрут для Post запроса для уведомления об оплате
async def payment(request: web.Request):
    print("== reg_headers", request.headers)  # HTTP Заголовки
    receivedSign = request.headers.get('Sign')  # Здесь Ключ 'Sign', подписанный продамусом
    print("== receivedSign ==", receivedSign)

    # Используем документацию: https://pypi.org/project/prodamuspy/
    prodamus = prodamuspy.ProdamusPy(SECRET_KEY_PAYMENT)  # инициализаци

    # Получаем данные тип: MultiDictProxy, почти как словарь
    data = await request.post()
    print("== data: == ", data)
    print("== REQUEST DICT: == ", request.__dict__)
    print("== REQUEST JSON  : == ", request.message)
    # print("== REQUEST_read_bytes: == ", request._read_bytes())

    # Попытка перевести в словарь, если не вложенный словарь, то все ОК.
    # Надо найти нормальный метод, способ перевода.
    data_dict = dict(data)
    print("== data_dict :== ", data_dict)

    # Verify signature:
    signIsGood = prodamus.verify(data_dict, receivedSign)
    # Проверка принятого из заголока HTTP подписи продамуса
    # с подписью, которую мы сформируем из принятых данных и ключа
    if signIsGood:
        print("Signature is awesome")
    else:
        print("Signature is incorrect")

    # ===================================
    # Здесь можно формировать свой код, ... например
    # отправку сообщения боту, ....
    # ==================================

    print(web.Response())
    return web.Response(status=200)  # Ответ 200 для продамуса.
    # return web.Response(text="Payment, Ok")


if __name__ == '__main__':
    # Стандартный запуск Aiohttp server-а
    app = web.Application()
    app.add_routes(routes)
    web.run_app(app)

# =========================================
# ====== Альтернативный способ ====
# async def hello(request):
#     return web.Response(text="Hello, world")
#
# app = web.Application()
# app.add_routes([web.get('/', hello)])
#
#
# if __name__ == '__main__':
#     web.run_app(app)

# =========================================
#     Моя ссылка на Ngrok для проверки:
# https://2114-178-204-220-54.ngrok-free.app/payment
# =========================================
# =========================================
# ============ Проверки !!!!  ===============================
# ======= ССылка на оплату !!!!  ==============
# https://volynets.payform.ru/?order_id=7&customer_phone=%2B79199485553&customer_email=volynec-s%40bk.ru&products%5B0%5D%5Bsku%5D=sku01&products%5B0%5D%5Bname%5D=test+good&products%5B0%5D%5Bprice%5D=50&products%5B0%5D%5Bquantity%5D=1&do=pay&urlReturn=https%3A%2F%2F2114-178-204-220-54.ngrok-free.app%2Fpayment&urlSuccess=https%3A%2F%2F2114-178-204-220-54.ngrok-free.app%2Fpayment&urlNotification=https%3A%2F%2F2114-178-204-220-54.ngrok-free.app%2Fpayment&sys=bysviat&discount_value=0.0&paid_content=%D0%A2%D0%B5%D0%BA%D1%81+%D1%81%D0%BE%D0%BE%D0%B1%D1%89%D0%B5%D0%BD%D0%B8%D1%8F&signature=92fc28ee8c2e50b92319d43cb6f6fd8f03edea694e03a007afc0aa2d4ff2299e

# ================ После Оплаты ==================
# https://2114-178-204-220-54.ngrok-free.app/payment?_payform_status=success&_payform_id=20963369&_payform_order_id=7&_payform_sign=35b202db806702b202c6a2f7d6db1a0e1fbbba832dfa4344459d6b945191ead1
# =======================================
# KeyError: 'asa'
# ==reg_headers <CIMultiDictProxy('Host': '2114-178-204-220-54.ngrok-free.app', 'User-Agent': 'curl', 'Content-Length': '833', 'Accept': '*/*', 'Content-Type': 'application/x-www-form-urlencoded', 'Sign': '6c5f2a8e8d22d19878a7b57304951b2aa4db4fe102ce0157e6f4f5c1f2826844', 'X-Forwarded-For': '178.154.224.160', 'X-Forwarded-Host': '2114-178-204-220-54.ngrok-free.app', 'X-Forwarded-Proto': 'https', 'Accept-Encoding': 'gzip')>
# ARGS string:
# ===data===       : <MultiDictProxy()>
# ARGS       : <MultiDictProxy()>
# ==req_post: <MultiDictProxy('date': '2024-05-02T00:46:06+03:00', 'order_id': '20963369', 'order_num': '7', 'domain': 'volynets.payform.ru', 'sum': '50.00', 'currency': 'rub', 'customer_phone': '+79199485553', 'customer_email': 'volynec-s@bk.ru', 'customer_extra': '', 'payment_type': 'Быстрый платёж, без ввода данных карты. Для карт РФ', 'commission': '2.9', 'commission_sum': '1.45', 'attempt': '1', 'sys': 'bysviat', 'discount_value': '0.0', 'products[0][name]': 'test good', 'products[0][price]': '50.00', 'products[0][quantity]': '1', 'products[0][sum]': '50.00', 'payment_status': 'success', 'payment_status_description': 'Успешная оплата', 'payment_init': 'manual')>

# ==reg_headers <CIMultiDictProxy('Host': '2114-178-204-220-54.ngrok-free.app', 'User-Agent': 'curl', 'Content-Length': '833', 'Accept': '*/*', 'Content-Type': 'application/x-www-form-urlencoded', 'Sign': '6c5f2a8e8d22d19878a7b57304951b2aa4db4fe102ce0157e6f4f5c1f2826844', 'X-Forwarded-For': '178.154.224.160', 'X-Forwarded-Host': '2114-178-204-220-54.ngrok-free.app', 'X-Forwarded-Proto': 'https', 'Accept-Encoding': 'gzip')>
# ARGS string:
# ===data===       : <MultiDictProxy()>
# ARGS       : <MultiDictProxy()>
# ==req_post: <MultiDictProxy('date': '2024-05-02T00:46:06+03:00', 'order_id': '20963369', 'order_num': '7', 'domain': 'volynets.payform.ru', 'sum': '50.00', 'currency': 'rub', 'customer_phone': '+79199485553', 'customer_email': 'volynec-s@bk.ru', 'customer_extra': '', 'payment_type': 'Быстрый платёж, без ввода данных карты. Для карт РФ', 'commission': '2.9', 'commission_sum': '1.45', 'attempt': '1', 'sys': 'bysviat', 'discount_value': '0.0', 'products[0][name]': 'test good', 'products[0][price]': '50.00', 'products[0][quantity]': '1', 'products[0][sum]': '50.00', 'payment_status': 'success', 'payment_status_description': 'Успешная оплата', 'payment_init': 'manual')>

# ======= End Проверки !!!!==================================
# =============================================================

# async def payment(request: web.Request):
#     print("==reg_headers", request.headers)
#
#     print('ARGS string:', request.query_string)
#     data = request.query
#     print('===data===       :', data)
#     # print('===data[asa]===       :', data['asa'])
#     print('ARGS       :', request.query)
#     # print("===data=== ", data)
#     # print(await resp.json())
#
#     receivedSign = request.headers.get('Sign')
#     # receivedSign = request.headers.get('signature')
#     #-------------------
#     prodamus = prodamuspy.ProdamusPy(API_TOKEN)
#
#     # body = generated_payment_link
#     # bodyDict = prodamus.parse(body)
#     # body = request.json()
#     # print("==body== ", body)
#     # bodyDict = prodamus.parse(request.query_string)
#     # bodyDict = prodamus.parse(body)
#     # bodyDict = request.json()
#     # bodyDict = async json(*, loads=json.loads)[source]
#     req_post = await request.post()
#     print("==req_post:", req_post)
#     print("==req_post.key:", req_post['asa'])
#
#     # text = json.dumps(req_post)
#     text = dict(req_post)
#     print("==text :== ", text)
#
#     bodyDict = await request.json()
#     print("==bodyDict :== ", bodyDict)
#
#
#
#     # bodyDict = request.body
#     # bodyDict = request.query_string
#
#     # Verify signature:
#     signIsGood = prodamus.verify(bodyDict, receivedSign)
#     if signIsGood:
#         print("Signature is awesome")
#     else:
#         print("Signature is incorrect")
#
#     print(web.Response())
#     #----------------------
#
#
#     return web.Response(text="payment, Ok")

# ========== OLD_1=====================================
# @routes.post('/payment')
# async def payment(request: web.Request):
#     print("==request", request)
#     print("==reg_headers", request.headers)
#
#
#     print('ARGS string:', request.query_string)
#     data = request.query
#     print('===data===       :', data)
#     # print('===data[asa]===       :', data['asa'])
#     print('ARGS       :', request.query)
#     # print("===data=== ", data)
#     # print(await resp.json())
#
#     receivedSign = request.headers.get('Sign')
#     # receivedSign = request.headers.get('signature')
#     #-------------------
#     prodamus = prodamuspy.ProdamusPy(API_TOKEN)
#
#     # body = generated_payment_link
#     # bodyDict = prodamus.parse(body)
#     # body = request.json()
#     # print("==body== ", body)
#     # bodyDict = prodamus.parse(request.query_string)
#     # bodyDict = prodamus.parse(body)
#     # bodyDict = request.json()
#     # bodyDict = async json(*, loads=json.loads)[source]
#     req_post = await request.post()
#     print("==req_post:", req_post)
#     # print("==req_post.key:", req_post['asa'])
#
#     # text = json.dumps(req_post)
#     text = dict(req_post)
#     print("==text :== ", text)
#
#     # bodyDict = await request.json()
#     # print("==bodyDict :== ", bodyDict)
#
#     # https://2114-178-204-220-54.ngrok-free.app/payment
#
#     # bodyDict = request.body
#     # bodyDict = request.query_string
#
#     # Verify signature:
#     signIsGood = prodamus.verify(bodyDict, receivedSign)
#     if signIsGood:
#         print("Signature is awesome")
#     else:
#         print("Signature is incorrect")
#
#     print(web.Response())
#     #----------------------
#
#
#     return web.Response(text="payment, Ok")
# =====================================================
# ===============================================