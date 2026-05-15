# user->token
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone

# token->user 
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer

security = HTTPBearer()

class AUTHENTICATION_ENGINE:
    def __init__(self):
        self.KEY = "a3f91c2d9b7e4c1f8a6d3e2b9c0d4f11a8c7d6e5b4a3928170f6d5c4b3a2910"
        self.ALGORITHM = "HS256"
        self.ACCESS_TOKEN_EXPIRE_MINUTES = 30

    # session token handling
    def create_access_token(self, data: dict):
        to_encode = data.copy()
        # creates an "expiration data" for the token
        expire = datetime.now(timezone.utc) + timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES)

        to_encode.update({"exp": expire})

        # "signs off" on the token
        return jwt.encode(to_encode, self.KEY, self.ALGORITHM)
    
    # pure token verification, no api integration: "is this token valid?"
    def verify_token(self, token: str): # token is the JWT token string
        try:
            # jwt confirms the signature using the secret key
            # converts token->dict(user)
            payload = jwt.decode(token, self.KEY, self.ALGORITHM)
            return payload
        except JWTError:
            return None
        
    # fast api handling: extract the token from the api request: "how do I get the user from an HTTP request?"
    def get_current_user(self, api_request = Depends(security)): # api request is what is coming from api.js
        # extract the JWT token from the api request
        access_token = api_request.credentials

        # use our function to generate the user
        payload = self.verify_token(access_token)

        # none will be returned if the token isn't verified, so return the appropriate error
        if not payload:
            raise HTTPException(status_code=401, detail="Invalid access token")
        
        return payload
