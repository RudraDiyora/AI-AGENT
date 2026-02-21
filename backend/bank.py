from main import User, Transaction, TransactionType
from validation import validate_user
from database import DATABASE, userDB, transactionDB
import uuid

class Bank:
    def __init__(self):
        self.id = str(uuid.uuid4())
        self.users = {} # store by {id: UserClass}
        self.emails = {} # store by {email: UserClass}
        self.transactions = {} # {transaction ID: transaction class} (stores transfers,deposites,withdraws)

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
    def get_transaction_history(self, user_id: str) -> dict:
        user = self.search_user(user_id=user_id)
        transactions = {}

        for transaction_id, transaction in self.transactions.items():
            if user.id in transaction.transaction_participants:
                transactions[transaction_id] = transaction

        return transactions

    @validate_user
    def request_deposit(self, user_id: str, amount: float) -> bool:
        user = self.users[user_id]
        user.balance += amount

        deposit_transaction = Transaction(sender=user, receiver=user, transaction_amount=amount, transaction_type=TransactionType.DEPOSIT)
        self.transactions[deposit_transaction.id] = deposit_transaction

        return True
    
    @validate_user
    def request_withdraw(self, user_id: str, amount: float) -> bool:
        
        user = self.users[user_id]

        if (user.balance - amount) > 0:
            user.balance -= amount

            withdrawl_transaction = Transaction(sender=user, receiver=user, transaction_amount=amount, transaction_type=TransactionType.WITHDRAW)
            self.transactions[withdrawl_transaction.id] = withdrawl_transaction

            return True
        else:
            raise ValueError("WITHDRAW ERROR: Not enough funds")

    @validate_user
    def request_transfer(self, sender_id: str, receiver_id: str, transaction_amount: float) -> Transaction:

        sender = self.users[sender_id]
        receiver = self.users[receiver_id]

        if sender == receiver:
            raise ValueError("TRANSFER ERROR: The sender and receiver can not be the same")
        if sender.balance < transaction_amount:
            raise ValueError("TRANSFER ERROR: The sender doesn't have enough funds to transfer")

        if sender.balance >= transaction_amount:
            sender.balance -= transaction_amount
            receiver.balance += transaction_amount

            new_transaction = Transaction(
                sender=sender, 
                receiver=receiver, 
                transaction_amount=transaction_amount, 
                transaction_type=TransactionType.TRANSFER
            )
            
            self.transactions[new_transaction.id] = new_transaction
            transactionDB.create(new_transaction)

            return new_transaction
