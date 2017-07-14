import unittest

from CommonUtil import *
from messages.MessageEncoding import *


class MessageEncodingTester(unittest.TestCase):

    def test_encode_then_decode(self):
        msg = Message("0000000000000000", "0000000000000000", "server", "0000000000000000", "Hello world")
        dec = MessageDecoder().decode(msg.pack())
        #self.assertDictEqual(msg.__dict__, dec.__dict__)
