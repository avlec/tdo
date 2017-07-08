import unittest
from Logger import Logger

class TestLoggerMethods(unittest.TestCase):

    def test_creation(self):
        logger = Logger('log.txt')
        self.assertIsNotNone(logger)

    def test_recreation(self):
        logger1 = Logger('x.txt')
        logger2 = Logger('y.txt')
        # instances are the same but references can be created and thrown away
        self.assertEqual(logger2.instance, logger2.instance)

    def test_logwrite(self):
        pass


if __name__ == '__main__':
    unittest.main()