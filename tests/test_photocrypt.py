"""
Tests photocrypt module for image encryption and decryption
"""
from photocrypt import encrypt_image, open_image, decrypt_image
from photocrypt.crypto.RSA import generate_key

if __name__ == '__main__':
    n_pass = 0
    n_fail = 0

    print("generating RSA key...")
    try:
        private, public = generate_key()
        print("pass")
        n_pass += 1
        
    except Exception as e:
        print("fail")
        print(e)
        n_fail += 1
    print("encrypting image...")
    try:
        eimg = encrypt_image(open_image("samples/tuatara.jpg"), public)
        eimg.save("samples/tuatara_ecb.jpg")
        print("pass")
        n_pass += 1

    except Exception as e:
        print("fail")
        print(e)
        n_fail += 1
    try:
        print("decrypting image...")
        eimg = decrypt_image(open_image("samples/tuatara_ecb.jpg"), private)
        eimg.save("samples/tuatara_dcb.jpg")
        print("pass")
        n_pass += 1

    except Exception as e:
        print("fail")
        print(e)
        n_fail += 1

    print(f"passed: {n_pass} / {n_fail + n_pass}")
