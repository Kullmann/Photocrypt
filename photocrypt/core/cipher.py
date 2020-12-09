"""
    author: Hosung Lee
    date: December 7 2020

    Abstract Cipher class is a base class of all ciphers used within photocrypt package.
"""
from abc import ABC, abstractmethod
from typing import Optional, List

class Cipher(ABC):
    """
    Abstract cipher class
    """

    @abstractmethod
    def encrypt(self, data: bytes, extra: Optional[List[bytes]] = None) -> (bytes, bytes):
        """
        encrypts bytes

            Parameters:
                data (bytes): data to encrypt
                extra (Optional[List[bytes]]): optional data required for encryption

            Return:
                encrypted (bytes): encrypted data
                extra (Optional[bytes]): packed bytes for extra
                                            (packed using photocrypt.pack).
        """
        ...

    @abstractmethod
    def decrypt(self, data: bytes, extra: Optional[List[bytes]] = None) -> (bytes, bytes):
        """
        decrypts bytes

            Parameters:
                data (bytes): data to decrypt
                extra (Optional[List[bytes]]): optional data required for decryption

            Return:
                decrypted (bytes): encrypted data
                extra (Optional[bytes]): packed bytes for extra
                                            (packed using photocrypt.pack).
        """
        ...
