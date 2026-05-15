from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel
from .bank import Bank
from .database import masterDB



# create the app instance
app = FastAPI()
# create a testing bank
bank = Bank(masterDB=masterDB)

#newUser = bank.create_user("Rudra","rudra@gmail.com")
# secondUser = bank.create_user("Bob","Bob@gmail.com")

# make sure the frontend reads the same server as the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# Define the shape of your data
class Deposit(BaseModel):
    amount: float         # required 
class Withdraw(BaseModel):
    amount: float         # required 
class Transfer(BaseModel):
    receiver_id: str
    transaction_amount: float         # required 
class User(BaseModel):
    name: str
    email: str
    password: str
class LoginRequest(BaseModel):
    email: str
    password: str


# debugging
@app.get("/db_users")
def get_users():
    try:
        masterDB.database_cursor.execute("SELECT * FROM USERS;")
        return masterDB.database_cursor.fetchall()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
@app.get("/db_transactions")
def get_transaction_history_all():
    try:
        masterDB.database_cursor.execute("SELECT * FROM TRANSACTIONS;")
        return masterDB.database_cursor.fetchall()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    
#session handling
@app.get("/me")
def get_me(user = Depends(bank.authentication_engine.get_current_user)):
    return user

#login handling
@app.post("/login")
def login(request: LoginRequest):

    user = bank.search_user(email=request.email)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    
    if not bank.security_engine.verifyPassword(
        raw_password=request.password,
        hashed_password=user.hashed_password
    ):
        raise HTTPException(
            status_code=401,
            detail="Incorrect credentials"
        )
    
    access_token = bank.authentication_engine.create_access_token(
        {
            "user_id": user.id,
            "name": user.name,
            "email": user.email
        }
    )
    
    return {
        "success": True,
        "access_token": access_token,
        "token_type": "bearer"
    }

# creating classes
@app.post("/create-user")
def create_user(user: User):
    try:
        hashed_password = bank.security_engine.hashPassword(user.password)
        new_user = bank.create_user(user.name, user.email, hashed_password)
        return {"id": new_user.id, "name": new_user.name, "email": new_user.email, "password": "***"}
    except Exception as e:
        # backend raised an error(most likely user already exists)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@app.get("/transaction-history")
def get_transaction_history(user = Depends(bank.authentication_engine.get_current_user)):
    try:
        user_id = user["user_id"]
        return bank.get_transaction_history(user_id=user_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    
# This is a "route" — a URL path that does something
@app.get("/balance")
def balance(user = Depends(bank.authentication_engine.get_current_user)):
    user_id = user["user_id"]
    return {"balance": bank.get_balance(user_id)}

@app.post("/deposit")
def deposit(deposit: Deposit, user = Depends(bank.authentication_engine.get_current_user)):
    try:
        user_id = user["user_id"]
        deposit_request = bank.request_deposit(user_id, deposit.amount)
        print(f"api.py: {deposit_request}")
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
def withdraw(withdraw: Withdraw, user = Depends(bank.authentication_engine.get_current_user)):
    try:
        user_id = user["user_id"]
        withdraw_request = bank.request_withdraw(user_id, withdraw.amount)

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
def transfer(transfer: Transfer, user = Depends(bank.authentication_engine.get_current_user)):
    sender_id = user["user_id"]
    try:
        # success = true fail = false
        transfer_request = bank.request_transfer(
                            sender_id, 
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