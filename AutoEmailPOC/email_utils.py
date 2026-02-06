import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email_util(to_email:str,subject:str,body:str):
    print("sending email to:",to_email)


    #MIMEMultipart is used when email have multiple parts to send (like sub+body+attachments)
    msg=MIMEMultipart()
    msg["From"]=os.getenv("EMAIL_USER")
    msg["To"]=to_email
    msg["Subject"]=subject

    #msg.attach(MIMEText(body,"html"))
     
    #here MIMEText is used to form email body(text/html) 
    msg.attach(MIMEText("Hello test email","html"))
     
    server=smtplib.SMTP(
        os.getenv("EMAIL_HOST"),
        int(os.getenv("EMAIL_PORT")))

    server.set_debuglevel(1)
    
    server.starttls()
    server.login(os.getenv("EMAIL_USER"),os.getenv("EMAIL_PASS"))
    server.send_message(msg)
    
    server.quit()


