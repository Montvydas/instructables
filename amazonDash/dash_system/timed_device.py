from datetime import datetime
from datetime import timedelta


class TimedDevice:
    def __init__(self, device, scheduler, job_id,
                 trigger_on="turn_on", trigger_off="turn_off",
                 hours=0, minutes=0, seconds=0):
        self.device = device
        # how long should a single click run for
        self.trigger_on = trigger_on
        self.trigger_off = trigger_off
        self.timeout = timedelta(hours=hours, minutes=minutes, seconds=seconds)
        self.scheduler = scheduler
        self.job_id = job_id

    def get_name(self):
        return self.device.get_name()

    def set_timeout(self, hours=0, minutes=0, seconds=0):
        self.timeout = timedelta(hours=hours, minutes=minutes, seconds=seconds)

    def stop_timer(self):
        # get the job by the id
        job = self.get_job()
        # if job exists, remove it and trigger the set off action
        if job:
            getattr(self.device, self.trigger_off)()
            job.remove()

    def start_timer(self):
        # get the job by the id
        job = self.get_job()
        # if we don't have a job, make one
        if job is None:
            now = datetime.now()
            # Set the trigger OFF function
            self.scheduler.add_job(getattr(self.device, self.trigger_off),
                                   trigger='date', run_date=now + self.timeout, id=self.job_id)
            # now trigger the ON action
            getattr(self.device, self.trigger_on)()
        else:
            print "Job is already started!"

    def add_extra(self):
        # get the job by the id
        job = self.get_job()
        # if job exists, add extra
        if job:
            self.scheduler.reschedule_job(self.job_id, trigger='date', run_date=job.next_run_time + self.timeout)
            print "Added EXTRA"

    def get_job(self):
        return self.scheduler.get_job(self.job_id)

    def start_or_add_timer(self):
        if self.get_job() is None:
            self.start_timer()
        else:
            self.add_extra()
