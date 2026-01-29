from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from twilio.rest import Client
 
import random
 
 
 
app =FastAPI()
 
#Twillo credentials

 
Client= Client(TWILLO_ACCOUNT_SID,TWILLO_AUTH_TOKEN)
 
#otp storage
otp_storage={}
 
#model for sending otp
class Phone(BaseModel):
    phone_number:str
 
#model for verifying number
class VerfyOTP(BaseModel):
    Phone_number:str
    otp:str
 
 
#to generate OTP function
 
def generate_otp():
    return str(random.randint(1000,9999))
 
#send otp via sms
 
def send_otp(phone_number,otp):
    message=f"Your Otp is :{otp}"
    Client.messages.create(to=phone_number,from_=TWILLO_PHONE_NUMBER,body=message)
 
 
#route to send otp
@app.post("/send-otp/")
async def send_otp_route(phone:Phone):
    otp=generate_otp()
    otp_storage[phone.phone_number]=otp
    send_otp(phone.phone_number,otp)
    return {"detail":"OTP sent successfully"}
 
#Route to verify OTP
@app.post("/verify-otp/")
async def verify_otp_route(otp_data:VerfyOTP):
    stored_otp=otp_storage.get(otp_data.Phone_number)
    if not stored_otp:
        raise HTTPException(status_code=400,detail="OTP not found")
    if stored_otp!=otp_data.otp:
        raise HTTPException(status_code=400,detail="Ivalid OTP")
    #for clearing the otp once after successful verification
    del otp_storage[otp_data.Phone_number]
    return{"detail":"OTP varified successfully"}