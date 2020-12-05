"""
    author: Sean Kullman, Hosung Lee
    date: December 4 2020

    AES class
"""
from abc import abstractmethod
from typing import Optional, List
from Cryptodome.Cipher import AES
from Cryptodome.Cipher.AES import MODE_CCM, MODE_EAX, MODE_GCM, MODE_SIV, MODE_OCB
from photocrypt.core import Cipher
from photocrypt.utils import packer

class AESCipher(Cipher):
    """
    Abstract AES Cipher class
    """
    def __init__(self, mode, key: bytes):
        self._mode = mode
        self._key = key
    
    @property
    def mode(self):
        """
        getter method of mode
        """
        return self._mode


    @property
    def key(self):
        """
        getter method of key
        """
        return self._key

    @abstractmethod
    def encrypt(self, data: bytes, extra: Optional[bytes] = None) -> List[bytes]:
        """
        encrypts bytes

            Parameters:
                data (bytes): data to encrypt using AES
                extra (Optional[bytes]): optional data required for encryption

            Return:
                encrypted (bytes): encrypted data
                extra (bytes): extra data produced from decryption
        """
        ...

    @abstractmethod
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
        ...

class AESCipherModern(AESCipher):
    """
    AES Cipher class
    """
    def __init__(self, mode: int, key: bytes, extra: Optional[bytes] = None):
        extra = packer.unpack(extra) if extra else []
        _nonce = None
        if len(extra) > 0:
            _nonce = extra[0]
        self.aes = AES.new(key, mode, nonce=_nonce)
        self._nonce = _nonce
        super().__init__(mode, key)

    def encrypt(self, data: bytes, extra: Optional[bytes] = None) -> List[bytes]:
        """
        encrypts bytes

            Parameters:
                data (bytes): data to encrypt using AES
                extra (Optional[bytes]): packed bytes for extra
                            (packed using photocrypt.util.packer).

            Return:
                encrypted (bytes): encrypted data
                extra (bytes): packed bytes of nonce and tag
                            (packed using photocrypt.util.packer).
        """

        nonce = self._nonce if self.mode == MODE_SIV else self.aes.nonce
        ciphertext, tag = self.aes.encrypt_and_digest(data)
        return ciphertext, packer.pack(nonce, tag)

    def decrypt(self, data: bytes, extra: Optional[bytes] = None) -> List[bytes]:
        """
        decrypts bytes

            Parameters:
                data (bytes): data to decrypt using AES
                extra (Optional[bytes]): packed bytes for extra
                            (packed using photocrypt.util.packer).

            Return:
                decrypted (bytes): encrypted data
                extra: packed bytes for extra
                            (packed using photocrypt.util.packer).
        """
        tag = packer.unpack(extra)[0]
        return self.aes.decrypt_and_verify(data, tag), packer.pack(b'')

# supported modes
_supported_modes = {
    MODE_CCM: AESCipherModern,
    MODE_EAX: AESCipherModern,
    MODE_GCM: AESCipherModern,
    MODE_SIV: AESCipherModern,
    MODE_OCB: AESCipherModern
}

def _get_aes(mode, key, extra: Optional[bytes] = None):
    """
    Factory of AES Ciphers
    """
    if not mode in _supported_modes:
        raise ValueError("The mode is not supported.")

    return _supported_modes[mode](mode, key, extra)

def create(mode, key, extra: Optional[bytes] = None):
    """
    Creates AES Cipher

        Parameters:
            mode (constant): mode of AES
            key (bytes): key for cipher
            extra (bytes): packed bytes for extra (packed using photocrypt.util.packer).
    """
    return _get_aes(mode, key, extra)
