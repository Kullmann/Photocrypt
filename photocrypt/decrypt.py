#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import AES, PKCS1_OAEP
import base64
import io
from PIL import Image
from Cryptodome.Cipher import AES


def decrypt(image):

    with open("../../data/encrypted_data.bin", "wb") as f:
        f.write(image)

    file_in = open("../../data/encrypted_data.bin", "rb")

    private_key = RSA.import_key(open("../../keys/private.pem").read())

    enc_session_key, nonce, tag, ciphertext = \
        [file_in.read(x) for x in (private_key.size_in_bytes(), 16, 16, -1)]

    # Decrypt the session key with the private RSA key
    cipher_rsa = PKCS1_OAEP.new(private_key)
    session_key = cipher_rsa.decrypt(enc_session_key)

    # Encrypt the data with the AES session key
    cipher_aes = AES.new(session_key, AES.MODE_EAX, nonce)
    data = cipher_aes.decrypt_and_verify(ciphertext, tag)
    print("Decrypted data: ", data)

    im = Image.open(io.BytesIO(data))
    with io.BytesIO() as barray:
        im.save(barray, format="BMP")
        barray = barray.getvalue()

    image = barray
    image_trimmed = image[64:-2]
    print("dec image: ", len(image_trimmed))
    # plaintext = cipher_aes.decrypt_and_verify(ciphertext, tag)
    plaintext = image[0:64] + image_trimmed + image[-2:]

    return plaintext


def decryptOld(image):
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
    print("dec image: ", len(image_trimmed))
    plaintext = cipher_e.decrypt(image_trimmed)
    plaintext = image[0:64] + plaintext + image[-2:]

    return plaintext
