import Connector
import random
import threading
import socket
import sys

# format: message id|message sender id|message channel id|message
# ids are 10 digits, message is limited to 256 characters
# sample: 0000000000|0000000000|0000000000|Hello world
class Client:
    def __init__(self):
        self.id = Connector.createID()
        self.currentChannel = Connector.createID()


if __name__ == "__main__":
    #see CL2, will port here soon