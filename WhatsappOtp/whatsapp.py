from twilio.rest import Client
import os
from dotenv import load_dotenv


load_dotenv()  

client = Client(
    os.getenv("TWILIO_ACCOUNT_SID"),
    os.getenv("TWILIO_AUTH_TOKEN")
)


def send_whatsapp_otp(phone:str,otp:str):
    
    message=client.messages.create(
        from_=os.getenv("TWILIO_WHATSAPP_FROM"),
        to= f"whatsapp:{phone}",
        body= f"your login OTP is:{otp}"
    )
    return message.sid
