import unittest
from messages.Message import Message as Message


class MessageEncodingTester(unittest.TestCase):

    def test_encode_then_decode(self):
        msg = Message('0000000000000000', '0000000000000000', 'server', 'Hello')
        enc = msg.encode()
        dec = Message.decode(enc)
        self.assertDictEqual(msg.__dict__, dec.__dict__)
