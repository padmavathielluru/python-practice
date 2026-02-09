from apscheduler.schedulers.background import BackgroundScheduler

from email_utils import send_email_util

from datetime import datetime

scheduler=BackgroundScheduler()


def schedule_email_job(to_email:str,subject:str,body:str,run_at):
    #run_at is used to schedule the time when we wanted to send that email
    
    scheduler.add_job(
        send_email_util,
        trigger="date",
        run_date=run_at,
        args=[to_email,subject,body]

    )
scheduler.start()
