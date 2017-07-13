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
        if type == 'user':
            return self.lookup_query('USERS','ALIAS', identifier)
        elif type == 'chatroom':
            return self.lookup_query('CHATROOMS', 'NAME', identifier)
        elif type == '':
            pass
        return None

    def write(self, data):
        # determine what kind of object is
        # send it to the appropriate write method
        pass

    # for writing a user to the DB
    def write_user(self, data):
        (salt, alias, passphrase) = data
        self.cursor.execute('''INSERT INTO USERS (salt, alias, pass)
                               VALUES (%s, %s, %s);''', (salt, alias, passphrase))
        self.connection.commit()
