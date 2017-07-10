import psycopg2
import hashlib, binascii


# Class used to manage interactions between the database and server
class DatabaseManager:

    connection = None
    cursor = None



    table_list = ['users', 'messages', 'chat_rooms']

    def __init__(self, user, password):
        connection = psycopg2.connect("dbname=tdo user=%s password=%s" % (user, password))
        cursor = connection.cursor()

    def write(self):
        pass
