import binascii
import hashlib
import unittest

from database.DatabaseManager import DatabaseManager


class TestDatabaseManager(unittest.TestCase):
    def setUp(self):
        self.dbm = DatabaseManager('api', 'password')
        hashed_pass = binascii.hexlify(hashlib.pbkdf2_hmac('sha256',b'aleciscool',b'0123456789abcdef', 10000))
        self.test_user_data = ('0123456789abcdef', 'alec', hashed_pass)

    def tearDown(self):
        pass

    def test_write_user(self):
        self.dbm.write_user(self.test_user_data)
        self.dbm.cursor.execute('''SELECT * FROM USERS
                            WHERE salt=%s AND alias=%s AND pass=%s;''', self.test_user_data)
        self.assertEqual(self.test_user_data[1:], self.dbm.cursor.fetchone()[1:])
        # remove entry
        self.dbm.cursor.execute('''DELETE FROM USERS
                            WHERE salt=%s AND alias=%s AND pass=%s;''', self.test_user_data)
        self.dbm.connection.commit()

