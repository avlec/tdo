import psycopg2
import hashlib, binascii


# Class used to manage interactions between the database and server
class DatabaseManager:

    connection = None
    cursor = None

    table_list = ['users', 'messages', 'chat_rooms']

    def __init__(self, user, password):
        self.connection = psycopg2.connect("dbname=tdo user=%s password=%s" % (user, password))
        self.cursor = self.connection.cursor()

    def lookup(self):
        pass

    def write(self, data):
        # determine what kind of object is
        # send it to the appropriate write method
        pass

    # for writing a user to the DB
    def write_user(self, data):
        (salt, alias, passphrase) = data
        self.cursor.execute('''INSERT INTO USERS (salt, alias, passphrase)
                               VALUES (%s, %s, %s);''', (salt, alias, passphrase))
        self.connection.commit()
