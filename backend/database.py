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
        self.database_connection = sqlite3.connect(f'./databases/BANK_MAIN.db')
        # create a class to actual conduct operations on the database
        self.database_cursor = self.database_connection.cursor()


    def create(self, instance):

        instance_variables = instance.__dict__
        self.save_database(instance_variables)


    def save_database(self, values):

        # standardized the case sentititvyt to upper case
        values = {
            k.upper(): (v.name if isinstance(v, Enum) else v)
            for k, v in values.items()
        }

        database_type = self.database_type

        # Generate the names of the desired columns
        colum_names = ", ".join(database_type.value.keys())
        # Generate the values that will be inserted
        placeholders = ", ".join(f":{column_name}" for column_name in database_type.value.keys())

        sql = f"""
            INSERT INTO {database_type.name} 
            ({colum_names}) 
            VALUES({placeholders})
            """

        # Before we exequte and inject the sql, make sure that nothing is missing
        for column_name in database_type.value.keys():
            if column_name.upper() not in values:
                raise ValueError(f"Missing field: {column_name}")

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
        #fire off the database request(only use .commit() when changing the database)
        self.database_connection.commit()


userDB = DATABASE(database_type=DATABASE.DATABASE_TYPES.USERS)
userDB.create_database()
transactionDB = DATABASE(database_type=DATABASE.DATABASE_TYPES.TRANSACTIONS)
transactionDB.create_database()

# Testing

userDB.database_cursor.execute("SELECT * FROM USERS;")

transactionDB.database_cursor.execute("SELECT * FROM TRANSACTIONS;")

print(transactionDB.database_cursor.fetchall())