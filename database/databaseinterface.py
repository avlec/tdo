import re
from database.DatabaseManager import DatabaseManager as DatabaseManager


# methods return error messages if they did not complete action, none if successful
class databaseinterface:

    def __init__(self):
        self.dbmanager = DatabaseManager('api','password')

    def getChannels(self):
        """
        :return: List of all channels
        """
        return self.dbmanager.lookupChannels()

    def getUsers(self):
        """
        :return: List of all users
        """
        return self.dbmanager.lookupUsers()

    def newUser(self, user):
        """
        Adds a user to the database
        :param user: User object
        :return: None
        """
        self.dbmanager.createUser( (user.id, user.alias, user.password) )

    def changeUser(self, userid, user):
        """
        Updates the user in the database at user ID to be user
        Basically removes then re adds
        :param userid: Id of user being updated
        :param user: User object
        :return: None
        """
        self.dbmanager.updateUser(userid, user.name, user.password)

    def getUser(self, userid):
        """
        Returns the information to create a user object from what was stored in the database
        :param userid: Id of user being looked up
        :return: User object
        """
        (id, alias, password) = self.dbmanager.lookupUser(userid)
        return (alias, id, None, None)

    def getUserAlias(self, alias):
        """
        returns user with alias==alias, none if not found
        :param alias: Alias of user being looked up
        :return: User object
        """
        x = self.dbmanager.lookupUser(alias, "alias")
        if not x:
            return None
        (id, alias, password) = x
        return (alias, id, None, None)

    def newChannel(self, channel):
        """
        Adds a channel object to the database
        :param channel: Channel object
        :return:
        """
        self.dbmanager.createChannel((channel.id, channel.name, channel.permisions))

    def getChannel(self, channel):
        """
        Retrieve information from the database and create a channel object
        :param channel:
        :return:
        """
        (id, name, permissions, blocked_users) = self.dbmanager.lookupChannel(channel)
        return (name, permissions, id, blocked_users)

    def change_default_permisions(self, channel, permissions):
        regex = re.match(r'([01]{3})',permissions)
        if regex:
            self.dbmanager.updateChannelPermissions(channel.id, permissions)
            # change permision in channel with given id


    def blockUser(self, channel, user):
        """
        Blocks a given user from a given channel
        :param channel: Channel object
        :param user: User object
        :return: None
        """
        self.dbmanager.appendBlockedChannel(channel.id, user.id)

    def UnblockUser(self, channel,user):
        """
        Unblocks a given user from a given channel
        :param channel: Channel object
        :param user: User object
        :return: None
        """
        self.dbmanager.removeBlockedUser(channel.id, user.id)