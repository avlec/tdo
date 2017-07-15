# from Queue import *


# TODO design and implement
class MessageHandler:

    message_sender = None
    message_receiver = None
    message_processor = None

    def __init__(self):
        message_sender = MessageSender()
        message_receiver = MessageReceiver()
        message_processor = MessageProcessor()

    def run(self):
        pass


# TODO design and implement
class MessageProcessor:

    process_queue = None

    def __init__(self):
        pass

    def run(self):
        pass


# TODO design and implement
class MessageSender:

    outbound_queue = None

    def __init__(self):
        pass

    def run(self):
        pass


# TODO design and implement
class MessageReceiver:

    inbound_queue = None

    def __init__(self):
        pass

    def run(self):
        pass
