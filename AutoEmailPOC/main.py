from fastapi import FastAPI,BackgroundTasks
from email_utils import send_email_util
from dotenv import load_dotenv



from datetime import datetime,timedelta
from scheduler import schedule_email_job


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