import bank as b

def validate_user(func):
   # def decorator(func):
        def wrapper(*args, **kwargs):

            validated = True
            bank = (args[0] if isinstance(args[0], b.Bank) else {})

            for param, param_value in kwargs.items():
                match param:
                    case 'user_id' | 'sender_id' | 'receiver_id':
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
#    return decorator
