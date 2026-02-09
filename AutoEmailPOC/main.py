from fastapi import FastAPI,BackgroundTasks
from email_utils import send_email_util
from dotenv import load_dotenv



from datetime import datetime,timedelta
from scheduler import schedule_email_job
from dayscheduler import schedule_day_email
from intervalscheduler import add_interval_email_job
from cronscheduler import add_cron_email_job

load_dotenv()

app=FastAPI()


@app.post("/send-email")
def send_email_api(background_tasks:BackgroundTasks):
    to_email = "noor_fastapi_2026@mailinator.com"

    background_tasks.add_task(
        send_email_util,
        to_email,
        "AutoEmailPOC",
        "<h2>Hello this is automatic email generating poc</h2>"
        )

    return{
        "message":"Email queued successfully"
        }




@app.post("/schedule-mail")
def schedule_mail_api():
    to_email="noor_fastapi_2026@mailinator.com" # this is mailinator test email
    run_time=datetime.now()+timedelta(minutes=1)

    schedule_email_job(
        to_email=to_email,
        subject="Scheduled Email",
        body="<h2>Hello Noor</h2><p>This is scheduled email</p>",
        run_at=run_time
    )
    return{
        "message":"Email scheduled successfully",
        "scheduled_time":run_time
    }



@app.post("/schedule-day-email")
def schedule_mail_day():
    to_email="Reenu@123gmail.com"
    subject="Happy Birthday"
    body="Happy Birthday ,May you get whatevr you wish for"

    run_date=datetime(2026,7,17,0,0) #this formate is in the form of YYYY,MM,DD,HH,MIN
 #run_date = birthday_date - timedelta(days=1) #for sending 1 day advance mail
    schedule_day_email(
        to_email=to_email,
        subject=subject,
        body=body,
        target_date=run_date,
        days_before=1
    )

    return {
        "message":"Day based email scheduled succesfully"
       
   }


@app.post("/scheduler-interval-mail")
def schedule_interval_mail_api():
    to_email="Noor@gmail.com"
    subject="Interval reminder"
    body="This is an interval based reminder email"

    add_interval_email_job(
        to_email=to_email,
        subject=subject,
        body=body,
        days=1
    )
    return {
        "message":"Interval-based email scheduled successfully"
    }


@app.post("/scheduler-cron-mail")
def schedule_cron_main_api():
    to_email="Noor@gmail.com"
    subject="Cron Email"
    body="This email is sent using cron scheduler"
    #to send mails ate every monday at 10:00am
    add_cron_email_job(
        to_email=to_email,
        subject=subject,
        body=body,
        day_of_week="mon", 
        #if we want to send on every two three days means we can add like 
        #day_of_week="mon,thursday"
        hour=10,
        minute=0

    )

    return {
        "message":"Cron email scheduled succesfully"
    }



