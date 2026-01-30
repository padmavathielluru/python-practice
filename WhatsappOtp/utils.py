
from dotenv import load_dotenv
load_dotenv()

from fastapi import HTTPException,Depends
from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials
from jose import jwt,JWTError
import os

SECRET_KEY=os.getenv("SECRET_KEY")
ALGORITHM="HS256"

security=HTTPBearer()

def get_current_user(
        credentials:HTTPAuthorizationCredentials=Depends(security)):
    token=credentials.credentials
    if not SECRET_KEY:
        raise HTTPException(status_code=500, detail="SECRET_KEY is not set!")
    
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        phone=payload.get("sub")

        if phone is None:
            raise HTTPException(status_code=401,detail="Invalid token")
        return phone
    except JWTError:
        raise HTTPException(status_code=401,detail="Token Invalid or expired")
