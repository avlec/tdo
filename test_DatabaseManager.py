import unittest
import hashlib, binascii
from DatabaseManager import DatabaseManager


class TestDatabaseManager(unittest.TestCase):

    # dbm = None
    # test_user_data = None

    def setUp(self):
        self.dbm = DatabaseManager('postgres', 'mDmLfpPcTjwG7KJ4')
        self.test_user_data = (
                '0123456789abcdef',
                'alec',
                binascii.hexlify(hashlib.pbkdf2_hmac('sha256',b'aleciscool',b'0123456789abcdef', 10000)) )

    def tearDown(self):
        pass

    def test_write_user(self):
        self.dbm.write_user(self.test_user_data)
        self.dbm.cursor.execute('''SELECT * FROM USERS
                            WHERE salt=%s AND alias=%s AND passphrase=%s;''', self.test_user_data)
        self.assertEqual(self.test_user_data[1:], self.dbm.cursor.fetchone()[1:])
        # remove entry
        self.dbm.cursor.execute('''DELETE FROM USERS
                            WHERE salt=%s AND alias=%s AND passphrase=%s;''', self.test_user_data)
        self.dbm.connection.commit()

