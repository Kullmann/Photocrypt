# from photocrypt.image import open_image
# from photocrypt.crypto import imcrypto
# from photocrypt.crypto.RSA import generate_key

# pri, pub = generate_key()
# image = open_image("hi.png")
# cim = imcrypto.encrypt_image(image, pub)
# cim.save("enc.png")
# print()
# print(*cim.headers, sep="\n\n")
# pim = imcrypto.decrypt_image(cim, pri)
# pim.save("dec.png")

from photocrypt import encrypt_image, open_image, decrypt_image
from photocrypt.crypto.RSA import generate_key, load_key, load_keypair, save_key, save_keypair

private, public = load_keypair(("private.pem", "public.pem"))
eimg = decrypt_image(encrypt_image(open_image("samples/tuatara.jpg"), public), private)
eimg.save("test_samples/test.png")
