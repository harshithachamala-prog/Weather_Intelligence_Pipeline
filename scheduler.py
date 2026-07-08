from main import main
from logs.log_config import scheduler_logger
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger


scheduler = BlockingScheduler()

#trigger = CronTrigger.from_crontab('0 * * * *')  # Runs every hour at minute 0

trigger = CronTrigger(minute=0) # same job as the above trigger - just simpler

job_defaults = { 'coalesce': True, 'max_instances': 1, 'misfire_grace_time': 180}

scheduler.configure(job_defaults = job_defaults)
scheduler.add_job(main, trigger = trigger)

try:
    scheduler_logger.info("Scheduler started")
    scheduler.start()
except (KeyboardInterrupt, SystemExit):
    scheduler_logger.info("Scheduler stopped.")



