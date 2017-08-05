import binascii
import hashlib
import unittest

from database.DatabaseManager import DatabaseManager


class TestDatabaseManager(unittest.TestCase):
    def setUp(self):
        self.dbm = DatabaseManager('api', 'password')
        hashed_pass = binascii.hexlify(hashlib.pbkdf2_hmac('sha256',b'aleciscool',b'0123456789abcdef', 10000))
        self.test_user_data = ('0123456789abcdef', 'alec', hashed_pass)
        self.test_message_data = ('0000000000000000','0000000000000000','0000000000000000', 'Hey Mom!', '1999-01-08 04:05:06')

    def tearDown(self):
        self.dbm = None

    def test_write_client(self):
        self.dbm.create_user(self.test_user_data)
        self.dbm.cursor.execute('''SELECT * FROM USERS
                            WHERE id=%s AND alias=%s AND pass=%s;''', self.test_user_data)
        self.assertEqual(self.test_user_data[1:], self.dbm.cursor.fetchone()[1:])
        self.dbm.connection.commit()
        # remove entry
        self.dbm.cursor.execute('''DELETE FROM USERS
                            WHERE id=%s AND alias=%s AND pass=%s;''', self.test_user_data)
        self.dbm.connection.commit()

    def test_write_message(self):
        self.dbm.create_message(self.test_message_data)
        self.dbm.cursor.execute('''SELECT * FROM MESSAGES
                                   WHERE id=%s AND senderid=%s AND channelid=%s AND message=%s''', self.test_message_data[:-1])
        self.dbm.connection.commit()
        # remove entry
        self.assertEqual(self.test_message_data[:-1], self.dbm.cursor.fetchone()[:-1])
        self.dbm.cursor.execute('''DELETE FROM MESSAGES
                                   WHERE id=%s AND senderid=%s AND channelid=%s AND message=%s''', self.test_message_data[:-1])
        self.dbm.connection.commit()
