"""
  Реализация принятия уведомления об успешной оплате.
  Поднимаем сервер на aiohttp (так как устанавливается вместе с Aiogram3)
  Он принимает POST запрос от продамуса, перешедшего на этот сервер
по ссылке URL_NOTIFICATION.
 Этот URL мы передавали при формировании ссылки для оплаты в
 файле payment_link.py
"""
# import ssl
import os
import logging
from json import JSONDecodeError

from aiohttp import web
from dotenv import load_dotenv

from utils_prodamus import sign
from DB_Sqlite.adding_payments import add_payments
# from Prodamus.DB_Sqlite.adding_payments import add_payments

# Загрузка переменных среды из .env файла
load_dotenv("../.env")
# Логирование в файл
logging.basicConfig(level=logging.INFO, filename="verif_pay.log", filemode="w",
                    format="[%(asctime)s] [%(levelname)s] %(message)s")

# Переменные окружения "взяты" из ".env"
# (В будущем лучше организовать через settings Pydantic)
SECRET_KEY_PAYMENT = os.getenv("SECRET_KEY_PAYMENT")  # Секретный ключ для оплаты
# URL_NOTIFICATION = os.getenv("URL_SUCCESS")  # URL для уведомления об оплате
# URL_RETURN = os.getenv("URL_RETURN")  # Пока не используем!!!
# URL_SUCCESS = os.getenv("URL_SUCCESS")  # Пока не используем!!!

routes = web.RouteTableDef()  # для маршрутов, страниц, путей


# Путь вначале "/prodamus" выставляется для всех маршрутов, т.к. в настройках Nginx это корневой маршрут
# для переадресации на наш aiohttp сервер
@routes.post('/prodamus/notification')  # Маршрут для Post запроса для уведомления об оплате
async def payment_notification(request: web.Request):
    receivedSign = request.headers.get('Sign')  # Здесь Ключ 'Sign', подписанный продамусом
    print("=== Полученная подпись (receivedSign) ===", receivedSign)
    logging.info(f"=== Полученная подпись (receivedSign): {receivedSign} ===")

    try:
        # Получаем данные в формате json. Задается в "payment_link" параметр "'callbackType': 'json',"
        data_json = await request.json()
    except JSONDecodeError as e:
        print(f"Плохо - Нет данных в формате JSON.\n", e)
        logging.error(f"=!!! Плохо - Нет данных в формате JSON: {e} !!!=")
        return web.Response(status=400, text="=!!! Нет данных в формате JSON !!!=")  # Ответ 400 для продамуса.

    # подписываем эти данные с помощью кастомной функции sign
    # (см utils_prodamus, вынес все утилиты продамуса, отдельно)
    sign_my = sign(data_json, SECRET_KEY_PAYMENT)
    print("=== Наша подпись (sign_my) === ", sign_my)
    logging.info(f"=== Наша подпись (sign_my): {sign_my} === ")

    # Сравниваем две подписи
    if receivedSign == sign_my:
        print("Совпадение - Signature is awesome")
        logging.info("=== Совпадение - Signature is awesome === ")

        # ===================================
        # Здесь можно формировать свой код, ... например
        # отправку сообщения боту, занести данные об оплате в БД, ....
        # ==================================

        # Добавление записи в базу данных Sqlite
        add_payments(data_json)

        return web.Response(status=200, text="Ok")  # Ответ 200 для продамуса.

    else:
        # add_payments(data_json)
        print("=!!! Плохо - Signature is incorrect !!!=")
        logging.error("=!!! Плохо - Signature is incorrect !!!=")
        return web.Response(status=400, text="Подписи не совпадают")  # Ответ 400 для продамуса.


@routes.get('/prodamus/successful')  # Маршрут для возврата пользователя при успешной оплате
async def successful_payment(request):
    print("=== Оплата прошла удачно! ===")
    logging.info("=== Оплата прошла удачно! ===")
    return web.Response(text="Оплата прошла удачно!")


@routes.get('/prodamus/return')  # Маршрут для возврата пользователя без оплаты
async def without_payment(request):
    print("=!!! Оплата НЕ прошла !!!=")
    logging.warning("=!!! Оплата НЕ прошла !!!=")
    return web.Response(text="</h2>!!! Оплата НЕ прошла !!!</h2>")


@routes.get('/prodamus')  # Тестовая home страница
async def hello(request):
    print("=== Проверка доступности сервера на Aiohttp прошла! ===")
    logging.info("=== Проверка доступности сервера на Aiohttp прошла! ===")
    return web.Response(text="Проверка доступности сервера на Aiohttp прошла!")


if __name__ == '__main__':
    # Стандартный запуск Aiohttp server-а
    app = web.Application()
    app.add_routes(routes)
    web.run_app(app, host='127.0.0.1', port=9090)

    # web.run_app(app)
    # ====== Для запуска httpS =========================
    # ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    # ssl_context.load_cert_chain('127.0.0.1.crt', '127.0.0.1.key')
    # web.run_app(app, host='localhost', port=9090, ssl_context=ssl_context)
# =========================================================
# ====== Альтернативный способ запуска Aiohttp сервера ====
# async def hello(request):
#     return web.Response(text="Hello, world")
#
# app = web.Application()
# app.add_routes([web.get('/', hello)])
#
#
# if __name__ == '__main__':
#     web.run_app(app)

# =========================================================
