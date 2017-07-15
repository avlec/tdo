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

    def lookup_query(self, table, identifier_type, identifier):
        self.cursor.execute('''SELECT * FROM %s
                               WHERE %s=%s''', (table, identifier_type, identifier))
        return self.cursor.fetchone()

    def lookup(self, type, identifier):
        """
        Considering redoing the way this method works,
        Possibly also changing how messages are accessed
        Because: messages are probably going to be accessed'
        by channel ID over id, and be sorted by time
        :param type:
        :param identifier:
        :return:
        """
        if type == 'USER':
            return self.lookup_query('tdo.public.users','ALIAS', identifier)
        elif type == 'MESSAGE':
            return self.lookup_query('tdo.public.messages', 'ID', identifier)
        elif type == '':
            pass
        return None

    def write(self, data):
        """
        Determines what class type the input is
        and calls the appropriate write method
        :param data:
        :return:
        """
        class_type = data.__class__.__name__
        if class_type is '__Client__':
            self._write_client(data)
        elif class_type is '__Message__':
            self._write_message(data)
        pass

    # for writing a user to the DB
    def _write_client(self, data):
        """
        (salt, alias, passphrase) = data
        """
        self.cursor.execute('''INSERT INTO tdo.public.users (salt, alias, pass)
                               VALUES (%s, %s, %s);''', data)
        self.connection.commit()

    def _write_message(self, data):
        """
        (messageId, senderId, messageChannelId, message, time) = data
        """
        self.cursor.execute('''INSERT INTO tdo.public.messages (id, senderid, channelId, message, time)
                               VALUES (%s, %s, %s, %s, %s);''', data)
        self.connection.commit()