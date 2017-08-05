import re
import psycopg2
from database.DatabaseManager import DatabaseManager as DatabaseManager


# methods return error messages if they did not complete action, none if successful
class databaseinterface:

    def __init__(self):
        self.dbmanager = DatabaseManager('api','password')

    # Create Methods

    def new_user(self, user):
        """
        Adds a user to the database if the user isn't already
        In the database.
        :param user: User object
        :return: None
        """
        try:
            self.dbmanager.create_user((user.id, user.alias, user.password))
        except psycopg2.IntegrityError:
            print("Error duplicate channel found, ignoring.")

    def new_channel(self, channel):
        """
        Adds a channel object to the database
        :param channel: Channel object
        :return:
        """
        try:
            self.dbmanager.create_channel((channel.id, channel.name, channel.permisions))
        except psycopg2.IntegrityError:
            print("Error duplicate channel found, ignoring.")

    # Fetch Methods

    def get_channels(self):
        """
        :return: List of all channels
        """
        return self.dbmanager.lookup_channels()

    def get_users(self):
        """
        :return: List of all users
        """
        return self.dbmanager.lookup_users()

    def get_user_from_id(self, userid):
        """
        Returns the information to create a user object from what was stored in the database
        :param userid: Id of user being looked up
        :return: User object
        """
        (id, alias, password) = self.dbmanager.lookup_user(userid)
        return (alias, id, None, None)

    def get_user_from_alias(self, alias):
        """
        returns user with alias==alias, none if not found
        :param alias: Alias of user being looked up
        :return: User object
        """
        x = None
        try:
            x = self.dbmanager.lookup_user(alias, "alias")
        except psycopg2.InternalError:
            pass

        if not x:
            return None
        (id, alias, password) = x
        return (alias, id, None, None)

    def get_channel_from_id(self, channel):
        """
        Retrieve information from the database and create a channel object
        :param channel:
        :return:
        """
        temp = None
        try:
            temp = self.dbmanager.lookup_channel(channel.id)
        except psycopg2.InternalError:
            pass

        if temp is None:
            return None
        (id, name, permissions, blocked_users) = temp
        return (id, name, permissions, blocked_users)


    def get_channel_from_name(self, channelname):
        """
        Returns a channel given a name
        :param channel:
        :return:
        """
        (id, name, permissions, blocked_users) = self.dbmanager.lookup_channel(channelname, "name")
        return (name, permissions, id, blocked_users)

    # Modification Methods

    def change_user(self, userid, user):
        """
        Updates the user in the database at user ID to be user
        Basically removes then re adds
        :param userid: Id of user being updated
        :param user: User object
        :return: None
        """
        self.dbmanager.update_user(userid, user.name, user.password)

    def change_default_permisions(self, channel, permissions):
        regex = re.match(r'([01]{3})',permissions)
        if regex:
            self.dbmanager.update_channel_permissions(channel.id, permissions)
            # change permision in channel with given id

    def block_user(self, channel, user):
        """
        Blocks a given user from a given channel
        :param channel: Channel object
        :param user: User object
        :return: None
        """
        self.dbmanager.append_blocked_user_to_channel(channel.id, user.id)

    def unblock_user(self, channel, user):
        """
        Unblocks a given user from a given channel
        :param channel: Channel object
        :param user: User object
        :return: None
        """
        self.dbmanager.remove_blocked_user_from_channel(channel.id, user.id)

    # Deletion Methods

    def delete_user(self, user):
        try:
            self.dbmanager.delete_user(user.id, user.alias)
        except psycopg2.IntegrityError:
            print("Error user not found when deleting channel, ignoring.")

    def delete_channel(self, channel):
        try:
            self.dbmanager.delete_channel(channel.id, channel.name)
        except psycopg2.IntegrityError:
            print("Error channel not found when deleting channel, ignoring.")