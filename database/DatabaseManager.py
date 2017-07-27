import psycopg2
# import hashlib, binascii

# Class used to manage interactions between the database and server
class DatabaseManager:

    connection = None
    cursor = None

    def __init__(self, user, password):
        self.connection = psycopg2.connect("dbname=tdo host='localhost' user=%s password=%s" % (user, password))
        self.cursor = self.connection.cursor()

    # Lookup Commands

    def lookupUser(self, identifier, column="id"):
        self.cursor.execute('''SELECT * FROM tdo.public.messages
                                               WHERE %s=%s''', (column, identifier))
        return self.cursor.fetchone()

    def lookupChannel(self, identifier, column="id"):
        self.cursor.execute('''SELECT * FROM tdo.public.messages
                                               WHERE %s=%s''', (column, identifier))
        return self.cursor.fetchone()

    def lookupMessage(self, identifier, column="id"):
        self.cursor.execute('''SELECT * FROM tdo.public.messages
                                       WHERE %s=%s''', (column, identifier))
        return self.cursor.fetchone()

    def lookupMessages(self, identifier, column="id"):
        self.cursor.execute('''SELECT * FROM tdo.public.messages
                                       WHERE %s=%s''', (column, identifier))
        return self.cursor.fetchall()

    # Create methods

    def createUser(self, data):
        """

        :param data:
        :return:
        """
        self.cursor.execute('''INSERT INTO tdo.public.users (id, alias, pass)
                                       VALUES (%s, %s, %s);''', data)
        self.connection.commit()

    def createChannel(self, data):
        """
        Use to instantiate a record in the database of the channel
        :param data: Should hold the form (ID, NAME, PERMISSIONS)
        Blocked users isn't included in creation, cause there shouldn't be any on creation
        :return:
        """
        self.cursor.execute('''INSERT INTO tdo.public.channels (id, name, permissions)
                               VALUES (%s, %s, %s);''', data)
        self.connection.commit()

    def createMessage(self, data):
        """

        :param data: Should hold the form (ID, SENDERID, CHANNELID, MESSAGE, TIME)
        :return:
        """
        self.cursor.execute('''INSERT INTO tdo.public.messages (id, senderid, channelid, message, time)
                               VALUES (%s, %s, %s, %s, %s);''', data)
        self.connection.commit()

    # update methods

    def updateUser(self, userid, name, password):
        """

        :param userid:
        :return:
        """
        self.cursor.execute('''UPDATE channels SET alias=%s, password=%s
                               WHERE id=%s''', (name,password,userid))
        self.connection.commit()
    #

    def updateChannelPermissions(self, channelid, permissions):
        """
        Update the permissions of a channel
        :param channelid: A channels id
        :param permissions: Permissions replacing with
        :return: None
        """
        self.cursor.execute("""UPDATE channels SET permissions=%s
                               WHERE id=%s""", (permissions, channelid))
        self.connection.commit()

    def appendBlockedChannel(self, channelid, userid):
        """
        Adds a user to the blocked user list for the channel
        :param channelid:
        :param userid:
        :return:
        """
        self.cursor.execute("""UPDATE channels SET blocked_members = array_append(blocked_members, %s)
                               WHERE id=%s""", (userid, channelid))
        self.connection.commit()

    def removeBlockedUser(self, channelid, userid):
        """

        :param channelid:
        :param userid:
        :return:
        """
        self.cursor.execute("""UPDATE channels SET blocked_members = array_remove(blocked_members, %s)
                               WHERE id=%s""", (userid, channelid))
        self.connection.commit()