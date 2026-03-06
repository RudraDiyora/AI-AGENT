class TRANSACTION_ENGINE:
    def __init__(self, userDB, transactionDB):
        self.userDB = userDB
        self.transactionDB = transactionDB

    def get_balance(self, user_id):
        self.userDB.database_cursor.execute(
            "SELECT BALANCE FROM USERS WHERE ID=?", 
            (user_id,)
        )

        result = self.userDB.database_cursor.fetchone()
        if result is None:
            raise ValueError("User not found")
        return result[0]
    
    def deposit(self, deposit_record):
        if deposit_record.transaction_amount <= 0:
            raise ValueError("Deposit: Amount must be positive")
        try:
            with self.transactionDB.database_connection: # auto commit and rollback
                # Confirm the sender
                self.transactionDB.database_cursor.execute("""
                    SELECT BALANCE FROM USERS WHERE ID = ?""", 
                    (deposit_record.sender.id,)
                )
                user_balance = self.transactionDB.database_cursor.fetchone()    
                if not user_balance:
                    raise ValueError("User Not Found")
                user_balance = user_balance[0]
                
                # Conduct the transaction
                self.transactionDB.database_cursor.execute ("""
                    UPDATE USERS
                    SET BALANCE = BALANCE + ?
                    WHERE ID = ? """,
                    (deposit_record.transaction_amount, deposit_record.sender.id)
                )

            deposit_record.sender.balance = self.get_balance(deposit_record.sender.id)
            return True
        except Exception as e:
            print(deposit_record.__dict__)
            print(f"Deposit failed: {e}")
            return False

    def withdraw(self, withdrawl_record):
        if withdrawl_record.transaction_amount <= 0:
            raise ValueError("Withdraw: Amount must be positive")
        try:
            with self.transactionDB.database_connection: # auto commit and rollback
                # Confirm the sender
                self.transactionDB.database_cursor.execute("""
                    SELECT BALANCE FROM USERS WHERE ID = ?""", 
                    (withdrawl_record.sender.id,)
                )
                user_balance = self.transactionDB.database_cursor.fetchone()    
                if not user_balance:
                    raise ValueError("User Not Found")
                user_balance = user_balance[0]

                if user_balance < withdrawl_record.transaction_amount:
                    raise ValueError("User has insuffient funds")
                
                # Conduct the transaction
                self.transactionDB.database_cursor.execute ("""
                    UPDATE USERS
                    SET BALANCE = BALANCE - ?
                    WHERE ID = ? """,
                    (withdrawl_record.transaction_amount, withdrawl_record.sender.id)
                )
            withdrawl_record.sender.balance = self.get_balance(withdrawl_record.sender.id)
            return True

        except Exception as e:
            print(f"Withdrawal failed: {e}")
            return False

    def transfer(self, transaction_record):
        try: 
            with self.transactionDB.database_connection: # auto commit and rollback
                # Confirm the sender
                self.transactionDB.database_cursor.execute("""
                    SELECT BALANCE FROM USERS WHERE ID = ?""", 
                    (transaction_record.sender.id,)
                )
                sender_balance = self.transactionDB.database_cursor.fetchone()    
                if not sender_balance:
                    raise ValueError("Sender Not Found")
                sender_balance = sender_balance[0]

                # confirm that that the sender has enough money
                if sender_balance < transaction_record.transaction_amount:
                    raise ValueError("Sender does not have enough funds")

                # Confirm the receiver
                self.transactionDB.database_cursor.execute("""
                    SELECT BALANCE FROM USERS WHERE ID = ?""", 
                    (transaction_record.receiver.id,)
                )
                receiver_balance = self.transactionDB.database_cursor.fetchone()    
                if not receiver_balance:
                    raise ValueError("Receiver Not Found")
                
                # Conduct the transaction
                self.transactionDB.database_cursor.execute ("""
                    UPDATE USERS
                    SET BALANCE = BALANCE - ?
                    WHERE ID = ? """,
                    (transaction_record.transaction_amount, transaction_record.sender.id)
                )
                self.transactionDB.database_cursor.execute("""
                    UPDATE USERS
                    SET BALANCE = BALANCE + ?
                    WHERE ID = ?""",
                    (transaction_record.transaction_amount, transaction_record.receiver.id)
                )

            transaction_record.sender.balance = self.get_balance(transaction_record.sender.id)
            transaction_record.receiver.balance = self.get_balance(transaction_record.receiver.id)
            return True

        except Exception as e:
            print(f"Transfer failed: {e}")
            return False
