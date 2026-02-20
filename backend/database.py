import sqlite3
from enum import Enum

class DATABASE:

    class DATABASE_TYPES(Enum):
        USERS = {
            "ID": "TEXT", # Integer Primary Key = Original SQL Native
            "NAME": "TEXT",
            "EMAIL": "TEXT",
            "BALANCE": "REAL"
        }
        TRANSACTIONS = {
            "ID": "TEXT",
            "SENDER_ID": "TEXT",
            "RECEIVER_ID": "TEXT",
            "TRANSACTION_AMOUNT": "REAL",
            "TIME_STAMP": "TEXT",
            "TRANSACTION_TYPE": "TEXT"
        }
    
    def __init__(self, database_type):
        self.database_type = database_type  
        # create a connection to the database
        self.database_connection = sqlite3.connect(f'./databases/{database_type.name}.db')
        # create a class to actual conduct operations on the database
        self.database_cursor = self.database_connection.cursor()


    def create(self, instance):

        instance_variables = instance.__dict__
        self.save_database(instance_variables)


    def save_database(self, values):

        # standardized the case sentititvyt to upper case
        values = {k.upper(): v for k, v in values.items()}

        for k, v in values.items():
            if isinstance(v, Enum):
                values[k] = v.name # only pass the name of the Enum

        database_type = self.database_type
        sql_ = f"""INSERT INTO {database_type.name} ("""

        # Generate all the columns
        for column_name in database_type.value.keys():
            text = f"{column_name.upper()},"
            sql_ += text
        
        # Prepare to insert values
        parts_of_sql_ = sql_.rsplit(sep=",", maxsplit=1)
        sql = "".join(parts_of_sql_) + ") \nVALUES ("

        # Generate the values SQL Injection
        for column_name in database_type.value.keys():
            text = f":{column_name.upper()},"
            sql += text
        # Format the sql
        sql = "".join(sql.rsplit(sep=",", maxsplit=1)) + ")"

        self.database_cursor.execute(sql, values) # request an sql query
        self.database_connection.commit() # commit the request


    def create_database(self):
        database_type = self.database_type
        sql_ = f"""CREATE TABLE IF NOT EXISTS {database_type.name} (\n"""

        for column_name, column_value in database_type.value.items():
            text = f"{column_name} {column_value},\n"
            sql_ += text

        parts_of_sql_ = sql_.rsplit(sep=",", maxsplit=1)
        sql = "".join(parts_of_sql_) + ")"

        #call CURSOR.execute and pass in our SQL query
        self.database_cursor.execute(sql)
        #fire off the database request
        self.database_connection.commit()


userDB = DATABASE(database_type=DATABASE.DATABASE_TYPES.USERS)
userDB.create_database()
transactionDB = DATABASE(database_type=DATABASE.DATABASE_TYPES.TRANSACTIONS)
transactionDB.create_database()

# Testing

userDB.database_cursor.execute("SELECT * FROM USERS;")
userDB.database_connection.commit()

transactionDB.database_cursor.execute("SELECT * FROM TRANSACTIONS;")
transactionDB.database_connection.commit()
print(transactionDB.database_cursor.fetchall())