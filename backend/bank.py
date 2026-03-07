from backend.main import User, Transaction, NullTransaction, TransactionType
from backend.bank_validation import validate_user
from backend.database import DATABASE, userDB, transactionDB
from backend.engines.transaction_engine import TRANSACTION_ENGINE
import uuid

class Bank:
    def __init__(self):
        self.id = str(uuid.uuid4())
        self.users = {} # store by {id: UserClass}
        self.emails = {} # store by {email: UserClass}
        self.transactions = {} # {transaction ID: transaction class} (stores transfers,deposites,withdraws)
        self.transaction_engine = TRANSACTION_ENGINE(userDB=userDB, transactionDB=transactionDB)

    def create_user(self, name: str, email: str):
        if email in self.emails.keys():
            print("ERROR: Email already exists")
        else:
            new_user = User(name, email)
            self.users[new_user.id] = new_user
            self.emails[email] = new_user

            userDB.create(new_user)
            return new_user
        
    def search_user(self, user_id: str = 'NULL', email: str = 'NULL') -> User | bool:
        try:
            user = False
            if user_id != 'NULL': user = self.users[user_id]
            elif email != 'NULL': user = self.emails[email]
            return user
        except KeyError:
            return False
        
    @validate_user
    def get_balance(self, user_id: str) -> float:
        try:
            user = self.users[user_id]
            return self.transaction_engine.get_balance(user_id=user_id)
        except KeyError:
            print("---ERROR---\n User Not Found")
            return 0.0
    
    @validate_user
    def get_transaction_history(self, user_id: str) -> dict:
        user = self.search_user(user_id=user_id)
        transactions = {}

        for transaction_id, transaction in self.transactions.items():
            if user.id in transaction.transaction_participants:
                transactions[transaction_id] = transaction

        return transactions

    @validate_user
    def request_deposit(self, user_id: str, amount: float) -> bool:
        print("____\n")
        print(self.users)
        print("____")
        user = self.users[user_id]
        deposit_transaction = Transaction(sender=user, receiver=user, transaction_amount=amount, transaction_type=TransactionType.DEPOSIT)
        if self.transaction_engine.deposit(deposit_record=deposit_transaction):
            user.balance = self.transaction_engine.get_balance(user_id=user_id)
            self.transactions[deposit_transaction.id] = deposit_transaction
            transactionDB.create(deposit_transaction)

            return deposit_transaction
        else:
            return NullTransaction()
    
    @validate_user
    def request_withdraw(self, user_id: str, amount: float) -> bool:
        
        user = self.users[user_id]

        if (user.balance - amount) >= 0:
            withdrawl_transaction = Transaction(sender=user, receiver=user, transaction_amount=amount, transaction_type=TransactionType.WITHDRAW)

            if self.transaction_engine.withdraw(withdrawl_record=withdrawl_transaction):

                user.balance = self.transaction_engine.get_balance(user_id=user_id)

                self.transactions[withdrawl_transaction.id] = withdrawl_transaction
                transactionDB.create(withdrawl_transaction)

                return withdrawl_transaction
            else:
                return NullTransaction()
        else:
            return NullTransaction()

    @validate_user
    def request_transfer(self, sender_id: str, receiver_id: str, transaction_amount: float) -> Transaction:

        sender = self.users[sender_id]
        receiver = self.users[receiver_id]

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
                transactionDB.create(new_transaction)

                return new_transaction
            else:
                return NullTransaction()
        else:
            return NullTransaction()
