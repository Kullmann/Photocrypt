# Need top get key with from encrypt function, and then decrypt
# with RSA first, and then AES key
from Crypto.Cipher import AES
key = "letsgetthisbread".encode("utf8")
cipher_d = AES.new(key, AES.MODE_EAX)

def decrypt(image):
    image_trimmed = image[64:-2]
    plaintext = cipher_d.decrypt(image_trimmed)
    plaintext = image[0:64] + plaintext + image[-2:]
    return image