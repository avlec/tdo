import unittest

from messages.MessageEncoding import MessageDecoder, MessageEncoder
from messages.Message import Message as Message


class MessageEncodingTester(unittest.TestCase):

    def test_encode_then_decode(self):
        msg = Message(Message.pack("0000000000000000","0000000000000000","server","0000000000000000","Hello world."))
        enc = msg.encode()
        # dec = Message.decode(enc)
        # self.assertDictEqual(msg.__dict__, dec.__dict__)
