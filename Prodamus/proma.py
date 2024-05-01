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

