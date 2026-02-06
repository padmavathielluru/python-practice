from fastapi import FastAPI,HTTPException,Request
from pydantic import BaseModel
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

app=FastAPI()

class EmailSchema(BaseModel):
    recipient_email:str
    subject:str
    body:str


@app.post("/send_email")
def send_email(email_data:EmailSchema):
    send_email="acchugatlanoorjahan@gmail.com"
    sender_password="baxfcuxqggiqlnyz"
    recipient_email=email_data.recipient_email
    subject=email_data.subject
    body=email_data.body


    #setup for SMTP server
    smtp_server=smtplib.SMTP("smtp.gmail.com",587)
    smtp_server.starttls()
    try:
        #login to the SMPT sever
        smtp_server.login(send_email,sender_password)
        #create a multipart message and set headers
        message=MIMEMultipart()
        message["From"]=send_email
        message["To"]=recipient_email
        message["Subject"]=subject

        #Add body to email
        message.attach(MIMEText(body,"plain"))
    
        #send the email
        smtp_server.sendmail(send_email,recipient_email,message.as_string())
        smtp_server.quit()

        return {
           "message":"Email send successfully"

        }
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"failed to send email:{str(e)}")

