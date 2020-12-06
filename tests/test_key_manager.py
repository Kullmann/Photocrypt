"""
Tests photocrypt.utils.keymgr module for image encryption and decryption
"""
import unittest
from photocrypt.utils import keymgr

class TestKeyManager(unittest.TestCase):
    """
    Tests photocrypt.utils.keymgr
    """
    def test_write_key(self):
        """
        Tests write key
        """
        key_mgr = keymgr.create(":memory:")
        key_mgr.connect()
        self.assertEqual(key_mgr.write_key('hello', 'email', b'hello'), True)
        self.assertEqual(key_mgr.write_key('hello', 'email', b'hello'), False)
        with self.assertRaises(ValueError):
            key_mgr.write_key('', 'email', b'hello')
        key_mgr.close()

    def test_list_key(self):
        """
        Tests read key
        """
        key_mgr = keymgr.create(":memory:")
        key_mgr.connect()
        key_mgr.write_key('hello', 'email', b'hello')
        self.assertEqual(
            key_mgr.list_key(), 
            [{'uid': 1, 'name': 'hello', 'email': 'email', 'public_key': b'hello'}]
            )
        key_mgr.close()

    def test_delete_key(self):
        """
        Tests delete key
        """
        key_mgr = keymgr.create(":memory:")
        key_mgr.connect()
        key_mgr.write_key('hello', 'email', b'hello')
        uid = key_mgr.list_key()[0]['uid']
        key_mgr.delete_key(uid)
        self.assertEqual(len(key_mgr.list_key()), 0)
        key_mgr.close()
    
    def test_get_key(self):
        """
        Tests get key
        """
        key_mgr = keymgr.create(":memory:")
        key_mgr.connect()
        key_mgr.write_key('hello', 'email', b'hello')
        uid = key_mgr.list_key()[0]['uid']
        self.assertEqual(key_mgr.get_key(uid), b'hello')
        key_mgr.close()

if __name__ == '__main__':
    unittest.main()
