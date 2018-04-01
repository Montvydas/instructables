# linux: pip install apscheduler
# mac: pip install --user apscheduler

from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from datetime import timedelta

scheduler = BackgroundScheduler()
scheduler.start()

def printText(text):
    global scheduler
    print text
    scheduler.print_jobs()

now = datetime.now()
extra = timedelta(seconds=10)
scheduler.add_job(printText, trigger='date', run_date=now+extra, args=["Hello from now+extra"], id='first_job')
scheduler.add_job(printText, trigger='date', run_date=now+extra+extra, args=["Hello from now+extra+extra"], id='second_job')
scheduler.print_jobs()