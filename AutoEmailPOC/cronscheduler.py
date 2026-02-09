from scheduler import scheduler
from email_utils import send_email_util

def add_cron_email_job(
        to_email:str,
        subject:str,
        body:str,
        day_of_week:str | None=None,
        day:int |None=None,
        hour:int=10,
        minute:int=0
):
    
    scheduler.add_job(
        send_email_util,
        trigger='cron',
        day_of_week=day_of_week,
        day=day,
        hour=hour,
        minute=minute,
        args=[to_email,subject,body]

    )
"""
    Cron-based email scheduler

    Examples:
    - day_of_week="mon"        -> every Monday
    - day=1                    -> every month 1st
    - day_of_week="mon,fri"    -> Monday & Friday
"""