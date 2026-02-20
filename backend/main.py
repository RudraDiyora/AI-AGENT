from datetime import datetime
from enum import Enum
import uuid

class TransactionType(Enum):
    TRANSFER = 1,
    DEPOSIT = 2,
    WITHDRAW = 3

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

    