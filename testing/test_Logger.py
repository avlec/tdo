import unittest
import os
from Logger import Logger


class TestLoggerMethods(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        try:
            os.remove('logfile.txt')
        except OSError:
            pass

    def test_creation(self):
        logger = Logger('log.txt')
        self.assertIsNotNone(logger)

    def test_recreation(self):
        logger1 = Logger('x.txt')
        logger2 = Logger('y.txt')
        # instances are the same but references can be created and thrown away
        self.assertEqual(logger1.instance, logger2.instance)

    def test_log_write(self):
        logger = Logger('logfile.txt')
        logger.instance.write_path = 'logfile.txt'
        logger.log('Writing Log', 'Notification')
        expected_format = 'Notification: Writing Log'
        with open('logfile.txt') as logfile:
            self.assertEqual(expected_format, logfile.read())


if __name__ == '__main__':
    unittest.main()
