from datetime import datetime
import uuid

class User:
    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email
        self.balance = 0
        self.id = str(uuid.uuid4())
    def __repr__(self):
        return f"User({self.name}, Balance: {self.balance})"

    
class Transaction:
    def __init__(self, sender: User, receiver: User, transaction_amount: int):
        self.id = str(uuid.uuid4())
        self.sender_id = sender.id
        self.receiver_id = receiver.id
        self.transaction_amount = transaction_amount
        self.time_stamp = datetime.now
        
    def __repr__(self):
        return (
            f"Transaction({self.transaction_amount} from {self.sender_id} "
            f"to {self.receiver_id} at {self.time_stamp()})"
        )

    