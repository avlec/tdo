import unittest
import hashlib, binascii
from DatabaseManager import DatabaseManager


class TestDatabaseManager(unittest.TestCase):

    # dbm = None
    # test_user_data = None

    def setUp(self):
        self.dbm = DatabaseManager('postgres', 'mDmLfpPcTjwG7KJ4')
        self.test_user_data = ('alec',
                binascii.hexlify(hashlib.pbkdf2_hmac('sha256',b'aleciscool',b'0123456789abcdef', 10000)),
                '0123456789abcdef',
                '192.168.0.0')

    def tearDown(self):
        pass

    def test_write_user(self):
        self.dbm.write_user(self.test_user_data)
        self.dbm.cursor.execute('''SELECT * FROM USERS
                            WHERE name=%s AND passphrase=%s AND salt=%s AND ipaddress=%s''', self.test_user_data)
        self.assertEqual(self.test_user_data, self.dbm.cursor.fetchone()[1:])
        # remove entry
        self.dbm.cursor.execute('''DELETE FROM USERS USERS
                                            WHERE name=%s AND passphrase=%s AND salt=%s AND ipaddress=%s''',
                                self.test_user_data)
        self.dbm.connection.commit()

