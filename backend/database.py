import sqlite3
from enum import Enum


class DATABASE:
    class DATABASE_TYPES(Enum):
        USERS = {
            "ID": "INTEGER PRIMARY KEY",
            "Name": "TEXT",
            "Email": "TEXT",
            "Balance": "REAL"
        }
        TRANSACTIONS = {
            "ID": "INTEGER PRIMARY KEY",
            "SENDER_ID": "TEXT",
            "RECEIVER_ID": "TEXT",
            "AMOUNT": "REAL",
            "TIME": "TEXT",
            "TYPE": "TEXT"
        }
    def __init__(self, database_type):
        # create a connection to the database
        self.database_connection = sqlite3.connect(f'./databases/{database_type.name}.db')
        self.database_type = database_type
        # create a class to actual conduct operations on the database
        self.database_cursor = self.database_connection.cursor()

    def create_database(self):
        database_type = self.database_type
        sql_ = f"""CREATE TABLE IF NOT EXISTS {database_type.name} (\n"""

        for column_name, column_value in database_type.value.items():
            text = f"{column_name} {column_value},\n"
            sql_ += text

        parts_of_sql_ = sql_.rsplit(sep=",", maxsplit=1)
        sql = "".join(parts_of_sql_) + ")"

        print(sql)
        #call CURSOR.execute and pass in our SQL query
        self.database_cursor.execute(sql)
        #finally, fire off the database request
        self.database_connection.commit()


userDB = DATABASE(database_type=DATABASE.DATABASE_TYPES.USERS)
userDB.create_database()