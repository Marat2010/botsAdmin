import prodamuspy


API_TOKEN = "aaaa"


# Init object:

# prodamus = prodamuspy.PyProdamus(API_TOKEN)
prodamus = prodamuspy.ProdamusPy(API_TOKEN)

# Parse query string to a dictionary:
bodyDict = prodamus.parse(body)

# Create signature:
checkSign = prodamus.sign(bodyDict)

# Verify signature:
signIsGood = prodamus.verify(bodyDict, receivedSign)
if signIsGood:
    print("Signature is awesome")
else:
    print("Signature is incorrect")


# ======= URL адрес для уведомлений об оплате =======
# https://prodamus.bot.z2024.site/Payment_Notification
# ===================================================
# ===================================================
# ===================================================

