#!/usr/bin/env python
# -*- coding: utf-8 -*-

import base64
import io
from PIL import Image
from Cryptodome.Cipher import AES
# had to encode with utf8, was getting a some weird cant convert to c code error
def decrypt(image):
    footer = image[-32-len("nonce=")-len("tag="):]
    # print(footer)
    nonce = footer[len("nonce="):len("nonce=")+16]
    tag = footer[len("nonce=")+16+len("tag="):len("nonce=")+16+len("tag=")+16]

    key = "letsgetthisbread".encode("utf8")
    cipher_e = AES.new(key, AES.MODE_EAX, nonce)

    im = Image.open(io.BytesIO(image))
    with io.BytesIO() as barray:
        im.save(barray, format="BMP")
        barray = barray.getvalue()

    image = barray
    image_trimmed = image[64:-2]
    print("dec image: ",len(image_trimmed))
    plaintext = cipher_e.decrypt(image_trimmed)
    plaintext = image[0:64] + plaintext + image[-2:]

    return plaintext
    
