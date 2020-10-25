# Need to add encrypting AES key with RSA, and passing key to decrypt
# function, also need to generate entropy to randomly generate key

import base64
from Crypto.Cipher import AES
# had to encode with utf8, was getting a some weird cant convert to c code error
key = "letsgetthisbread".encode("utf8")
cipher_e = AES.new(key, AES.MODE_EAX)

def encrypt(image):
    image_trimmed = image[64:-2]
    ciphertext = cipher_e.encrypt(image_trimmed)
    ciphertext = image[0:64] + ciphertext + image[-2:]
    return ciphertext
    