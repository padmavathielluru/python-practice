from scheduler import scheduler
from email_utils import send_email_util

def add_interval_email_job(
        to_email:str,
        subject:str,
        body:str,
        days:int,
        
        #minutes:int | None=None,
        #hours:int | None=None,
        #days:int | None=None
):
    scheduler.add_job(
          send_email_util,
          trigger='interval',
          #minutes=minutes,
          #hours=hours,
          days=days,
          args=[to_email,subject,body]

    )


"""
    Interval-based email scheduler

    Example:
    - minutes=10  -> every 10 minutes
    - hours=2     -> every 2 hours
    - days=7      -> every 7 days
"""
    
    