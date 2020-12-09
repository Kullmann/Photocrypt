"""
Tests photocrypt module for image encryption and decryption
"""

import unittest
from photocrypt import encrypt_image, open_image, decrypt_image
from photocrypt.crypto.RSA import generate_key, save_keypair, load_key

class TestKeyManager(unittest.TestCase):
    """
    Tests image encryption and decryption
    """
    def test_rsa(self):
        """
        Tests RSA
        """
        private, public = generate_key()
        self.assertEqual(isinstance(private, bytes), True)
        self.assertEqual(isinstance(public, bytes), True)
        save_keypair((private, public), ("private.pem","public.pem"))


    def test_encryption(self):
        """
        Tests image encryption
        """
        public = load_key("public.pem")
        eimg = encrypt_image(open_image("samples/tuatara.jpg"), public)
        eimg.save("samples/tuatara_ecb.jpg")

    def test_decryption(self):
        """
        Tests image decryption
        """
        private = load_key("private.pem")
        dimg = decrypt_image(open_image("samples/tuatara_ecb.jpg"), private)
        with self.assertRaises(ValueError):
            decrypt_image(open_image("samples/tuatara.jpg"), private)
        dimg.save("samples/tuatara_dcb.jpg")

if __name__ == '__main__':
    unittest.main()
