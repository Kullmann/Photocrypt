"""
Driver of the photocrypt package
"""

from photocrypt.image import open_image, Image
from photocrypt.imcrypto import encrypt_image, decrypt_image
from photocrypt.crypto.RSA import generate_key
class Photocrypt:
    """
    provides image crypto feature
    """
    def __init__(self):
        # initializes Photocrypt
        self.current_recipient = None
        self.private_key = None
        self.keypath = None

    def encrypt(self, path: str) -> Image:
        """
        Encrypts photo in specified path.

            Parameters:
                path (str): path of image
        """
        if not self.current_recipient:
            raise ValueError("no recipient is selected.")
        image = open_image(path)
        return encrypt_image(image, self.current_recipient)

    def decrypt(self, path: str) -> Image:
        """
        Encrypts photo in specified path.

            Parameters:
                path (str): path of image
        """
        if not self.private_key:
            raise ValueError("private key not loaded.")
        image = open_image(path)
        return decrypt_image(image, self.private_key)

    @staticmethod
    def generate_key():
        """
        Generates key
        """
        private, public = generate_key()


    @staticmethod
    def new():
        """
        Encrypts photo in specified path.

            Parameters:
                path (str): 
        """
        pass
