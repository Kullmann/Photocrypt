from Crypto.Cipher import AES
key = "letsgetthisbread".encode("utf8")
cipher = AES.new(key, AES.MODE_EAX)
print(cipher)

with open("../samples/marbles.bmp", "rb") as f:
    clear = f.read()
    clear_trimmed = clear[64:-2]
    ciphertext = cipher.encrypt(clear_trimmed)
    ciphertext = clear[0:64] + ciphertext + clear[-2:]

with open("../samples/marbles_ecb.bmp", "wb") as f:
    f.write(ciphertext)

cipher_d = AES.new(key, AES.MODE_EAX, cipher.nonce)
with open("../samples/marbles_ecb.bmp", "rb") as f:
    clear = f.read()
    print(clear)
    clear_trimmed = clear[64:-2]
    plaintext = cipher_d.decrypt(clear_trimmed)
    plaintext = clear[0:64] + plaintext + clear[-2:]

with open("../samples/marbles_dcb.bmp", "wb") as f:
    f.write(plaintext)