from messages.MessageEncoding import MessageEncoder, MessageDecoder


class Message:
    def __init__(self, data):
        self.data = data
        inputList = data.decode().split('|')
        self.messageId = inputList[0]
        self.messageSenderId = inputList[1]
        self.senderAlias = inputList[2]
        self.messageChannelId = inputList[3]
        self.message = inputList[4]
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

    # pack class used to send a message in this format
    @staticmethod
    def pack(messageId ,messageSenderId ,senderAlias, messageChannelId, message):
        """Deprecated, instead instantiate Message object, then use its member function encode()."""
        return messageId + '|' + messageSenderId + '|' + senderAlias + '|' + messageChannelId + '|' + message

    def packmessage(self):
        """Deprecated, instead use member fuction encode()."""
        return self.messageId + '|' + self.messageSenderId + '|' + self.senderAlias + '|' + self.messageChannelId + '|' + self.message

