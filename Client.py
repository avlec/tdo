import random
import threading
import socket
import sys
import select

# format: message id|message sender id|message channel id|message
# ids are 10 digits, message is limited to 256 characters
# sample: 0000000000|0000000000|0000000000|Hello world


class Client:
    def __init__(self):
        self.id = None
        self.currentChannel = None

    # def chat_client(self):
    #
    #


if __name__ == "__main__":
    sys.exit(0)
    # see CL2, will port here soon
