from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from backend.bank import Bank


# create the app instance
app = FastAPI()
# create a testing bank
bank = Bank()

newUser = bank.create_user("Rudra","rudra@gmail.com")
secondUser = bank.create_user("Bob","Bob@gmail.com")

bank.request_deposit(user_id=newUser.id,amount=100)
bank.request_deposit(user_id=secondUser.id,amount=100)

# Define the shape of your data
class Deposit(BaseModel):
    user_id: str            # required 
    amount: float         # required 
class Withdraw(BaseModel):
    user_id: str            # required 
    amount: float         # required 
class Transfer(BaseModel):
    sender_id: str            # required 
    receiver_id: str
    transaction_amount: float         # required 
class User(BaseModel):
    name: str
    email: str


# creating classes
@app.post("/create-user")
def create_user(user: User):
    try:
        new_user = bank.create_user(user.name, user.email)
        return {"id": new_user.id, "name": new_user.name, "email": new_user.email}
    except Exception as e:
        # backend raised an error(most likely user already exists)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@app.get("/transaction_history/{user_id}")
def get_transaction_history(user_id: str):
    try:
        return bank.get_transaction_history(user_id=user_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    


# This is a "route" — a URL path that does something
@app.get("/balance/{user_id}")
def balance(user_id: str):
    return {"balance": bank.get_balance(user_id)}

@app.post("/deposit")
def deposit(deposit: Deposit):
    try:
        deposit_request = bank.request_deposit(deposit.user_id, deposit.amount)
        if not bool(deposit_request):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Deposit Failed: NullTransaction"
            )

        return {"status": "success"}
    except Exception as e:
        # backend raised a ValueError (e.g., negative funds)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
@app.post("/withdraw")
def withdraw(withdraw: Withdraw):
    try:
        withdraw_request = bank.request_withdraw(withdraw.user_id, withdraw.amount)

        if not bool(withdraw_request):
            # backend returned False
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Withdrawal Failed: NullTransaction"
            )
        return {"status": "success"}
    except Exception as e:
        # backend raised a ValueError (e.g., insufficient funds)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@app.post("/transfer")
def transfer(transfer: Transfer):
    try:
        # success = true fail = false
        transfer_request = bank.request_transfer(
                            transfer.sender_id, 
                            transfer.receiver_id, 
                            transfer.transaction_amount
                          )
        if not bool(transfer_request):
            # backend returned False
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Transfer Failed: NullTransaction"
            )
        return {"status": "success"}

    except Exception as e:
        # backend raised a ValueError (e.g., negative funds)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )