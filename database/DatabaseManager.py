import psycopg2
import hashlib, binascii

# Class used to manage interactions between the database and server
class DatabaseManager:

    connection = None
    cursor = None

    table_list = ['users', 'messages', 'chat_rooms']

    def __init__(self, user, password):
        self.connection = psycopg2.connect("dbname=tdo host='localhost' user=%s password=%s" % (user, password))
        self.cursor = self.connection.cursor()

    # Lookup Commands
    def lookupUser(self, identifier, column="salt"):
        self.cursor.execute('''SELECT * FROM tdo.public.messages
                                               WHERE %s=%s''', (column, identifier))
        return self.cursor.fetchone()

    def lookupChatroom(self, identifier, column="id"):
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

    def createClient(self, data):
        """

        :param data:
        :return:
        """
        self.cursor.execute('''INSERT INTO tdo.public.users (salt, alias, pass)
                                       VALUES (%s, %s, %s);''', data)
        self.connection.commit()

    def createChatroom(self, data):
        """
        Use to instantiate a record in the database of the channel
        :param data: Should hold the form (ID, NAME, INITIAL_MEMBER_ID, PERMISSIONS)
        Blocked users isn't included in creation, cause there shouldn't be any on creation
        :return:
        """
        self.cursor.execute('''INSERT INTO tdo.public.channels (id, name, members, permissions)
                               VALUES (%s, %s, %s, %s);''', data)
        self.connection.commit()

    def createMessage(self, data):
        """

        :param data:
        :return:
        """
        self.cursor.execute('''INSERT INTO tdo.public.messages (id, senderid, channelid, message, time)
                               VALUES (%s, %s, %s, %s, %s);''', data)
        self.connection.commit()