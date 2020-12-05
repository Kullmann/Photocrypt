from photocrypt.image import open_image_as, CryptoBitmap
# class AESCipher:
#     def __init__(self, args*, ):
#         pass

# data = b"secret"
# key = get_random_bytes(16)
# cipher = AES.new(key, AES.MODE_CBC)
# ct_bytes = cipher.encrypt(pad(data, AES.block_size))
# print(cipher.iv, ct_bytes)


# from photocrypt.image.bitmap import Bitmap
# from photocrypt.utils.bytes import ByteStream
# from random import randint

# def encrypt(data):
#     nd = bytearray(data)
#     for i in range(len(nd)):
#         nd[i] ^= randint(0, 255)
#     return bytes(nd)


bitmap = open_image_as("hell.png", CryptoBitmap)
# bitmap.apply(encrypt)
#bitmap.save("hell.png")
print(bitmap.headers)
