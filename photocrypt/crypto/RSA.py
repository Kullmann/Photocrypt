"""
    author: Sean Kullmann
    date: December 7 2020

    provides RSA cipher and generate key feature
"""
from typing import Optional, List, Tuple
from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_OAEP
from photocrypt.core import Cipher, packer


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
                                            (packed using photocrypt.pack).

            Return:
                encrypted (bytes): encrypted data
                extra (Optional[bytes]): packed bytes for extra
                                            (packed using photocrypt.pack).
        """
        return self._rsa.encrypt(data), packer.pack(b'')

    def decrypt(self, data: bytes, extra: Optional[bytes] = None) -> List[bytes]:
        """
        decrypts bytes

            Parameters:
                data (bytes): data to decrypt using AES
                extra (Optional[bytes]): packed bytes for extra
                                            (packed using photocrypt.pack).

            Return:
                decrypted (bytes): encrypted data
                extra (Optional[bytes]): packed bytes for extra
                                            (packed using photocrypt.pack).
        """
        return self._rsa.decrypt(data), packer.pack(b'')


def generate_key(key_size: int = 2048) -> (bytes, bytes):
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


def save_key(key: bytes, file_path: str) -> None:
    """
    saves single RSA key to given file path.
    Use save_keypair() to save both private and public key at once.

        Parameters:
            key (bytes): byte representation of key (private/public)
            file_path (str): file path to save key.
    """
    with open(file_path, "wb") as file:
        file.write(key)


def load_key(file_path: str) -> bytes:
    """
    loads single RSA key from given file path.
    Use load_keypair() to load both private and public key at once.

    Parameters:
        file_path (str): file path to load key.
    """
    with open(file_path, "rb") as file:
        key = file.read()
    return key


def save_keypair(keypair: Tuple[bytes, bytes], file_paths: Tuple[str, str]) -> None:
    """
    saves RSA keypair to given file path.
    Use save_key() to save a single key.

        Parameters:
            keypair (tuple of bytes): byte representations of keys in tuple (private, public)
            file_path (tuple of str): file paths in pair to save keyspairs.
    """
    if len(keypair) != 2 or len(file_paths) != 2:
        raise ValueError("The tuple has to be size of 2")

    for key, file_path in zip(keypair, file_paths):
        save_key(key, file_path)


def load_keypair(file_paths: Tuple[str, str]) -> Tuple[bytes, bytes]:
    """
    loads RSA keypair from given file path.
    Use load_key() to load a single key.

        Parameters:
            keypair (tuple of bytes): byte representations of keys in tuple (private, public)
            file_path (tuple of str): file paths in pair to save keyspairs.
    """
    if len(file_paths) != 2:
        raise ValueError("The tuple has to be size of 2")

    return (load_key(file_paths[0]), load_key(file_paths[1]))


def create(key: bytes):
    """
    creates RSA Cipher

        Parameters:
            key (bytes): key for cipher
    """
    return RSACipher(key)
