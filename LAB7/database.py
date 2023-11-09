from tinydb import TinyDB, Query

class Database:
    def __init__(self, name = 'db.json') -> None:
        self.db = TinyDB(name)

    def insert(self, data):
        self.db.insert(data)
    
    def all(self):
        self.db.all()

    def empty(self):
        self.db.truncate()











# import sqlite3
# from sqlite3 import Error

# def create_connection(db_file):
#     conn = None

#     try:
#         conn = sqlite3.connect(db_file)
#         print(sqlite3.version)
#     except Error as e:
#         print(e)
#     finally:
#         if conn:
#             conn.close()


# create_connection('999_data.db')