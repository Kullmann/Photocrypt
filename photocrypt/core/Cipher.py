"""
    author: Hosung Lee
    date: December 4 2020

    Abstract Cipher class
"""
from abc import ABC, abstractmethod
from typing import Optional, List

class Cipher(ABC):
    """
    Cipher class
    """

    @abstractmethod
    def encrypt(self, data: bytes, extra: Optional[List[bytes]] = None) -> bytes:
        """
        encrypts bytes

            Parameters:
                data (bytes): data to encrypt
                extra (Optional[List[bytes]]): optional data required for encryption

            Return:
                encrypted (bytes): encrypted data
                extra (Optional[bytes]): packed bytes for extra
                                            (packed using photocrypt.util.packer).
        """
        ...

    @abstractmethod
    def decrypt(self, data: bytes, extra: Optional[List[bytes]] = None) -> bytes:
        """
        decrypts bytes

            Parameters:
                data (bytes): data to decrypt
                extra (Optional[List[bytes]]): optional data required for decryption

            Return:
                decrypted (bytes): encrypted data
                extra (Optional[bytes]): packed bytes for extra
                                            (packed using photocrypt.util.packer).
        """
        ...
