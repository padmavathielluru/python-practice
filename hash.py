from fastapi import FastAPI,Depends,HTTPException,status
from datetime import datetime,timedelta,timezone
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import jwt,JWTError

app=FastAPI()

#these are configures
SECRET_KEY="thisissecretkey"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30

#password hashing
pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")

def hash_password(password:str):
    return pwd_context.hash(password)

def verify_password(plain,hashed):
    return pwd_context.verify(plain,hashed)

fake_users_db={
   "noor":{"username":"noor",
           "password":hash_password("user1234")}
           }
#for creating jwt token

def create_access_token(username:str):
    payload={
        "sub":username,
        "exp":datetime.now(timezone.utc)+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    return jwt.encode(payload,SECRET_KEY,algorithm=ALGORITHM)

#for user login

@app.post("/login")
def login(form_data:OAuth2PasswordRequestForm=Depends()):
    user=fake_users_db.get(form_data.username)

    if not user:
        raise HTTPException(status_code=401,detail="user not found")
    if not verify_password(form_data.password,user["password"]):
        raise HTTPException(status_code=401,detail="Wrong password")
    token=create_access_token(user["username"])

    return{
        "access_token":token,
        "token_type":"bearer"
    }

#for autherization

oauth2_scheme=OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token:str=Depends(oauth2_scheme)):
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        username=payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401)
        return username
    except JWTError:
        raise HTTPException(status_code=401,detail="Invalid token")
    
#protected route

@app.get("/dashboard")
def dashboard(user:str=Depends(get_current_user)):
    return{"message":f"welcome{user},you are autherized"}