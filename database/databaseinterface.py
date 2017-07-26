import re
#methods return error messages if they did not complete action, none if successful
class databaseinterface:

    @staticmethod
    def newUser(user):
        pass  # adds user to db, returns error msg if duplicate

    @staticmethod
    def changeUser(userid, user):
        pass  # updates user in db at userid to be user

    @staticmethod
    def getUser(userid):
        pass  # returns user object with given id

    @staticmethod
    def getUserAlias(alias):
        pass  # returns user with alias==alias, none if not found

    @staticmethod
    def userHasPermisions(channel, user, permisions):
        pass  # checks if user has  permissions

    @staticmethod
    def addUser(channel,user):
        pass #adds user to channel with default channel permissions

    @staticmethod
    def removeUser(channel,user):
        pass#removes user from channel

    @staticmethod
    def newChannel(channel):
        pass#takes channel object, adds to DB
    @staticmethod
    def getChannel(channel):
        pass #  returns channel class

    @staticmethod
    def changeChannel(channelid,channel):
        pass  # updates user in db at @channelid to be @channel

    @staticmethod
    def change_default_permisions(channel, permissions):
        regex = re.match(r'([01]{3})',permissions)
        if regex:
            pass  # change permision in channel with given id

    @staticmethod
    def SetChannelPermisions(channel, user, permissions):
        if re.match(r'([01]{3})',permissions):
            if user:
                pass# sets channel permisions for @user in @channel
            else:
                pass  # sets channel wide default permissions

    @staticmethod
    def blockUser(channel,user):
        pass #blocks user in given channel

    @staticmethod
    def UnblockUser(channel,user):
        pass#unblocks user in given channel