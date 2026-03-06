
from main import NullTransaction

def validate_user(func):
    def wrapper(*args, **kwargs):
        import bank as b

        # Expecting the first arg to be Bank instance
        bank_instance = args[0] if isinstance(args[0], b.Bank) else None
        if not bank_instance:
            raise ValueError("First argument must be a Bank instance")

        # Validate user IDs
        for param in ['user_id', 'sender_id', 'receiver_id']:
            if param in kwargs:
                if kwargs[param] not in bank_instance.users:
                    print(f"Validation failed: Invalid user ID '{kwargs[param]}'")
                    return NullTransaction()  # consistent with failed transactions

        # Validate amounts
        for param in ['amount', 'transaction_amount']:
            if param in kwargs:
                if kwargs[param] < 0:
                    print(f"Validation failed: Invalid amount '{kwargs[param]}'")
                    return NullTransaction()

        # Passed validation
        return func(*args, **kwargs)

    return wrapper