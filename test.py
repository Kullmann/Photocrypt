from photocrypt.image.bitmap import *
from io import BytesIO

bitmap = Bitmap.open("samples/marbles.bmp")

def encrypt(data):
    nd = bytearray(data)
    for i in range(len(nd)):
        nd[i] ^= 125
    return bytes(nd)

bitmap.apply(encrypt)
bitmap.save("asdf.jpg")
