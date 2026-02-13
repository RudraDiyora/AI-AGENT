def validate_user(bank):
    def decorator(func):
        def wrapper(*args, **kwargs):

            validated = True

            for param, param_value in kwargs.items():
                match param:
                    case 'user' | 'sender' | 'reciever':
                        if not(param_value in bank.users.keys()):
                            print(f"Invalid user: {param_value}")
                            validated = False
                    case 'amount' | 'transaction_amount':
                        if param_value < 0:
                            print(f"Invalid amount: {param_value}")
                            validated = False
                    case _:
                        pass
            
            if validated:
                return func(*args, **kwargs)
            else:
                print("Validation failed. Transaction aborted.")

        return wrapper
    return decorator
