from datetime import datetime,timedelta
from scheduler import scheduler
from email_utils import send_email_util

def schedule_day_email(
        to_email:str,
        subject:str,
        body:str,
        target_date:datetime, #actual date (birthday / event date)
        days_before:int=0 #how many days before we should send mail

):
    run_date=target_date-timedelta(days=days_before)

    scheduler.add_job(
        send_email_util,
        trigger="date",
        run_date=run_date,
        args=[to_email,subject,body]
    )
   
#logic for sheduling an email at one time like on that particular date,for suppose any friend birthday like that 
