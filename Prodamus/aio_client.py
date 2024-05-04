"""
  Реализация aiohttp клиента.
  Для проверки, тестирования, отправки POST запросов от имени продамуса
  Или можно в postmane.
"""

import aiohttp
import asyncio

from payment_link import SECRET_KEY_PAYMENT, sign

url = 'http://127.0.0.1:8080/payment'


async def main():
    async with aiohttp.ClientSession() as session:
        # payload = {'key1': 'value1', 'key2': 'value2', 'asa': ['q1', '123']}
        # Вложенные словари - будут ошибки!!!
        payload = {'key1': 'value1', 'key2': 'value2', 'asa': 999}

        # payload['signature'] = sign(payload, SECRET_KEY_PAYMENT)
        headers = {'Sign': sign(payload, SECRET_KEY_PAYMENT)}

        async with session.post(url, data=payload, headers=headers) as resp:
            print(await resp.text())

asyncio.run(main())


# ========================================
# ------- JSON data----------
# requests uses json= to send JSON and it automatically convert dictionary
# and add header 'Content-Type': 'application/json'.

# import requests
# r = requests.post('http://0.0.0.0:8080/test', json={'param1': 'value1', 'param2': 'value2'})
# ------ The same with standard data= .------

# import requests
# import json
#
# r = requests.post('http://0.0.0.0:8080/test',
#                   data=json.dumps({'param1': 'value1', 'param2': 'value2'}),
#                   headers={'Content-Type': 'application/json'},
#                  )
# --- It may raise error when there is no JSON data. ---------------
# from aiohttp import web
#
# routes = web.RouteTableDef()
#
# @routes.post('/test')
# async def test(request):
#
#     try:
#         print('JSON:', await request.json())  # json data as dictionary/list
#     except Exception as ex:
#         print('JSON: ERROR:', ex)
#
#     return web.Response(text='Received...')
#
# app = web.Application()
# app.add_routes(routes)
#
# if __name__ == '__main__':
#     web.run_app(app)

# -------POST data ---------------
# import requests
# r = requests.post('http://0.0.0.0:8080/test', data={'param1': 'value1', 'param2': 'value2'})
# -----  It doesn't raise error when there is no POST data ------------
# from aiohttp import web
#
# routes = web.RouteTableDef()
#
# @routes.post('/test')
# async def test(request):
#
#     print('POST       :', await request.post())         # POST data
#
#     return web.Response(text='Received...')
#
# app = web.Application()
# app.add_routes(routes)
#
# if __name__ == '__main__':
#     web.run_app(app)


# ========================================
# # async with session.get('http://0.0.0.0:8080/payment') as resp:
# async with session.get('http://0.0.0.0:8080/') as resp:
#     print(resp.status)
#     print(await resp.text())
# async with session.post('http://0.0.0.0:8080/payment', data=b'data'):
#     print(resp.status)
#     print(await resp.text())

# ========================================
# ========================================