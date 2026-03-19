from backend.main import User, Transaction, NullTransaction, NullUser, TransactionType
from backend.bank_validation import validate_user
from backend.database import DATABASE
from backend.engines.transaction_engine import TRANSACTION_ENGINE
import uuid

class Bank:
    def __init__(self, masterDB):
        self.id = str(uuid.uuid4())
        self.users = {} # store by {id: UserClass}
        self.emails = {} # store by {email: UserClass}
        self.transactions = {} # {transaction ID: transaction class} (stores transfers,deposites,withdraws)
        self.transaction_engine = TRANSACTION_ENGINE(masterDB=masterDB)
        self.masterDB = masterDB

    def create_user(self, name: str, email: str):
        try:
            new_user = User(name, email)
            self.masterDB.create(database_type=DATABASE.DATABASE_TYPES.USERS, instance=new_user)
            self.users[new_user.id] = new_user
            self.emails[email] = new_user
            return new_user
        except Exception as e:
            print(f"Create user failed: {e}")
            raise ValueError(f"Could not create user: {e}")
        
    def search_user(self, user_id: str = 'NULL', email: str = 'NULL') -> User | bool:
        # try:
        #     user = False
        #     if user_id != 'NULL': user = self.users[user_id]
        #     elif email != 'NULL': user = self.emails[email]
        #     return user
        # except KeyError:
        #     return False
        
        # if succesful: 0 -> id; 1 -> name; 2 -> email; 3 -> balance
        user_sql_data = self.masterDB.search_user(user_id=user_id)

        if user_sql_data:
            try:
                user = self.users[user_id]
            except:
                user = User(user_sql_data[1], user_sql_data[2])
                user.id = user_id
                user.balance = user_sql_data[3]
                self.users[user.id] = user
                self.emails[user.email] = user
            return user
        else:
            return NullUser()
        
    @validate_user
    def get_balance(self, user_id: str) -> float:
        try:
            user = self.users[user_id]
            return self.transaction_engine.get_balance(user_id=user_id)
        except KeyError:
            print("---ERROR---\n User Not Found")
            return 0.0
    
    @validate_user
    def get_transaction_history(self, user_id: str) -> list:
        try:
            user = self.search_user(user_id=user_id)
        except:
            raise ValueError("User not found")
        raw_transactions = self.masterDB.get_transaction_history(user_id=user_id)
        transaction_history = []

        for transaction in raw_transactions:
            transaction_history.append({
                "id": transaction[0],
                "sender_id": transaction[1],
                "receiver_id": transaction[2],
                "amount": transaction[3],
                "type": transaction[4],
                "time_stamp": transaction[5]
            })

        return transaction_history

    @validate_user
    def request_deposit(self, user_id: str, amount: float) -> bool:
        user = self.search_user(user_id=user_id)
        print(f"bank.py user_id: {user.id}")
        deposit_transaction = Transaction(sender=user, receiver=user, transaction_amount=amount, transaction_type=TransactionType.DEPOSIT)
        print(f"bank.py transaction: {deposit_transaction}")
        if self.transaction_engine.deposit(deposit_record=deposit_transaction):
            user.balance = self.transaction_engine.get_balance(user_id=user_id)
            self.transactions[deposit_transaction.id] = deposit_transaction

            return deposit_transaction
        else:
            return NullTransaction()
    
    @validate_user
    def request_withdraw(self, user_id: str, amount: float) -> bool:
        
        user = self.search_user(user_id=user_id)

        if (user.balance - amount) >= 0:
            withdrawl_transaction = Transaction(sender=user, receiver=user, transaction_amount=amount, transaction_type=TransactionType.WITHDRAW)

            if self.transaction_engine.withdraw(withdrawl_record=withdrawl_transaction):

                user.balance = self.transaction_engine.get_balance(user_id=user_id)

                self.transactions[withdrawl_transaction.id] = withdrawl_transaction

                return withdrawl_transaction
            else:
                return NullTransaction()
        else:
            return NullTransaction()

    @validate_user
    def request_transfer(self, sender_id: str, receiver_id: str, transaction_amount: float) -> Transaction:

        sender = self.search_user(user_id=sender_id)
        receiver = self.search_user(user_id=receiver_id)

        if sender == receiver:
            raise ValueError("TRANSFER ERROR: The sender and receiver can not be the same")
        if sender.balance < transaction_amount:
            raise ValueError("TRANSFER ERROR: The sender doesn't have enough funds to transfer")

        if sender.balance >= transaction_amount:

            new_transaction = Transaction(
                sender=sender, 
                receiver=receiver, 
                transaction_amount=transaction_amount, 
                transaction_type=TransactionType.TRANSFER
            )

            if self.transaction_engine.transfer(new_transaction):
                sender.balance = self.transaction_engine.get_balance(sender_id)
                receiver.balance = self.transaction_engine.get_balance(receiver_id)
                
                self.transactions[new_transaction.id] = new_transaction

                return new_transaction
            else:
                return NullTransaction()
        else:
            return NullTransaction()
