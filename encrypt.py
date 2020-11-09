#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Need to add encrypting AES key with RSA, and passing key to decrypt
# function, also need to generate entropy to randomly generate key

import base64
import io
from PIL import Image
from Cryptodome.Cipher import AES
# had to encode with utf8, was getting a some weird cant convert to c code error

def encrypt(image):
    key = "letsgetthisbread".encode("utf8")
    cipher_e = AES.new(key, AES.MODE_EAX)

    im = Image.open(io.BytesIO(image))
    with io.BytesIO() as barray:
        im.save(barray, format="BMP")
        barray = barray.getvalue()
    #print(barray[0:64])
    #print(image[0:64])
    #print(image[-2:])
    
    image = barray
    image_trimmed = image[64:-2]
    print("enc image: ",len(image_trimmed))
    ciphertext, tag = cipher_e.encrypt_and_digest(image_trimmed)
    ciphertext = image[0:64] + ciphertext + image[-2:]
    return ciphertext+b'nonce='+cipher_e.nonce+b'tag='+tag
    
