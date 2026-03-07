from datetime import datetime
from enum import Enum
import uuid

class TransactionType(Enum):
    TRANSFER = 1,
    DEPOSIT = 2,
    WITHDRAW = 3,
    NULL = 4

class User:
    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email
        self.balance = 0
        self.id = str(uuid.uuid4())

    def __repr__(self):
        return f"User({self.name}, Balance: {self.balance})"

    
class Transaction:
    def __init__(self, sender: User, receiver: User, transaction_amount: int, transaction_type: TransactionType):
        self.id = str(uuid.uuid4())
        self.transaction_participants = [sender.id, receiver.id]
        self.sender = sender
        self.receiver = receiver
        self.sender_id = sender.id
        self.receiver_id = receiver.id
        self.transaction_amount = transaction_amount
        self.time_stamp = str(datetime.now().isoformat())
        self.transaction_type = transaction_type
        
    def __repr__(self):
        return (
            f"Transaction({self.transaction_amount} ({self.transaction_type}) from {self.sender_id} "
            f"to {self.receiver_id} at {self.time_stamp})"
        )
    
    def __bool__(self):
        return True

class NullTransaction(Transaction):
    def __init__(self):
        # Call the parent constructor with dummy/fake values
        # Or just set the properties manually
        self.id = "NULL"
        self.transaction_participants = []
        self.sender_id = None
        self.receiver_id = None
        self.transaction_amount = 0
        self.time_stamp = str(datetime.now().isoformat())
        self.transaction_type = TransactionType.NULL # or use your TransactionType enum if you have one

    def __repr__(self):
        return "<NullTransaction: FAILED>"
    
    def __bool__(self):
        return False