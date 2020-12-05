"""
    author: Sean Kullman, Hosung Lee
    date: December 4 2020

    rsa class
"""
from typing import Optional, List
from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_OAEP
from photocrypt.utils import packer
from photocrypt.core import Cipher

class RSACipher(Cipher):
    """
    Abstract RSA Cipher class
    """
    def __init__(self, key: bytes):
        self._key = RSA.import_key(key)
        self._rsa = PKCS1_OAEP.new(self._key)

    @property
    def key(self):
        """
        getter method of key
        """
        return self._key

    def encrypt(self, data: bytes, extra: Optional[bytes] = None) -> List[bytes]:
        """
        encrypts bytes

            Parameters:
                data (bytes): data to encrypt using AES
                extra (Optional[bytes]): packed bytes for extra
                                            (packed using photocrypt.util.packer).

            Return:
                encrypted (bytes): encrypted data
                extra (Optional[bytes]): packed bytes for extra
                                            (packed using photocrypt.util.packer).
        """
        return self._rsa.encrypt(data), packer.pack(b'')

    def decrypt(self, data: bytes, extra: Optional[bytes] = None) -> List[bytes]:
        """
        decrypts bytes

            Parameters:
                data (bytes): data to decrypt using AES
                extra (Optional[bytes]): packed bytes for extra
                                            (packed using photocrypt.util.packer).

            Return:
                decrypted (bytes): encrypted data
                extra (Optional[bytes]): packed bytes for extra
                                            (packed using photocrypt.util.packer).
        """
        return self._rsa.decrypt(data), packer.pack(b'')

def generate_key(key_size: int = 2048):
    """
    generates RSA private and public key

            Parameters:
                key_size (int): key size of rsa

            Return:
                private key (bytes): rsa private key
                public key (bytes): rsa public key
    """
    key = RSA.generate(key_size)
    return key.export_key(), key.publickey().export_key()

def create(key: bytes):
    """
    Creates AES Cipher

        Parameters:
            mode (constant): mode of AES
            key (bytes): key for cipher
            extra (bytes): packed bytes for extra (packed using photocrypt.util.packer).
    """
    return RSACipher(key)
