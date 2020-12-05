"""
    author: Sean Kullman, Hosung Lee
    date: December 4 2020

    AES class
"""

class Cipher:
    def __init__(self, cipher):
        self.cipher = cipher

class AESCipher(Cipher):
    def __init__(self, mode, key):
        self.mode = mode
        self.key = key
        cipher = AES
        super().__init__(cipher)