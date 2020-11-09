import base64
import io
from PIL import Image
from Cryptodome.Cipher import AES
# had to encode with utf8, was getting a some weird cant convert to c code error
key = b"letsgetthisbread"
cipher_e = AES.new(key, AES.MODE_EAX)
ciphertext, tag = cipher_e.encrypt_and_digest(b"hello")
n = cipher_e.nonce

key = b"letsgetthisbread"
cipher_d = AES.new(key, AES.MODE_EAX, n)
plaintext = cipher_d.decrypt_and_verify(ciphertext,tag)
print(plaintext)

"".encode("utf-8")