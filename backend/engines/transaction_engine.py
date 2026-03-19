class TRANSACTION_ENGINE:
    def __init__(self, masterDB):
        self.masterDB = masterDB

    def get_balance(self, user_id):
        with self.masterDB.database_connection:
            self.masterDB.database_cursor.execute(
                "SELECT BALANCE FROM USERS WHERE ID=?", 
                (user_id,)
            )

            result = self.masterDB.database_cursor.fetchone()
            if result is None:
                raise ValueError("User not found")
            return result[0]
    
    def deposit(self, deposit_record):
        if deposit_record.transaction_amount <= 0:
            raise ValueError("Deposit: Amount must be positive")
        try:
            with self.masterDB.database_connection: # auto commit and rollback
                # Confirm the sender
                self.masterDB.database_cursor.execute("""
                    SELECT BALANCE FROM USERS WHERE ID = ?""", 
                    (deposit_record.sender_id,)
                )
                user_balance = self.masterDB.database_cursor.fetchone()    
                self.masterDB.database_cursor.execute("SELECT * FROM USERS;")
                print(f"TESTING: {self.masterDB.database_cursor.fetchall()}")  
                print(f"USER: {user_balance} \n")
                if not user_balance:
                    raise ValueError("User Not Found")
                user_balance = user_balance[0]
                
                # Conduct the transaction
                self.masterDB.database_cursor.execute ("""
                    UPDATE USERS
                    SET BALANCE = BALANCE + ?
                    WHERE ID = ? """,
                    (deposit_record.transaction_amount, deposit_record.sender.id)
                )

                # create a deposit record in the transaction
                self.masterDB.database_cursor.execute("""
                    INSERT INTO TRANSACTIONS 
                        (ID, SENDER_ID, RECEIVER_ID, TRANSACTION_AMOUNT, TRANSACTION_TYPE, TIME_STAMP)
                        VALUES (?, ?, ?, ?, ?, ?)""",
                    (deposit_record.id, deposit_record.sender_id, deposit_record.receiver_id, deposit_record.transaction_amount, 
                     deposit_record.transaction_type.name, deposit_record.time_stamp)
                )
            deposit_record.sender.balance = self.get_balance(deposit_record.sender.id)

            return True
        except Exception as e:
            with self.masterDB.database_connection:
                self.masterDB.database_cursor.execute("""
                    INSERT INTO TRANSACTIONS 
                        (ID, SENDER_ID, RECEIVER_ID, TRANSACTION_AMOUNT, TRANSACTION_TYPE, TIME_STAMP)
                        VALUES (?, ?, ?, ?, ?, ?)""",
                    (deposit_record.id, deposit_record.sender_id, deposit_record.receiver_id, deposit_record.transaction_amount, 
                     "DEPOSIT_FAIL", deposit_record.time_stamp)
                )
            print(f"Deposit failed: {e}")
            return False

    def withdraw(self, withdrawl_record):
        if withdrawl_record.transaction_amount <= 0:
            raise ValueError("Withdraw: Amount must be positive")
        try:
            with self.masterDB.database_connection: # auto commit and rollback
                # Confirm the sender
                self.masterDB.database_cursor.execute("""
                    SELECT BALANCE FROM USERS WHERE ID = ?""", 
                    (withdrawl_record.sender_id,)
                )
                user_balance = self.masterDB.database_cursor.fetchone()    
                if not user_balance:
                    raise ValueError("User Not Found")
                user_balance = user_balance[0]

                if user_balance < withdrawl_record.transaction_amount:
                    raise ValueError("User has insuffient funds")
                
                # Conduct the transaction
                self.masterDB.database_cursor.execute ("""
                    UPDATE USERS
                    SET BALANCE = BALANCE - ?
                    WHERE ID = ? """,
                    (withdrawl_record.transaction_amount, withdrawl_record.sender.id)
                )

                # create a withdraw record in transactions
                self.masterDB.database_cursor.execute("""
                    INSERT INTO TRANSACTIONS 
                        (ID, SENDER_ID, RECEIVER_ID, TRANSACTION_AMOUNT, TRANSACTION_TYPE, TIME_STAMP)
                        VALUES (?, ?, ?, ?, ?, ?)""",
                    (withdrawl_record.id, withdrawl_record.sender_id, withdrawl_record.receiver_id, withdrawl_record.transaction_amount, 
                     withdrawl_record.transaction_type.name, withdrawl_record.time_stamp)
                )
            withdrawl_record.sender.balance = self.get_balance(withdrawl_record.sender.id)

            return True

        except Exception as e:
            # insert a failed transaction
            with self.masterDB.database_connection:
                self.masterDB.database_cursor.execute("""
                    INSERT INTO TRANSACTIONS 
                        (ID, SENDER_ID, RECEIVER_ID, TRANSACTION_AMOUNT, TRANSACTION_TYPE, TIME_STAMP)
                        VALUES (?, ?, ?, ?, ?, ?)""",
                    (withdrawl_record.id, withdrawl_record.sender_id, withdrawl_record.receiver_id, withdrawl_record.transaction_amount, 
                     "WITHDRAW_FAIL", withdrawl_record.time_stamp)
                )
            print(f"Withdrawal failed: {e}")
            return False

    def transfer(self, transaction_record):
        try: 
            with self.masterDB.database_connection: # auto commit and rollback
                # Confirm the sender
                self.masterDB.database_cursor.execute("""
                    SELECT BALANCE FROM USERS WHERE ID = ?""", 
                    (transaction_record.sender_id,)
                )
                sender_balance = self.masterDB.database_cursor.fetchone()    
                if not sender_balance:
                    raise ValueError("Sender Not Found")
                sender_balance = sender_balance[0]

                # confirm that that the sender has enough money
                if sender_balance < transaction_record.transaction_amount:
                    raise ValueError("Sender does not have enough funds")

                # Confirm the receiver
                self.masterDB.database_cursor.execute("""
                    SELECT BALANCE FROM USERS WHERE ID = ?""", 
                    (transaction_record.receiver_id,)
                )
                receiver_balance = self.masterDB.database_cursor.fetchone()    
                if not receiver_balance:
                    raise ValueError("Receiver Not Found")
                
                # Conduct the transaction
                self.masterDB.database_cursor.execute ("""
                    UPDATE USERS
                    SET BALANCE = BALANCE - ?
                    WHERE ID = ? """,
                    (transaction_record.transaction_amount, transaction_record.sender.id)
                )
                self.masterDB.database_cursor.execute("""
                    UPDATE USERS
                    SET BALANCE = BALANCE + ?
                    WHERE ID = ?""",
                    (transaction_record.transaction_amount, transaction_record.receiver.id)
                )

                # create a transfer record in transactions
                self.masterDB.database_cursor.execute("""
                    INSERT INTO TRANSACTIONS 
                        (ID, SENDER_ID, RECEIVER_ID, TRANSACTION_AMOUNT, TRANSACTION_TYPE, TIME_STAMP)
                        VALUES (?, ?, ?, ?, ?, ?)""",
                    (transaction_record.id, transaction_record.sender_id, transaction_record.receiver_id, transaction_record.transaction_amount, 
                     transaction_record.transaction_type.name, transaction_record.time_stamp)
                )

            transaction_record.sender.balance = self.get_balance(transaction_record.sender.id)
            transaction_record.receiver.balance = self.get_balance(transaction_record.receiver.id)
            return True

        except Exception as e:
            with self.masterDB.database_connection:
                self.masterDB.database_cursor.execute("""
                    INSERT INTO TRANSACTIONS 
                        (ID, SENDER_ID, RECEIVER_ID, TRANSACTION_AMOUNT, TRANSACTION_TYPE, TIME_STAMP)
                        VALUES (?, ?, ?, ?, ?, ?)""",
                    (transaction_record.id, transaction_record.sender_id, transaction_record.receiver_id, transaction_record.transaction_amount, 
                     "TRANSFER_FAIL", transaction_record.time_stamp)
                )
            print(f"Transfer failed: {e}")
            return False
