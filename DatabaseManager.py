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

    # for writing a user to the DB
    def write_user(self, (name, passphrase, salt, ip)):
        self.cursor.execute('''INSERT INTO USERS (name, passphrase, salt, ipaddress)
                               VALUES (%s, %s, %s, %s);''', (name, passphrase, salt, ip))
        self.connection.commit()
