import hashlib
import hmac

# Пример подписи URL секретным ключом.
secret = 'mysecret'.encode()

url = 'https://docs-python.ru/standart-library/'.encode()
signing = hmac.new(secret, url, hashlib.sha256)
# signing.digest()


print("== hexdigest() ==", signing.hexdigest())

print("== digest_size ==", signing.digest_size)

print("== block_size ==", signing.block_size)

print("== name ==", signing.name)

# Пример подписи бинарного файла python3 секретным ключом.

secret_key = 'secret-shared-key'
digest_maker = hmac.new(secret_key.encode(), digestmod='sha256')

with open('/usr/bin/python3', 'rb') as fp:
    while True:
        block = fp.read(1024)
        if not block:
            break
        digest_maker.update(block)

digest = digest_maker.hexdigest()
name = digest_maker.name
# print(digest)
# print(name)


