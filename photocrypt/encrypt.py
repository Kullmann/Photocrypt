#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Need to add encrypting AES key with RSA, and passing key to decrypt
# function, also need to generate entropy to randomly generate key

import base64
import io
from PIL import Image
from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes
from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import AES, PKCS1_OAEP

session_key = get_random_bytes(16)


def encryptPhoto(image):
    #session_key = get_random_bytes(16)
    file_out = open("../../data/encrypted_data.bin", "wb")
    recipient_key = RSA.import_key(open("../../keys/receiver.pem").read())

    # Encrypt the session key with the public RSA key
    cipher_rsa = PKCS1_OAEP.new(recipient_key)
    enc_session_key = cipher_rsa.encrypt(session_key)

    # Encrypt the data with the AES session key
    cipher_aes = AES.new(session_key, AES.MODE_EAX)
    ciphertext, tag = cipher_aes.encrypt_and_digest(image)

    [file_out.write(x)
        for x in (enc_session_key, cipher_aes.nonce, tag, ciphertext)]
    file_out.close()
    return enc_session_key+cipher_aes.nonce+tag+ciphertext


def displayEncryption(image):
    session_key = get_random_bytes(16)
    #file_out = open("data/encrypted_data.bin", "wb")
    recipient_key = RSA.import_key(open("../../keys/receiver.pem").read())

    # Encrypt the session key with the public RSA key
    cipher_rsa = PKCS1_OAEP.new(recipient_key)
    enc_session_key = cipher_rsa.encrypt(session_key)

    # Encrypt the data with the AES session key
    cipher_aes = AES.new(session_key, AES.MODE_EAX)

    im = Image.open(io.BytesIO(image))
    with io.BytesIO() as barray:
        im.save(barray, format="BMP")
        barray = barray.getvalue()

    image = barray
    image_trimmed = image[64:-2]
    print("enc image: ", len(image_trimmed))
    ciphertext, tag = cipher_aes.encrypt_and_digest(image_trimmed)
    ciphertext = image[0:64] + ciphertext + image[-2:]

    # [file_out.write(x)
    #     for x in (enc_session_key, cipher_aes.nonce, tag, ciphertext)]
    # file_out.close()

    return ciphertext+b'nonce='+cipher_aes.nonce+b'tag='


def encryptOld(image):
    key = get_random_bytes(16)
    #key = "letsgetthisbread".encode("utf8")
    cipher_e = AES.new(key, AES.MODE_EAX)

    im = Image.open(io.BytesIO(image))
    with io.BytesIO() as barray:
        im.save(barray, format="BMP")
        barray = barray.getvalue()
    # print(barray[0:64])
    # print(image[0:64])
    # print(image[-2:])

    image = barray
    image_trimmed = image[64:-2]
    print("enc image: ", len(image_trimmed))
    ciphertext, tag = cipher_e.encrypt_and_digest(image_trimmed)
    ciphertext = image[0:64] + ciphertext + image[-2:]
    return ciphertext+b'nonce='+cipher_e.nonce+b'tag='


def encrypt(image):
    file_out = open("../../data/encrypted_data.bin", "wb")
    #text = "Whats up".encode("utf-8")
    recipient_key = RSA.import_key(open("../../keys/receiver.pem").read())
    session_key = get_random_bytes(16)

    # Encrypt the session key with the public RSA key
    cipher_rsa = PKCS1_OAEP.new(recipient_key)
    enc_session_key = cipher_rsa.encrypt(session_key)
    print("Image data: ", image)
    # Encrypt the data with the AES session key
    cipher_aes = AES.new(session_key, AES.MODE_EAX)
    ciphertext, tag = cipher_aes.encrypt_and_digest(image)
    [file_out.write(x)
        for x in (enc_session_key, cipher_aes.nonce, tag, ciphertext)]
    file_out.close()

    return image
