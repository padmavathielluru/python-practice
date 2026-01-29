from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer,HTTPBearer,HTTPAuthorizationCredentials
from jose import jwt,JWTError
from datetime import datetime,timedelta
import random
from fastapi import APIRouter,HTTPException,Query,Depends

router=APIRouter()
bearer_scheme=HTTPBearer()

#for config
SECRET_KEY="NoorSecretKey"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTE=15

oauth2_scheme=OAuth2PasswordBearer(tokenUrl="login/verify-otp")

#for temporary storing dictionary,while production time we can store this users/admins data in our redis or db
otp_store={} 


#inbuilt users,i'm defining users here only bcz its user POC
EMAIL_ROLE={
    "Noor@gmail.com":"user",
    "admin@gmail.com":"admin",
    "NoorAdmin@gmail.com":"admin"
}

#for generating OTP
def generate_otp():
    return str(random.randint(10000,99999)) #i'm generating here 5 digits OTP so i took the range in between 10000-99999

#to create JWT token

def create_access_token(data:dict,expires_delta:timedelta|None=None):
    to_encode=data.copy()
    expire=datetime.utcnow()+(expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTE))
    to_encode.update(
        {
            "exp":expire
        }
    )
    return jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)

#to  request OTP

@router.post("/login/request-otp")
def request_otp(email:str=Query(...)): # here query (three dots) represents the required feild * like user must fill the detail
    otp=generate_otp()
    expires_at=datetime.utcnow()+timedelta(minutes=5)
    otp_store[email]={"otp":otp,"expires":expires_at}
    return{
        "message":"OTP sent successfully",
        "otp_for_testing":otp
    }

#to verify OTP+ login

@router.post("/login/verify-otp")
def verify_otp(email:str=Query(...),otp:str=Query(...)):
    if email not in otp_store:
        raise HTTPException(status_code=400,detail="OTP not requested")
    saved_otp=otp_store[email]["otp"]
    expiry_time=otp_store[email]["expires"]

    if datetime.utcnow() > expiry_time: #to check the current time and otp generated time,if the otp generated time is more than 5mins it will gives error
        raise HTTPException(status_code=400,detail="OTP expired")
    
    if otp!=saved_otp:
        raise HTTPException(status_code=400,detail="Invalid OTP")
    
    #for using one OTP at once
    del otp_store[email]

    #role will assign based on email
    role=EMAIL_ROLE.get(email,"user")
    #jwt token generate
    access_token=create_access_token(
        data={
            "sub":email,
            "role":role
        }
    )
    return{
        "message":"Login Successful",
        "access_token":access_token,
        "token_type":"bearer"
    }

#to verify current user on jwt

def get_current_user(credentials:HTTPAuthorizationCredentials=Depends(bearer_scheme)):
    token=credentials.credentials
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=401,detail="Invalid or expired token")
    
#to check the role whether they are user or admin

def require_role(required_role:str):
    def role_checker(user=Depends(get_current_user)):
        if user.get("role")!= required_role:
            raise HTTPException(status_code=403,detail="Access forbidden")
        return user
    return role_checker

#to read user authentication
@router.get("/user-dashboard")
def user_dashboard(user=Depends(require_role("user"))):
    return {
        "message": "Welcome to user-dashboard",
        "email":user["sub"],
        "role":user["role"]
    }

#to read admin authentication
@router.get("/admin-dashboard")
def admin_dashboard(user=Depends(require_role("admin"))):
    return{
        "message":"Welcome Admin",
        "email":user["sub"],
        "role":user["role"]
    }



