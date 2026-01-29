from fastapi import FastAPI,Depends,HTTPException,status
from jose import jwt,JWTError
from datetime import datetime,timedelta,timezone
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm

app=FastAPI()

SECRET_KEY="MySecretKey"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30

pwd_context=CryptContext(schemes=['bcrypt'],deprecated='auto')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


user_db:dict[str,dict]={}

def hash_password(password:str):
    return pwd_context.hash(password)
def verify_password(password:str,hashed:str):
    return pwd_context.verify(password,hashed)
def create_access_token(username:str,role:str):
    payload={
        'sub':username,
        'role':role,
        'exp':datetime.now(timezone.utc)+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    return jwt.encode(payload,SECRET_KEY,algorithm=ALGORITHM)

@app.post('/register')
def register(username:str,password:str,role:str='user'):
    if username in user_db:
        raise HTTPException(status_code=400,details='User already existed')
    user_db[username]={
        'username':username,
        'password':hash_password(password),
        'role':role
            
        }
    return {'message':'user registered successfully!'}
@app.post('/login')
def login(form_data:OAuth2PasswordRequestForm=Depends()):
    user=user_db.get(form_data.username)

    if not user or not verify_password(form_data.password,user['password']):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Invalid username or password')
    token=create_access_token(user['username'],user['role'])
    return{
        'access_token':token,
        'token_type':'bearer',
        'role':user['role']
    }

def get_current_user(token:str=Depends(oauth2_scheme)):
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=401,detail='Invalid or expired token')
    
def require_role(role:str):
    def checker(user=Depends(get_current_user)):
        if user['role']!=role:
            raise HTTPException(status_code=403,detail="Access forbidden")
        return user
    return checker

@app.get('/user_details')
def user_details(user=Depends(get_current_user)):
    return{
        'message':f"welcome{user['sub']}",
        'role':user['role']
    }

@app.get('/admin_details')
def user_details(user=Depends(require_role('admin'))):
    return {'message':'Admin access sucessful'}