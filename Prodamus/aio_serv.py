from aiohttp import web
import prodamuspy

API_TOKEN = "aaaa"
routes = web.RouteTableDef()


@routes.get('/')
async def hello(request):
    return web.Response(text="Hello, world")


@routes.post('/payment')
async def payment(request):
    print(request.headers)
    print(request)
    receivedSign = request.headers.get('Sign')

    #-------------------
    API_TOKEN = "aaaa"
    prodamus = prodamuspy.ProdamusPy(API_TOKEN)
    bodyDict = prodamus.parse("http://0.0.0.0:8080/payment")
    # Verify signature:
    signIsGood = prodamus.verify(bodyDict, receivedSign)
    if signIsGood:
        print("Signature is awesome")
    else:
        print("Signature is incorrect")

    print(web.Response())
    #----------------------


    return web.Response(text="payment, Ok")


if __name__ == '__main__':
    app = web.Application()
    app.add_routes(routes)
    web.run_app(app)

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
# ==================================