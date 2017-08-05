import psycopg2


# Singleton Pattern Found Here:
# https://stackoverflow.com/a/6798042
class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


# Class used to manage interactions between the database and server
class DatabaseManager:
    __metaclass__ = Singleton
    connection = None
    cursor = None

    def __init__(self, user, password):
        self.connection = psycopg2.connect("dbname=tdo host='localhost' user=%s password=%s" % (user, password))
        self.cursor = self.connection.cursor()

    # Lookup Commands
    def lookup_user(self, identifier, column="id"):
        """
        Returns a specific user given an identifier and column (defaults to id)
        :param identifier: Information by which the database is being indexed (default id)
        :param column: Column in the database (id/name) defaults to id
        :return: User found in database otherwise None
        """
        if column is "id":
            self.cursor.execute('''SELECT * FROM tdo.public.users
                                            WHERE id=%s;''', (identifier,))
        elif column is "alias":
            self.cursor.execute('''SELECT * FROM tdo.public.users
                                            WHERE alias=%s;''', (identifier,))

        return self.cursor.fetchone()

    def lookup_users(self):
        """
        Returns a list of all users stored in the database
        :return: List of all known users
        """
        self.cursor.execute('''SELECT * FROM tdo.public.users;''')
        return self.cursor.fetchall()

    def lookup_channel(self, identifier, column="id"):
        """
        Searches through the database for a channel
        :param identifier: Information by which the database is being indexed (default id)
        :param column: Column in the database (id/name) defaults to id
        :return: Channel found in the database otherwise None
        """
        if column is "id":
            self.cursor.execute('''SELECT * FROM tdo.public.channels
                                            WHERE id=%s;''', (identifier,))
        elif column is "name":
            self.cursor.execute('''SELECT * FROM tdo.public.channels
                                            WHERE name=%s;''', (identifier,))
        return self.cursor.fetchone()

    def lookup_channels(self):
        """
        Retrieves a list of all channels currently in the database.
        :return: List of channels in the database otherwise None
        """
        self.cursor.execute('''SELECT * FROM tdo.public.channels;''')
        return self.cursor.fetchall()

    def lookup_message(self, identifier, column="id"):
        """
        Searches through the database for a message
        :param identifier: Information bny which the database is being indexed (default id)
        :param column: Column in the database (id/senderid/channelid/message/time) defaults to id
        :return: Message found in the database otherwise None
        """
        if column is "id":
            self.cursor.execute('''SELECT * FROM tdo.public.messages
                                            WHERE id=%s;''', (identifier,))
        elif column is "senderid":
            self.cursor.execute('''SELECT * FROM tdo.public.messages
                                            WHERE senderid=%s;''', (identifier,))
        elif column is "channelid":
            self.cursor.execute('''SELECT * FROM tdo.public.messages
                                            WHERE channelid=%s;''', (identifier,))
        elif column is "message":
            self.cursor.execute('''SELECT * FROM tdo.public.messages
                                            WHERE message=%s;''', (identifier,))
        elif column is "time":
            self.cursor.execute('''SELECT * FROM tdo.public.messages
                                            WHERE time=%s;''', (identifier,))
        return self.cursor.fetchone()

    def lookup_messages(self):
        # TODO ADD TIME RANGE CONSTRAINT, AND CHANNEL CONSTRAINT
        """
        Returns all the messages in the database
        :return: All messages in the database otherwise None
        """
        self.cursor.execute('''SELECT * FROM tdo.public.messages;''')
        return self.cursor.fetchall()

    # Create methods

    def create_user(self, data):
        """
        Use to instantiate a record in the database of the channel
        :param data: Should hold the form (ID, ALIAS, PASS)
        :return: None
        """
        self.cursor.execute('''INSERT INTO tdo.public.users (id, alias, pass)
                                       VALUES (%s, %s, %s);''', data)
        self.connection.commit()

    def create_channel(self, data):
        """
        Use to instantiate a record in the database of the channel
        :param data: Should hold the form (ID, NAME, PERMISSIONS)
        Blocked users isn't included in creation, cause there shouldn't be any on creation
        :return: None
        """
        self.cursor.execute('''INSERT INTO tdo.public.channels (id, name, permissions)
                               VALUES (%s, %s, %s);''', data)
        self.connection.commit()

    def create_message(self, data):
        """
        Stores a message in the database
        :param data: Should hold the form (ID, SENDERID, CHANNELID, MESSAGE, TIME)
        :return: None
        """
        self.cursor.execute('''INSERT INTO tdo.public.messages (id, senderid, channelid, message, time)
                               VALUES (%s, %s, %s, %s, %s);''', data)
        self.connection.commit()

    # Delete methods

    def delete_user(self, userid, username):
        """
        Deletes a user from the database
        :param user: User object to be deleted
        :return: None
        """
        self.cursor.execute('''DELETE FROM users WHERE id=%s AND alias=%s;''', (userid, username))
        self.connection.commit()

    def delete_channel(self, channelid, channelname):
        """
        Deletes a channel from the database
        :param channel: Channel object to be deleted
        :return: None
        """
        self.cursor.execute('''DELETE FROM channels WHERE id=%s AND name=%s;''', (channelid, channelname))
        self.connection.commit()

    # update methods

    def update_user(self, userid, name, password):
        """
        Modifys the user in the database with the given ID
        :param userid: ID of user being changed
        :return: None
        """
        self.cursor.execute('''UPDATE channels SET alias=%s, password=%s
                               WHERE id=%s;''', (name,password,userid))
        self.connection.commit()
    #

    def update_channel_permissions(self, channelid, permissions):
        """
        Update the permissions of a channel
        :param channelid: A channels id
        :param permissions: Permissions replacing with
        :return: None
        """
        self.cursor.execute("""UPDATE channels SET permissions=%s
                               WHERE id=%s;""", (permissions, channelid))
        self.connection.commit()

    def append_blocked_user_to_channel(self, channelid, userid):
        """
        Adds a user to the blocked user list for the channel
        :param channelid: ID of channel where the user will be blocked
        :param userid: User being blocked
        :return: None
        """
        self.cursor.execute("""UPDATE channels SET blocked_members = array_append(blocked_members, %s)
                               WHERE id=%s;""", (userid, channelid))
        self.connection.commit()

    def remove_blocked_user_from_channel(self, channelid, userid):
        """
        Removes a specific user from a given channel
        :param channelid: ID of channel for which to unblock the user
        :param userid: User being unblocked
        :return: None
        """
        self.cursor.execute("""UPDATE channels SET blocked_members = array_remove(blocked_members, %s)
                               WHERE id=%s;""", (userid, channelid))
        self.connection.commit()