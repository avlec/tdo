from messages.MessageEncoding import MessageEncoder, MessageDecoder


class Message:
    def __init__(self, messageId, messageSenderId, senderAlias, messageChannelId, message, messageType):
        self.messageId = messageId
        self.messageSenderId = messageSenderId
        self.senderAlias = senderAlias
        self.messageChannelId = messageChannelId
        self.message = message
        self.messageType = messageType
        self.validate()

    # someone do this
    def validate(self):
        pass


    def encode(self):
        """Used to encode a Message to a json string."""
        return MessageEncoder().encode(self)

    @staticmethod
    def decode(message):
        """ This method is used to convert an input json string (message) to a Message object."""
        return MessageDecoder().decode(message)