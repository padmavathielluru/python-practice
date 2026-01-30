from fastapi import Depends,APIRouter,HTTPException
from datetime import datetime,timedelta
from jose import jwt 
import random
import os
from utils import get_current_user
from whatsapp import send_whatsapp_otp

router=APIRouter()

#for temperary storage
OTP_STORE={}

SECRET_KEY=os.getenv("SECRET_KEY","ItsNoorSecretKey")
ALGORITHM=os.getenv("ALGORITHM","HS256")

#for sending OTP
@router.post("/send-otp")
def send_otp(phone_number:str):
    otp=str(random.randint(100000,999999))
    OTP_STORE[phone_number]=otp

    send_whatsapp_otp(phone_number,otp)
    return {
        "message":"OTP sent on whatsapp"
    }

#for verfying otp
@router.post("/verify-otp")
def verify_otp(phone_number:str,otp:str):
    if OTP_STORE.get(phone_number)!=otp:
        raise HTTPException(status_code=400,detail="Invalid OTP")
    
    token = create_access_token(phone_number)

    return{
        "message":"LOGIN SUCCESSFUL",
        "access_token":token,
        "token_type":"bearer"      
    }

def create_access_token(phone:str):
    payload={
        "sub":phone,
        "exp":datetime.utcnow()+timedelta(minutes=15)
    }
    token=jwt.encode(payload,SECRET_KEY,algorithm=ALGORITHM)
    return token

@router.get("/me")
def get_me(user=Depends(get_current_user)):
    return {"logged_in_user": user}