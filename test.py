from photocrypt.image import open_image
from photocrypt.crypto import imcrypto
from photocrypt.crypto.RSA import generate_key

pri, pub = generate_key()
image = open_image("samples/tuatara.jpg")
cim = imcrypto.encrypt_image(image, pub)
cim.save("enc.png")
print()
print(*cim.headers, sep="\n\n")
pim = imcrypto.decrypt_image(cim, pri)
pim.save("dec.png")
