from main import main
from log_config import scheduler_logger
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR


scheduler = BlockingScheduler()

#trigger = CronTrigger.from_crontab('0 * * * *')  # Runs every hour at minute 0

trigger = CronTrigger(minute = 0) # same job as the above trigger - just simpler

job_defaults = { 'coalesce': True, 'max_instances': 1, 'misfire_grace_time': 180}

  
scheduler.configure(job_defaults = job_defaults)
scheduler.add_job(main, trigger = trigger)

def job_listener(event):
    if event.exception:
        scheduler_logger.error(f"Pipeline failed, {event.exception}")
    else:
        scheduler_logger.info("Pipeline finished successfully")

scheduler.add_listener(
    job_listener,
    EVENT_JOB_EXECUTED | EVENT_JOB_ERROR
)


try:
    scheduler_logger.info("Scheduler started")
    scheduler.start()
except (KeyboardInterrupt, SystemExit):
    scheduler_logger.info("Scheduler stopped.")





