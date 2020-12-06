"""
Image crypto module to encrypt/decrypt images
"""

from Cryptodome.Random import get_random_bytes
from photocrypt.crypto import AES
from photocrypt.crypto import RSA
from photocrypt.image import CryptoBitmap, Image, convert_image
from photocrypt import packer

def encrypt_image(image: Image, public_key: bytes, *, aes_mode=AES.MODE_EAX) -> Image:
    """
    converts image to CryptoBitmap, then uses AES and RSA to encrypt image.
    """
    # converts image to crypto-bitmap
    if not isinstance(image, CryptoBitmap):
        image = convert_image(image, CryptoBitmap)

    # encrypts image using AES, and encrypts key using RSA
    aes = AES.create(aes_mode, get_random_bytes(16))
    rsa = RSA.create(public_key)
    key_enc, _ = rsa.encrypt(aes.key)
    cdata, extra = aes.encrypt(image.data)
    image.data = cdata
    image.store_crypto_information(key_enc, *packer.unpack(extra))
    return image

def decrypt_image(image: Image, private_key: bytes, *, aes_mode=AES.MODE_EAX) -> Image:
    """
    Decrypts cryptoBitmap using AES and RSA.
    """
    # raise exception if image is not crypto-bitmap
    if not isinstance(image, CryptoBitmap):
        raise TypeError("decryption requires crypto image.")
    image = CryptoBitmap.from_bytes(image.to_bytes())
    unpacked = packer.unpack(image.crypto_header.header[1])
    if len(unpacked) < 3:
        raise ValueError("cannot unpack crypto information.")
    key_dec, nonce, extra = unpacked[0], unpacked[1], unpacked[2]
    rsa = RSA.create(private_key)
    key, _ = rsa.decrypt(key_dec)
    aes_extra, decrypt_extra = packer.pack(nonce), packer.pack(extra)
    aes = AES.create(aes_mode, key, aes_extra)
    pdata, _ = aes.decrypt(image.data, decrypt_extra)
    image.data = pdata
    return image
