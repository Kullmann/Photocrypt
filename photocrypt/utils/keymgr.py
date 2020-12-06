"""
    author: Hosung Lee
    date: December 7 2020

    Local key manager to manage public keys
"""
import sqlite3
from sqlite3 import Error, IntegrityError
from typing import List, Dict, Union

KEY_STORE_TABLE_NAME = 'keystore'
KEY_STORE_TABLE_SQL = f'''
    CREATE TABLE IF NOT EXISTS {KEY_STORE_TABLE_NAME} (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Name VARCHAR(50),
        Email VARCHAR(50),
        PublicKey BLOB UNIQUE
    )
'''

def conn_not_established():
    """
    Raise error that connection is not established.
    """
    raise Exception("connection not established. Call connect() method.")

def public_key_invalid():
    """
    Raise error that public key is invalid.
    """
    raise ValueError("public key is invalid.")

def name_length_invalid():
    """
    Raise error that name is invalid.
    """
    raise ValueError("name has to be longer than 0.")

class KeyManager:
    """
    Key manager class
    """
    def __init__(self, dbpath=":memory:"):
        self.dbpath = dbpath
        self.conn = None

    def connect(self):
        """
        Connect to keystore
        """
        try:
            self.conn = sqlite3.connect(self.dbpath)
            cursor = self.conn.cursor()
            cursor.execute(KEY_STORE_TABLE_SQL)
            self.conn.commit()
        except Error:
            print(Error)

    def list_key(self) -> List[Dict[str, Union[str, bytes]]]:
        """
        List all key in keystore
            Returns:
                list of dictionary[name, email, public_key]
        """
        if not self.conn:
            conn_not_established()

        cursor = self.conn.cursor()
        cursor.execute(f'SELECT * FROM {KEY_STORE_TABLE_NAME}')
        rows = cursor.fetchall()
        return [
            {'uid':i, 'name': name, 'email': email, 'public_key':public_key}
            for i, name, email, public_key
            in rows]

    def write_key(self, name: str, email: str, public_key: bytes) -> bool:
        """
        Write key to keystore

            Parameters:
                name (str): required, name of key holder
                email (str): not required, email of key holder
                public_key (bytes): required, public_key of key holder

            Returns:
                result (bool): True if successful, False if failed.
        """
        if not self.conn:
            conn_not_established()

        cursor = self.conn.cursor()
        if len(name) == 0:
            name_length_invalid()

        if len(public_key) == 0 or not isinstance(public_key, bytes):
            public_key_invalid()

        values = (name, email, public_key)

        try:
            cursor.execute(
                f'INSERT INTO {KEY_STORE_TABLE_NAME} (Name, Email, Publickey) VALUES(?, ?, ?)',
                values
                )

            self.conn.commit()

        except IntegrityError:
            return False
        return True

    def get_key(self, uid: int) -> bytes:
        """
        Get key by unique id

            Parameters:
                uid (int): required, unique id of key holder

            Returns
                public key (bytes): public key of key holder
        """
        if not self.conn:
            conn_not_established()

        cursor = self.conn.cursor()
        data = (uid, )

        cursor.execute(f'SELECT * FROM {KEY_STORE_TABLE_NAME} WHERE Id = ?', data)
        row = cursor.fetchone()
        if row:
            _, _, _, key = row
            return key

        return row

    def delete_key(self, uid: int) -> None:
        """
        Delete key by unique id

            Parameters:
                uid (int): required, unique id of key holder

            Returns
                public key (bytes): public key of key holder
        """
        if not self.conn:
            conn_not_established()

        cursor = self.conn.cursor()
        data = (uid, )

        cursor.execute(f'DELETE FROM {KEY_STORE_TABLE_NAME} WHERE Id = ?', data)
        self.conn.commit()

    def close(self):
        """
        Close connection to db
        """
        if self.conn:
            self.conn.close()

def create(keystore_path='keystore.db'):
    """
    Create key manager that controls specified keystore database.

        Parameters:
            keystore_path (str): path to keystore database.
                If there's no such file, key manager creates new one.

        Returns:
            key manager (KeyManager): key manager that controls keystore database.
    """
    keymgr = KeyManager(keystore_path)
    return keymgr
