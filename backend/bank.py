from main import User, Transaction
from validation import validate_user
import uuid

class Bank:
    def __init__(self):
        self.id = str(uuid.uuid4)
        self.users = {} # store by {id: UserClass}
        self.emails = {} # store by {email: name}
        self.transactions = {} # {transaction ID: transaction class}
        self.deposits = {} # --||--
        self.withdrawls = {} # {user ID: withdraw amount}

    def create_user(self, name: str, email: str):
        if email in self.emails.keys():
            print("ERROR: Email already exists")
        else:
            new_user = User(name, email)
            self.users[new_user.id: new_user]

            return new_user
        
    @validate_user
    def deposit(self, user_id: str, amount: int) -> bool:
        user = self.users[user_id]
        user.balance += amount

        deposit_transaction = Transaction(sender=user, reciever=user, transaction_amount=amount)
        self.deposits[deposit_transaction.id] = deposit_transaction

        return True
    
    @validate_user
    def withdraw(self, user_id: str, amount: int) -> bool:
        
        user = self.users[user_id]
        user.balance -= amount

        withdrawl_transaction = Transaction(sender=user, reciever=user, transaction_amount=amount)
        self.withdrawls[withdrawl_transaction.id] = withdrawl_transaction

        return True

    @validate_user
    def request_transaction(self, sender: User, reciever: User, transaction_amount: Transaction) -> Transaction:
        if sender.balance > transaction_amount:
            sender.balance -= transaction_amount
            reciever.balance += transaction_amount

            new_transaction = Transaction(sender=sender, reciever=reciever, transaction_amount=transaction_amount)
            self.transactions[new_transaction.id] = new_transaction

            return new_transaction
