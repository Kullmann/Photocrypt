"""
Image Crypto module to encrypt/decrypt images
"""

from Cryptodome.Random import get_random_bytes
from photocrypt.crypto import AES
from photocrypt.crypto import RSA
from photocrypt.image import CryptoBitmap, Image, convert_image
from photocrypt.utils import packer

def encrypt_image(image: Image, public_key: bytes, *, aes_mode=AES.MODE_EAX) -> Image:
    """
    converts image to CryptoBitmap, then uses AES and RSA to encrypt image.
    """
    if not isinstance(image, CryptoBitmap):
        image = convert_image(image, CryptoBitmap)
    aes = AES.create(aes_mode, get_random_bytes(16))
    rsa = RSA.create(public_key)
    key_enc, _ = rsa.encrypt(aes.key)
    cdata, extra = aes.encrypt(image.data)
    image.data = cdata
    image.store_crypto_information(key_enc, *packer.unpack(extra))
    print(*image.headers, sep="\n")
    return image

def decrypt_image(image: Image, private_key: bytes, *, aes_mode=AES.MODE_EAX) -> Image:
    if not isinstance(image, CryptoBitmap):
        raise TypeError("decryption requires crypto image.")
    image = CryptoBitmap.from_bytes(image.to_bytes())
    key_enc, nonce, extra = packer.unpack(image.crypto_header.header[1])
    rsa = RSA.create(private_key)
    key, _ = rsa.decrypt(key_enc)
    aes_extra, decrypt_extra = packer.pack(nonce), packer.pack(extra)
    aes = AES.create(AES.MODE_EAX, key, aes_extra)
    pdata, _ = aes.decrypt(image.data, decrypt_extra)
    image.data = pdata
    return image
